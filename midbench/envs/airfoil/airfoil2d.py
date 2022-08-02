# from typing import Optional, Union
import numpy as np
import os, sys, shutil, glob
import pandas as pd
sys.path.append(os.environ['SU2_RUN'])
import SU2
import midbench


class Airfoil2dCondition(midbench.core.Condition):
    def __init__(
        self, 
        mach = 0.8, 
        reynolds = 8000000, 
        lift = 0.348, 
        aoa = 0,
        projectname = '',
        partitions = 0,
        gradient = 'CONTINUOUS_ADJOINT',
        optimization = 'SLSQP',
        quiet = False,
        nzones = 1,
    ):
        self.mach = mach
        self.reynolds = reynolds
        self.lift = lift
        self.aoa = aoa      
        self.projectname = projectname                   
        self.partitions  = partitions                   
        self.gradient    = gradient
        self.optimization = optimization
        self.quiet       = quiet
        self.nzones      = nzones


class Airfoil2dDesign(midbench.core.Design):
    def __init__(
        self, 
        air_coord_path= 'airfoils_pred_cbegan_example.npy', 
        su2='mesh_NACA0012_inv.su2',
    ):
        self.air_coord_path = air_coord_path
        self.su2 = os.path.abspath(su2)
            
    def meshgen(self):
        air_coord = np.load(self.air_coord_path)
        air_coord[0,:,0] = (air_coord[0,:,0] - np.amin(air_coord[0,:,0]))/(np.amax(air_coord[0,:,0])-np.amin(air_coord[0,:,0]))
        np.savetxt(os.path.dirname(self.air_coord_path) + '/air_coord.dat', air_coord[0,:,:], delimiter='     ')
        
        # Converter the .dat points to .su2 mesh
        os.system('AirfoilGeometryConverter -i ' + os.path.dirname(self.air_coord_path) + '/air_coord.dat -o ' 
                  + os.path.dirname(self.air_coord_path) + '/air_coord -f su2 -frf circle')
        
        su2_abspath = os.path.abspath(os.path.dirname(self.air_coord_path) + '/air_coord.su2')
        self.su2 = su2_abspath
        
        return self
    

