import torch
import numpy as np
import os
from models.cgans import AirfoilAoAGenerator
from train import read_configs
from utils.dataloader import NoiseGenerator
from utils.metrics import ci_cons, ci_mll, ci_rsmth, ci_rdiv, ci_mmd

def load_generator(gen_cfg, save_dir, checkpoint, device='cpu'):
    ckp = torch.load(os.path.join(save_dir, checkpoint))
    generator = AirfoilAoAGenerator(**gen_cfg).to(device)
    generator.load_state_dict(ckp['generator'])
    generator.eval()
    return generator

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    airfoils_opt = np.load('../data/airfoils_opt.npy').astype(np.float32)
    aoas_opt = np.load('../data/aoas_opt.npy').astype(np.float32).reshape(-1, 1)
    inp_paras = np.load('../data/inp_paras.npy').astype(np.float32)

    inp_paras = (inp_paras - inp_paras.mean(0)) / inp_paras.std(0)

    af_train, af_test = airfoils_opt[:780], airfoils_opt[780:]
    ao_train, ao_test = aoas_opt[:780], aoas_opt[780:]
    ip_train, ip_test = inp_paras[:780], inp_paras[780:]

    save_dir = '../saves/complete/runs/Feb05_01-07-14'
    _, gen_cfg, _, cz = read_configs('conditional')
    generator = load_generator(gen_cfg, save_dir, 'conditional4999.tar', device=device)

    def build_gen_func(inp_paras):
        def gen_func(N=1): # [ao, ip] tuple
            tuples = []
            for i in range(N):
                noise = NoiseGenerator(len(inp_paras), cz, device=device)()
                pred = generator(noise, torch.tensor(inp_paras, device=device, dtype=torch.float))[0]
                af_pred = pred[0].cpu().detach().numpy().transpose([0, 2, 1]).reshape(len(pred[0]), -1)
                ao_pred = pred[1].cpu().detach().numpy()
                tuples.append(np.hstack([af_pred, ao_pred, inp_paras]))
            return np.concatenate(tuples)
        return gen_func
    
    n_run = 10

    X_train = np.hstack([af_train.reshape(af_train.shape[0], -1), ao_train, ip_train])
    X_test = np.hstack([af_test.reshape(af_test.shape[0], -1), ao_test, ip_test])
    # print("MLL: {} ± {}".format(*ci_mll(n_run, gen_func, X_test)))
    # print("LSC: {} ± {}".format(*ci_cons(n_run, gen_func, cz[0])))
    # print("RVOD: {} ± {}".format(*ci_rsmth(n_run, gen_func, X_test)))
    # print("Diversity: {} ± {}".format(*ci_rdiv(n_run, X, gen_func)))
    print("MMD Train: {} ± {}".format(*ci_mmd(n_run, build_gen_func(ip_train), X_train)))
    print("MMD Test: {} ± {}".format(*ci_mmd(n_run, build_gen_func(ip_test), X_test)))