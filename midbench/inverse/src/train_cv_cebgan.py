import torch
import numpy as np
import os, json

from datetime import datetime
from sklearn.model_selection import train_test_split, KFold
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
from models.cgans import AirfoilAoACEGAN, AirfoilAoADiscriminator1D, AirfoilAoAGenerator
from utils.dataloader import AirfoilDataset, NoiseGenerator
from utils.shape_plot import plot_samples, plot_comparision
from torchvision.transforms import Normalize
from utils.metrics import ci_cons, ci_mll, ci_rsmth, ci_rdiv, ci_mmd

cost1 = lambda x1, x2: torch.cdist(x1[0].flatten(1), x2[0].flatten(1), p=1) \
    + torch.cdist(x1[1], x2[1], p=1) \
    + torch.cdist(x1[2], x2[2], p=1)
cost2 = lambda x1, x2: torch.cdist(x1[0].flatten(1), x2[0].flatten(1), p=2) \
    + torch.cdist(x1[1], x2[1], p=2) \
    + torch.cdist(x1[2], x2[2], p=2)

def read_configs(name, base_dir="./"):
    with open(os.path.join(base_dir, 'configs', name+'.json')) as f:
        configs = json.load(f)
        dis_cfg = configs['dis']
        gen_cfg = configs['gen']
        egan_cfg = configs['egan']
        cz = configs['cz']
        noise_type = configs['noise_type']
    return dis_cfg, gen_cfg, egan_cfg, cz, noise_type

def assemble_new_gan(dis_cfg, gen_cfg, egan_cfg, device='cpu'):
    discriminator = AirfoilAoADiscriminator1D(**dis_cfg).to(device)
    generator = AirfoilAoAGenerator(**gen_cfg).to(device)
    egan = AirfoilAoACEGAN(generator, discriminator, 
        cost_func=cost2, 
        **egan_cfg)
    return egan

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    batch = 128 #[36, 64, 128, 250, 400]
    epoch = 7000 #[2000, 3500, 7000, 14000, 21000]
    save_intvl = 1000
    kf = KFold(n_splits=4)

    dis_cfg, gen_cfg, egan_cfg, cz, noise_type = read_configs('cebgan')
    # data_fname = '../data/airfoil_interp.npy'
    # data_fname = '../data/train.npy'
    save_dir = '../saves/tuning'
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'runs'), exist_ok=True)

    airfoils_opt = np.load('../data/airfoils_opt_995.npy').astype(np.float32)
    inp_paras = np.load('../data/inp_paras_995.npy').astype(np.float32)
    aoas_opt = np.load('../data/aoas_opt_995.npy').astype(np.float32).reshape(-1, 1)
    mean_std = (inp_paras.mean(0), inp_paras.std(0))

    
    time = datetime.now().strftime('%b%d_%H-%M-%S')
    save_iter_list = list(np.linspace(1, epoch/save_intvl, dtype=int) * save_intvl - 1)
    
    for fold, (train_index, test_index) in enumerate(kf.split(aoas_opt)):
        airfoils_train, airfoils_test = airfoils_opt[train_index], airfoils_opt[test_index]
        inp_paras_train, inp_paras_test = inp_paras[train_index], inp_paras[test_index]
        aoas_opt_train, aoas_opt_test = aoas_opt[train_index], aoas_opt[test_index]

        # build entropic gan on the device specified
        egan = assemble_new_gan(dis_cfg, gen_cfg, egan_cfg, device=device)

        # build dataloader and noise generator on the device specified
        dataset = AirfoilDataset(inp_paras_train, airfoils_train, aoas_opt_train, inp_mean_std=mean_std, device=device)
        dataloader = DataLoader(dataset, batch_size=batch, shuffle=True)
        noise_gen = NoiseGenerator(batch, sizes=cz, noise_type=noise_type, device=device) # all Gaussian noise

        # build tensorboard summary writer
        tb_dir = os.path.join(save_dir, 'runs/cost', 'b{}_e{}_l{}'.format(batch, epoch, egan_cfg['lamb']), 'fold_{}'.format(fold))
        os.makedirs(os.path.join(tb_dir, 'images'), exist_ok=True)
        writer = SummaryWriter(tb_dir)
        
        def epoch_plot(epoch, batch, fake, *args, **kwargs):
            if (epoch + 1) % 50 == 0:
                num = min(36, len(fake[0]))
                airfoils, aoas_opt, _ = batch
                airfoils = airfoils.cpu().detach().numpy().transpose([0, 2, 1])[:num]
                aoas_opt = aoas_opt.cpu().detach().numpy().squeeze()[:num]
                pred_airfoils = fake[0].cpu().detach().numpy().transpose([0, 2, 1])[:num]
                pred_aoas = fake[1].cpu().detach().numpy().squeeze()[:num]
                # plot_samples(
                #     None, fake_airfoils, annotate=pred_aoas, scale=1.0, scatter=False, symm_axis=None, lw=1.2, alpha=.7, c='k', 
                #     fname=os.path.join(tb_dir, 'images', 'epoch {}'.format(epoch+1))
                #     )
                plot_comparision(
                    None, airfoils, [pred_airfoils], aoas_opt, pred_aoas, scale=1.0, scatter=False, symm_axis=None, 
                    fname=os.path.join(tb_dir, 'images', 'epoch {}'.format(epoch+1))
                    )

        egan.train(
            epochs=epoch,
            num_iter_D=1, 
            num_iter_G=1,
            dataloader=dataloader, 
            noise_gen=noise_gen, 
            tb_writer=writer,
            report_interval=1,
            save_dir=save_dir,
            save_iter_list=save_iter_list,
            plotting=epoch_plot
            )


        # test on validation set
        def build_gen_func(inp_paras):
            def gen_func(N=1): # [ao, ip] tuple
                tuples = []
                egan.generator.eval()
                for i in range(N):
                    noise = NoiseGenerator(len(inp_paras), cz, noise_type, device=device)()
                    pred = egan.generator(noise, torch.tensor(inp_paras, device=device, dtype=torch.float))[0]
                    af_pred = pred[0].cpu().detach().numpy().transpose([0, 2, 1]).reshape(len(pred[0]), -1)
                    ao_pred = pred[1].cpu().detach().numpy()
                    tuples.append(np.hstack([af_pred, ao_pred, inp_paras]))
                return np.concatenate(tuples)
            return gen_func
        
        n_run = 10

        inp_paras_train = (inp_paras_train - mean_std[0]) / mean_std[1]
        inp_paras_test = (inp_paras_test - mean_std[0]) / mean_std[1]

        X_train = np.hstack([airfoils_train.reshape(airfoils_train.shape[0], -1), aoas_opt_train, inp_paras_train])
        X_test = np.hstack([airfoils_test.reshape(airfoils_test.shape[0], -1), aoas_opt_test, inp_paras_test])
        train_mean, train_std = ci_mmd(n_run, build_gen_func(inp_paras_train), X_train)
        test_mean, test_std = ci_mmd(n_run, build_gen_func(inp_paras_test), X_test)

        with open(os.path.join(tb_dir, 'MMD_log.txt'), 'w') as f:
            f.write("MMD Train: {} ± {}".format(train_mean, train_std) + '\n')
            f.write("MMD Test: {} ± {}".format(test_mean, test_std) + '\n')

        # print("MMD Train: {} ± {}".format(*ci_mmd(n_run, build_gen_func(inp_paras_train), X_train)))
        # print("MMD Test: {} ± {}".format(*ci_mmd(n_run, build_gen_func(inp_paras_test), X_test)))