class Airfoil2dEnv(midbench.core.Env):
    """
    ### Arguments

    ```
    midbench.make('Airfoil2d')
    ```

    No additional arguments are currently supported.
    """

    def __init__(
        self, 
        cfgfile_simu = '/config_simu.cfg',
        cfgfile_opt = '/config_opt.cfg',
    ):
        self.cfgfile_simu = cfgfile_simu
        self.cfgfile_opt = cfgfile_opt
        
        
    def simulate(self, conditions, designs, performances, results_dir_simu):
        
        config = SU2.io.Config(os.path.dirname(designs.su2) + self.cfgfile_simu)
        config.MACH_NUMBER = conditions.mach
        config.REYNOLDS_NUMBER = conditions.reynolds
        config.TARGET_CL = conditions.lift
        config.AOA = conditions.aoa
        config.MESH_FILENAME = designs.su2     # Customize mesh filename in the configuration file
        # config.CONV_FILENAME = 'history' + filename # Customize the history filename in the configuration file
        SU2.io.Config.write(config, os.path.dirname(designs.su2) + self.cfgfile_simu)        # Regenerate the configuration file with the same filename
        cfgfile_simu_abspath = os.path.abspath(os.path.dirname(designs.su2) + self.cfgfile_simu) 
        
        # Run the simulation using SU2 simulator
        if not os.path.exists(results_dir_simu):
            os.makedirs(results_dir_simu)
        os.chdir(results_dir_simu)
        os.system('SU2_CFD ' + cfgfile_simu_abspath)
        
        # Extract the drag and lift coefficients from the history file
        data = pd.read_csv('history.csv')
        data.dropna(inplace = True) # dropping null value columns to avoid errors
        for name in performances:
            if name == 'drag':
                cd = data['       "CD"       '][data.index[-1]]
            elif name == 'lift':
                cl = data['       "CL"       '][data.index[-1]]
        
        os.chdir("../../../..")
        
        return cd, cl
    
    def optimize(self, conditions, designs, objectives, results_dir_opt):      
        # Config
        os.chdir(os.path.abspath(os.path.dirname(designs.su2)))
        config = SU2.io.Config(os.path.dirname(designs.su2) + self.cfgfile_opt)
        config.NUMBER_PART = conditions.partitions
        config.NZONES      = int( conditions.nzones )
        if conditions.quiet: config.CONSOLE = 'CONCISE'
        config.GRADIENT_METHOD = conditions.gradient
        config.MACH_NUMBER = conditions.mach
        config.REYNOLDS_NUMBER = conditions.reynolds
        config.TARGET_CL = conditions.lift
        config.AOA = conditions.aoa
        config.MESH_FILENAME = os.path.basename(designs.su2) # Customize mesh filename in the configuration file
        
        its               = int ( config.OPT_ITERATIONS )                      # number of opt iterations
        bound_upper       = float ( config.OPT_BOUND_UPPER )                   # variable bound to be scaled by the line search
        bound_lower       = float ( config.OPT_BOUND_LOWER )                   # variable bound to be scaled by the line search
        relax_factor      = float ( config.OPT_RELAX_FACTOR )                  # line search scale
        gradient_factor   = float ( config.OPT_GRADIENT_FACTOR )               # objective function and gradient scale
        def_dv            = config.DEFINITION_DV                               # complete definition of the desing variable
        n_dv              = sum(def_dv['SIZE'])                                # number of design variables
        accu              = float ( config.OPT_ACCURACY ) * gradient_factor    # optimizer accuracy
        x0                = [0.0]*n_dv # initial design
        xb_low            = [float(bound_lower)/float(relax_factor)]*n_dv      # lower dv bound it includes the line search acceleration factor
        xb_up             = [float(bound_upper)/float(relax_factor)]*n_dv      # upper dv bound it includes the line search acceleration fa
        xb                = list(zip(xb_low, xb_up)) # design bounds
        
        # State
        state = SU2.io.State()
        state.find_files(config)
    
        # add restart files to state.FILES
        if config.get('TIME_DOMAIN', 'NO') == 'YES' and config.get('RESTART_SOL', 'NO') == 'YES' and conditions.gradient != 'CONTINUOUS_ADJOINT':
            restart_name = config['RESTART_FILENAME'].split('.')[0]
            restart_filename = restart_name + '_' + str(int(config['RESTART_ITER'])-1).zfill(5) + '.dat'
            if not os.path.isfile(restart_filename): # throw, if restart files does not exist
                sys.exit("Error: Restart file <" + restart_filename + "> not found.")
            state['FILES']['RESTART_FILE_1'] = restart_filename
    
            # use only, if time integration is second order
            if config.get('TIME_MARCHING', 'NO') == 'DUAL_TIME_STEPPING-2ND_ORDER':
                restart_filename = restart_name + '_' + str(int(config['RESTART_ITER'])-2).zfill(5) + '.dat'
                if not os.path.isfile(restart_filename): # throw, if restart files does not exist
                    sys.exit("Error: Restart file <" + restart_filename + "> not found.")
                state['FILES']['RESTART_FILE_2'] =restart_filename 
    
        # Project
        if os.path.exists(conditions.projectname):
            project = SU2.io.load_data(conditions.projectname)
            project.config = config
        else:
            project = SU2.opt.Project(config,state,folder = results_dir_opt)
            
        # Optimize
        if conditions.optimization == 'SLSQP':
          SU2.opt.SLSQP(project,x0,xb,its,accu)
        if conditions.optimization == 'CG':
          SU2.opt.CG(project,x0,xb,its,accu)
        if conditions.optimization == 'BFGS':
          SU2.opt.BFGS(project,x0,xb,its,accu)
        if conditions.optimization == 'POWELL':
          SU2.opt.POWELL(project,x0,xb,its,accu)
    
        # rename project file
        if conditions.projectname:
            shutil.move('project.pkl',conditions.projectname)
        
        # Objectives
        para = pd.read_csv(results_dir_opt + '/history_project.csv')
        para.dropna(inplace = True) # dropping null value columns to avoid errors
        
        # Optimized airfoil
        list_of_folders = glob.glob(results_dir_opt + '/DESIGNS/*') # * means all if need specific format then *.csv
        sorted_folder = sorted(list_of_folders, key=os.path.getctime)
        try:
            data = pd.read_csv(sorted_folder[-1] + '/DIRECT/surface_flow.csv')
        except OSError:
            data = pd.read_csv(sorted_folder[-2] + '/DIRECT/surface_flow.csv')
        
        for name in objectives:
            if name == 'drag':
                cd = para[' "DRAG"          '][para.index[-1]]
            elif name == 'ld_ratio':
                ld = para[' "EFFICIENCY"    '][para.index[-1]]
            elif name == 'airfoil_opt':
                airfoil_opt_x = data['x']
                airfoil_opt_y = data['y']
                airfoil_opt = [airfoil_opt_x, airfoil_opt_y]
                
        return cd, ld, airfoil_opt

 