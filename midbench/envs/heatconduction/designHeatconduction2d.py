import glob, os, sys
import time as tm
import numpy as np
import time as tm
from math import floor

with open(r"./midbench/envs/heatconduction/Des_var.txt", 'r') as fp:
    lines = fp.read()
    lines2=lines.split("\t")
NN = int(lines2[1]) #70 for experiments #discretization resolution: somewhat arbitrary. NOTE: Increasing the int coeff dramatically increases model training and testing #time!!!
step = 1.0/float(NN)
x_values = np.zeros((NN+1)) #horizontal dir (x(0))
y_values = np.zeros((NN+1)) #vertical dir (x(1))
x_values=np.linspace(0,1,num=NN+1)
y_values=np.linspace(0,1,num=NN+1)
vol_f = float(lines2[0])
os.system('rm ./midbench/envs/heatconduction/Des_var.txt')
#Now set up
from fenics import *
V = Constant(vol_f)  # volume bound on the control.   Default = 0.4
mesh = UnitSquareMesh(NN, NN)
A = FunctionSpace(mesh, "CG", 1)  # function space for control
if __name__ == "__main__":
    MM = V
    a = interpolate(MM, A)  # initial guess.
    #xdmf_filename = XDMFFile(MPI.comm_world, "Design/initial_v="+str(vol_f)+"_resol="+str(NN)+"_.xdmf")
    #xdmf_filename.write(a)
    with XDMFFile("./midbench/envs/heatconduction/Design/initial_v="+str(vol_f)+"_resol="+str(NN)+"_.xdmf") as outfile:
        outfile.write(mesh)
        outfile.write_checkpoint(a, "u", 0, append=True)
    results = np.zeros(((NN+1)**2,3))
    ind = 0
    for xs in x_values:
        for ys in y_values:
            results[ind,0] = xs
            results[ind,1] = ys
            results[ind,2] =V
            ind = ind+1
    filename = "./midbench/envs/heatconduction/Design/initial_v="+str(vol_f)+"_resol="+str(NN)+"_.npy"
    np.save(filename,results)
