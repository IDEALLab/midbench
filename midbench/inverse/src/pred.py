import sys; sys.path.append('./midbench/inverse/src/')
import torch
import numpy as np
import os
import matplotlib.pyplot as plt
from .models.cgans import AirfoilAoAGenerator
from .train_final_cebgan import read_configs

def load_generator(gen_cfg, save_dir, checkpoint, device='cpu'):
    ckp = torch.load(os.path.join(save_dir, checkpoint), map_location=torch.device('cpu'))
    # ckp = torch.load(os.path.join(save_dir, checkpoint))
    generator = AirfoilAoAGenerator(**gen_cfg).to(device)
    generator.load_state_dict(ckp['generator'])
    generator.eval()
    return generator

# if __name__ == '__main__':
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

save_dir = './midbench/inverse/saves/final/'
_, gen_cfg, _, cz, _ = read_configs('cebgan')
epoch = 15000

inp_paras = np.load('./midbench/inverse/data/inp_paras_995.npy')
mean, std = inp_paras.mean(0), inp_paras.std(0)


def cebgan_pred(inp_paras):
 # reload inp_paras from Jun's test set.
    tr_inp_paras = (inp_paras - mean) / std

    generator = load_generator(gen_cfg, save_dir, 'cebgan{}.tar'.format(epoch-1), device=device)
    params = torch.tensor(tr_inp_paras, dtype=torch.float, device=device)

    noise = torch.zeros([len(params), cz[0]], device=device, dtype=torch.float)
    pred = generator(noise, params)[0]
    designs = pred[0].cpu().detach().numpy().transpose([0, 2, 1])
    aoas = pred[1].cpu().detach().numpy()
    np.save('./tutorials/airfoil2d/air_coord_pred.npy', designs)
    airfoils = './tutorials/airfoil2d/air_coord_pred.npy'
    return airfoils, aoas


# inp_paras = np.load('../data/inp_paras_test.npy')
# print(cebgan_pred(inp_paras))