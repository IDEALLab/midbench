# Usage

## Build From Source (SU2 installation needed)

### SU2 Installation
Users who are interested in the open-source [SU2](https://su2code.github.io/) CFD solver can install the SU2 suite directly on you devices by following the intallation guide on SU2 official website.

* **Linux and Mac Users:** Please find the installation steps [here](https://su2code.github.io/docs_v7/Build-SU2-Linux-MacOS/) to install SU2 and enable SU2 python library:

    1. **Download source code:** Please first download the source code from the [SU2 download webpage](https://su2code.github.io/download.html).
    2. **Create a configuration using the `meson.py`:** `./meson.py build -Denable-autodiff=true`.
    3. **Set environment variables:** There will be an instruction showing up in the terminal window for setting environment variables after creating the configuration. Users can copy and paste the paths to the ~/.bashrc and `source ~/.bashrc`. If you miss the instruction, please follow this [link](https://su2code.github.io/docs_v7/SU2-Linux-MacOS/) to set up the environment variables.
    4. **Compile and install SU2:** `./ninja -C build install`.

* **Windows Users:** Please install SU2 and enable SU2 python library using the steps shown [here](https://su2code.github.io/docs_v7/SU2-Windows/).

<!-- The [Quick Start](https://sylabs.io/guides/3.6/user-guide/quick_start.html) guide on the official webpage provide clear and detailed installation steps. Users should be able to install Singularity successfully by just following the guide step by step. For our MID Benchmark Suite, the Singularity version 3.5.3 is used to build our Singularity containers for different environments. Users should be able to run the Singularity containers with the same version or higher. -->

### Run the MIDBench API code

* **Make sure you have installed midbench:**
```bash
pip install midbench
```

* **Clone midbench repo or download midbench repo:**
```bash
git clone https://github.com/IDEALLab/midbench.git
```

* **Set environment variable for 2D airfoil mesh generator:**
```bash
export PATH=$PATH:/Path/to/midbench/tutorials/airfoil2d/AirfoilGeometryConverter
```
Users can also add the path to ~/.bashrc and `source ~/.bashrc`.

* **set `./midbench` as working directory and open jupyter notebook or jupyter lab:**
```bash
jupyter-notebook
```

* In the tutorials, there is an iPython notebook [**"inverse_design_usage.ipynb"**](../tutorials/inverse_design_usage.ipynb). Please open the notebook in jupyter lab or jupyter notebook.

* Please run the API demo code in the notebook cell by cell to check out the **_2D Airfoil Inverse Design, Simulation, and Optimization_** demos

* The commands in the jupyter notebook are as follows:**

**Prediction (Inverse Design)**
```python
# Prediction (Inverse Design)
import midbench
from midbench.envs import make
import torch
import numpy as np
from midbench.inverse.src.pred import cebgan_pred

# Load input parameters (Mach number, Reynolds number, target lift coefficient)
inp_paras = np.load('./midbench/inverse/data/inp_paras_test.npy')[0,:].reshape(-1,3)

# Predict optimal airfoil and angle of attack using CEBGAN inverse model
airfoils, aoas = cebgan_pred(inp_paras)
```

**Simulation**
```python
# Simulation
# Direct to the Environment of 2D airfoil
Env, Design, Condition = make("Airfoil2d-v0")

# Convert airfoil coordinates to 2D mesh
designs = Design(air_coord_path = airfoils).meshgen() 

# Boundary condition setup for simulation
conditions = Condition(**{'mach':inp_paras[0,0],'reynolds':inp_paras[0,1],'lift':inp_paras[0,2],'aoa':aoas[0,0]})

# Target performances (e.g., lift and drag coefficients)
performances = ['lift', 'drag']

# Execute simulation
lift, drag = Env.simulate(conditions, designs, performances, './tutorials/airfoil2d/results_simu')
```

**Optimization**
```python
# Optimization
# Convert airfoil coordinates to 2D mesh
designs = Design(air_coord_path = airfoils).meshgen()

# Boundary condition setup for optimization
conditions = Condition(**{'mach':inp_paras[0,0],'reynolds':inp_paras[0,1],'lift':inp_paras[0,2],'aoa':aoas[0,0]})

# Objectives (e.g., drag coefficient, lift/drag efficiency, optimized airfoil coordinates)
objectives = ['drag', 'ld_ratio', 'airfoil_opt']

# Execute Optimization
drag, ld_ratio, airfoil_opt = Env.optimize(conditions, designs, objectives, './results_opt')
```


## SU2 Singularity Container (No SU2 installation needed) 

**_Inverse Design not enabled for current version, only simulation and optimization_**

We perform the 2D airfoil simulation and optimization using [SU2](https://su2code.github.io/) CFD solver. For user's easy usage, we have pre-built the SU2 suite using a [singularity container](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html) with the required environments set up. The ready-to-use SU2 singularity container can be pulled or downloaded from [https://cloud.sylabs.io/library/junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh](https://cloud.sylabs.io/library/junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh).

### Run the MIDBench API code
1. **Linux Users:** If you are using Linux (e.g., Ubuntu) or Linux VM box), please do the following steps:
    * Install Singularity. If you already have singularity installed on your device, please ignore this step. If not, please follow the [3-step quick installation guide](../installation.md) to install Singularity first. Our MID Benchmark Suite uses Singularity version 3.5.3. You should be able to run the SIF container with the same version or higher.
    * Download SU2 SIF container. Please download the SU2 SIF container from Sylabs using this link ([https://cloud.sylabs.io/library/junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh](https://cloud.sylabs.io/library/junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh)). After installing Singularity, you can also pull the SU2 SIF container using the following command: `$ singularity pull --arch amd64 library://junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh:latest`
    * Enter SU2 SIF container by typing the following command in your terminal: `singularity shell /path/to/your/downloaded/su2v7.3.1_conda3.9.12_gmsh_latest.sif`
    * Open jupyter notebook or jupyter lab by typing command in your terminal: `jupyter lab` or `jupyter-notebook`.
    * In the tutorials, there is an iPython notebook [**"example_usage.ipynb"**](../tutorials/example_usage.ipynb). Please open the notebook in jupyter lab or jupyter notebook.
    * Please run the API demo code in the notebook cell by cell to check out the **_2D Airfoil Simulation and Optimization_** demos in your SU2 SIF container.

2. **Windows Users:** If you are using Windows system and not interested in installing the Linux system or subsystem, you can directly implement our MIDBench API demos in [Google Colab Notebook](https://colab.research.google.com/) by following the installation and implementation steps below (we also include an iPython notebook [**_"singularity_SU2.ipynb"_**](../tutorials/singularity_SU2.ipynb) for Windows users to use directly in Colab):

<!-- * **Install System Dependencies:**
```bash
!sudo apt-get update && sudo apt-get install -y \
    build-essential \
    libssl-dev \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    libseccomp-dev \
    wget \
    pkg-config \
    git \
    cryptsetup
```

* **Install Go:**
```bash
%%bash
wget https://go.dev/dl/go1.18.4.linux-amd64.tar.gz && \
sudo rm -rf /usr/local/go && tar -C /usr/local -xzf go1.18.4.linux-amd64.tar.gz
```

* **Download Singularity:**
```bash
%%bash
export VERSION=3.5.3 && # adjust this as necessary \
  wget https://github.com/singularityware/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
  tar -xzf singularity-${VERSION}.tar.gz && \
  cd singularity
```

* **Compiling Singularity Source Code:**
```bash
%%shell
export PATH=$PATH:/usr/local/go/bin && \
source /etc/profile && \
go version && \
cd singularity && \
./mconfig && \
    make -C builddir && \
    sudo make -C builddir install
```

* **Verify Singularity Installation:**
```bash
!singularity version
```
 -->
* **Install Singularity:** Please follow the [3-step quick installation guide](../installation.md) to install Singularity. 
 
* **Pull SU2 SIF Container:**
```bash
!singularity pull --arch amd64 library://junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh:latest
```

* **Make sure you have installed midbench:**
```bash
pip install midbench
```

* **Clone midbench repo or download midbench repo:**
```bash
git clone https://github.com/IDEALLab/midbench.git
```

* **Create and Execute Python Scripts using SIF Container (recommended):**

```
# Simulation
%%writefile midbench/airfoil2d_simu.py
from midbench.envs import make
Env, Design, Condition = make("Airfoil2d-v0")

designs = Design(air_coord_path = './tutorials/airfoil2d/airfoils_pred_cbegan_example.npy').meshgen()
conditions = Condition(**{'mach':0.7,'reynolds':7000000,'lift':0.350})
performances = ['lift', 'drag']

lift, drag = Env.simulate(conditions, designs, performances, './tutorials/airfoil2d/results_simu')
print(lift, drag)
```

```bash
# Simulation
%%bash
cd midbench/
singularity exec --userns ../su2v7.3.1_conda3.9.12_gmsh_latest.sif bash -c "python airfoil2d_simu.py"
```

```
# Optimization
%%writefile midbench/airfoil2d_opt.py
from midbench.envs import make
Env, Design, Condition = make("Airfoil2d-v0")

designs = Design(su2='./tutorials/airfoil2d/mesh_NACA0012_inv.su2')
conditions = Condition(**{'mach':0.6,'reynolds':8000000,'lift':0.320})
objectives = ['drag', 'ld_ratio', 'airfoil_opt']

drag, ld_ratio, airfoil_opt = Env.optimize(conditions, designs, objectives, './results_opt')
print(drag, ld_ratio, airfoil_opt)
```

```bash
# Optimization
%%bash
cd midbench/
singularity exec --userns ../su2v7.3.1_conda3.9.12_gmsh_latest.sif bash -c "python airfoil2d_opt.py"
```

* **Alternatively, You can Spawn a New Shell within SIF Container:**
```bash
singularity shell --userns su2v7.3.1_conda3.9.12_gmsh_latest.sif
```

After entering SU2 SIF container, please run the 2D airfoil simulation and optimization demos using the following commands:

Type `python`. In the Python environment, please enter the following commands to run demos:
```python
from midbench.envs import make
Env, Design, Condition = make("Airfoil2d-v0")

# Simulation
designs = Design(air_coord_path = './tutorials/airfoil2d/airfoils_pred_cbegan_example.npy').meshgen()
conditions = Condition(**{'mach':0.7,'reynolds':7000000,'lift':0.350})
performances = ['lift', 'drag']

lift, drag = Env.simulate(conditions, designs, performances, './tutorials/airfoil2d/results_simu')

# Optimization
designs = Design(su2='./tutorials/airfoil2d/mesh_NACA0012_inv.su2')
conditions = Condition(**{'mach':0.6,'reynolds':8000000,'lift':0.320})
objectives = ['drag', 'ld_ratio', 'airfoil_opt']

drag, ld_ratio, airfoil_opt = Env.optimize(conditions, designs, objectives, './results_opt')
print(drag, ld_ratio, airfoil_opt)
```

__**NOTE**:__ The singuarity container also includes a 2D airfoil mesh generator `AirfoilGeometryConverter`. The generator will first convert the 2D coordinates of the airfoil curve points into mesh. The SU2 solver then takes the mesh for the follwoing CFD simulation and shape optimization.
