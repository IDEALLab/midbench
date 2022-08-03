import os, sys
import numpy as np
import midbench

class Heatconduction2dCondition(midbench.core.Condition):
    def __init__(self,volume = 0.5, length = 0.5,resolution = 50):
        self.volume = volume
        self.length = length
        self.resolution = resolution

class Heatconduction2dDesign(midbench.core.Design):
    def __init__(self,volume = 0.5,resolution = 50):
        self.volume = volume
        self.resolution = resolution

    def output(self):
        # volume=self.volume
        # resolution=self.resolution
        with open('./tutorials/heatconduction2d/Des_var.txt', 'w') as f:
            f.write('%f'%self.volume+"\t"+'%d'%self.resolution)
            f.close()
        os.system('python3 ./tutorials/heatconduction2d/designHeatconduction2d.py')
        self.design=np.load("./tutorials/heatconduction2d/Design/initial_v="+str(self.volume)+"_resol="+str(self.resolution)+"_.npy")
        self.xdmf="./tutorials/heatconduction2d/Design/initial_v="+str(self.volume)+"_resol="+str(self.resolution)+"_.xdmf"

        return self

class Heatconduction2dEnv(midbench.core.Env):
    def simulate(self, conditions, designs, performances):
        volume=conditions.volume
        length=conditions.length 
        resolution=conditions.resolution
        with open('sim_var.txt', 'w') as f:
            f.write('%f'%volume+"\t"+'%f'%length+"\t"+'%d'%resolution)
            f.close()
        with open('sim_design.txt', 'w') as des:
            des.write('%s'%designs.xdmf+"\t"+'%d'%designs.resolution)
            des.close()
        os.system('python3 ./tutorials/heatconduction2d/simulateHeatconduction2d.py')

        with open(r"./tutorials/heatconduction2d/RES_SIM/Performance.txt", 'r') as fp:
            PERF = fp.read()
        
        return float(PERF)

    def optimize(self, conditions, designs, objectives):
        volume=conditions.volume
        length=conditions.length
        resolution=conditions.resolution
        with open('OPT_var.txt', 'w') as f:
            f.write('%f'%volume+"\t"+'%f'%length+"\t"+'%d'%resolution)
            f.close()
        with open('OPT_design.txt', 'w') as des:
            des.write('%s'%designs.xdmf+"\t"+'%d'%designs.resolution)
            des.close()
        os.system('python3 ./tutorials/heatconduction2d/optimizeHeatconduction2d.py')

        with open(r"./tutorials/heatconduction2d/RES_OPT/Performance.txt", 'r') as fp:
            PERF = fp.read()

        return float(PERF)
