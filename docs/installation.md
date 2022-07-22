Installing the full MID Benchmark Suite has three main parts:

1. Installing the MID Benchmark Suite core library -- this handles common functions across the entire suite, such as the main classes, computing common ID metrics, etc.
2. Downloading any datasets or pre-trained models that you desire. These are existing curated datasets that we have used in past publications and that are compatible with the MID Benchmark Suite. We do not download these by default, though there are opens in both the install and when using the API to download these when needed.
3. Installing the individual simulation environments -- these are only needed if you wish to run more advanced metrics that require actually evaluating a given engineering solver.

You can run certain models and metrics using only the core MID library, however for most meaningful benchmarks you will need to access to at least one simulation environment.

# Installing the core MID Benchmark Suite Library

For the baseline library, you can install this with `pip` via:

```bash
pip install midbench
```

# Download ID Datasets and Pre-trained Baseline Models

# Installing Simulation and Optimization Containers

## Singularity Container

Singularity is a container platform. It allows you to create and run containers that package up pieces of software in a way that is portable and reproducible. You can build a container using Singularity on your laptop, and then run it on many of the largest HPC clusters in the world, local university or company clusters, a single server, in the cloud, or on a workstation down the hall. Your container is a single file, and you don’t have to worry about how to install all the software you need on each different operating system.

Singularity was created to run complex applications on HPC clusters in a simple, portable, and reproducible way. First developed at Lawrence Berkeley National Laboratory, it quickly became popular at other HPC sites, academic sites, and beyond. Singularity is an open-source project, with a friendly community of developers and users. The user base continues to expand, with Singularity now used across industry and academia in many areas of work.

Many container platforms are available, but Singularity is focused on:

* Verifiable reproducibility and security, using cryptographic signatures, an immutable container image format, and in-memory decryption.

* Integration over isolation by default. Easily make use of GPUs, high speed networks, parallel filesystems on a cluster or server by default.

* Mobility of compute. The single file SIF container format is easy to transport and share.

* A simple, effective security model. You are the same user inside a container as outside, and cannot gain additional privilege on the host system by default. Read more about Security in Singularity.

*For more information about Singularity Container, please check the [official website](https://sylabs.io/guides/3.6/user-guide/introduction.html).*

### Installing Singularity

You will need a **Linux** system to run Singularity natively. Options for using Singularity on Mac and Windows machines, along with alternate Linux installation options are discussed [here](https://docs.sylabs.io/guides/3.5/admin-guide/installation.html#installation-on-windows-or-mac).

#### Install System Dependencies

You must first install development libraries to your host.

```bash
$ sudo apt-get update && sudo apt-get install -y \
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

#### Three steps to install Singularity:

1. [Installing GO (Linux)](https://go.dev/doc/install)

2. Downloading Singularity

3. Compiling Singularity Source Code


##### Download Singularity from a release

You can download Singularity from one of the releases. To see a full list, visit the [GitHub release page](https://github.com/sylabs/singularity/releases). After deciding on a release to install, you can run the following commands to proceed with the installation.

```bash
$ export VERSION=3.5.3 && # adjust this as necessary \
    wget https://github.com/singularityware/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
    tar -xzf singularity-${VERSION}.tar.gz && \
    cd singularity
```
For our MID Benchmark Suite, the Singularity version 3.5.3 is used to build our Singularity containers for different environments. Users should be able to run the Singularity containers with the same version or higher.

##### Compile the Singularity source code

Now you are ready to build Singularity. You can build Singularity using the following commands:

```bash
$ ./mconfig && \
    make -C builddir && \
    sudo make -C builddir install
```

Singularity must be installed as root to function properly. You can verify you've installed Singularity by typing the following command:

```bash
$ singularity version
```

Confirm that the command prints the installed version of Singularity.

We use Singularity containers for many of our different environments. An example of using SU2 Singularity container for 2D airfoil simulation and optimization can be found in one of our tutorials about the [2D airfoil inverse design](tutorials/airfoil-su2-singularity.md).

<!--
### Usage

<!-- The [Quick Start](https://sylabs.io/guides/3.6/user-guide/quick_start.html) guide on the official webpage provide clear and detailed installation steps. Users should be able to install Singularity successfully by just following the guide step by step. For our MID Benchmark Suite, the Singularity version 3.5.3 is used to build our Singularity containers for different environments. Users should be able to run the Singularity containers with the same version or higher.

#### SU2 Singularity Container

We perform the 2D airfoil simulation and optimization using [SU2](https://su2code.github.io/) CFD solver. For user's easy usage, we have pre-built the SU2 suite using a [singularity container](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html) with the required environments set up. The ready-to-use SU2 singularity container can be pulled or downloaded from https://cloud.sylabs.io/library/junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh.

* **Install Singularity**. If you already have singularity installed on your device, please ignore this step. If not, please follow this 3-step quick installation guide above to install Singularity first. Our MID Benchmark Suite uses Singularity version 3.5.3. You should be able to run the SIF container with the same version or higher.

* **Download SU2 SIF container**. Please download the SU2 SIF container from Sylabs using this link (https://cloud.sylabs.io/library/junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh). After installing Singularity, you can also pull the SU2 SIF container using the following command: `$ singularity pull --arch amd64 library://junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh:sha256.c6bf72230e360d23e2acdc8fc5cf9b8d26a3b709cc0c96feaaba42b60a611158`   

* **To run the MIDBench API code**:
    1. **Linux Users:** If you are using Linux (e.g., Ubuntu) or Linux VM box), please do the following steps:
        * Enter SU2 SIF container by typing the following command in your terminal: `singularity shell /path/to/your/downloaded/su2v7.3.1_conda3.9.12_gmsh.sif`
        * Open jupyter notebook or jupyter lab by typing command in your terminal: `jupyter lab` or `jupyter-notebook`.
        * Download our **_"MIDBenchmarkSuite.zip_**" from https://github.com/IDEALLab/MIDBenchmarkSuite or `git clone https://github.com/IDEALLab/MIDBenchmarkSuite.git`. In the MIDBenchmarkSuite directory, there is an iPython notebook **_“midbench_api.ipynb”_**. Please open the notebook in jupyter lab or jupyter notebook.
        * Please run the API demo code in the notebook cell by cell to check out the **_2D Airfoil Simulation and Optimization_** demos in your SU2 SIF container.

    2. **Windows Users:** If you are using Windows system and not interested in installing the Linux system or subsystem, you can directly use [Google Colab](https://colab.research.google.com/) to implement our MIDBench API demos by following the detailed installation and implementation steps below:

* **Install System Dependencies:**
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

* **Pull SU2 SIF Container:**
```bash
!singularity pull --arch amd64 library://junideallab/midbench/su2v7.3.1_conda3.9.12_gmsh:sha256.c6bf72230e360d23e2acdc8fc5cf9b8d26a3b709cc0c96feaaba42b60a611158
```

* **Download and Unzip "MIDBenchmarkSuite.zip":**
```bash
!unzip MIDBenchmarkSuite.zip
```

* **Execute the Python Script using SIF Container (recommended):**

```bash
# Simulation
%%bash
cd MIDBenchmarkSuite/
singularity exec --userns ../su2v7.3.1_conda3.9.12_gmsh_sha256.c6bf72230e360d23e2acdc8fc5cf9b8d26a3b709cc0c96feaaba42b60a611158.sif bash -c "python airfoil2d_simu.py"
```

```bash
# Optimization
%%bash
cd MIDBenchmarkSuite/
singularity exec --userns ../su2v7.3.1_conda3.9.12_gmsh_sha256.c6bf72230e360d23e2acdc8fc5cf9b8d26a3b709cc0c96feaaba42b60a611158.sif bash -c "python airfoil2d_opt.py"
```

* **Alternatively, You can Spawn a New Shell within SIF Container:**
```bash
singularity shell --userns su2v7.3.1_conda3.9.12_gmsh_sha256.c6bf72230e360d23e2acdc8fc5cf9b8d26a3b709cc0c96feaaba42b60a611158.sif
```

After entering SU2 SIF container, please run the 2D airfoil simulation and optimization demos using the following commands:

Go to the path of directory **"MIDBenchmarkSuite"** by entering command `cd /Path/to/MIDBenchmarkSuite`. Then, type `python`. In the Python environment, please enter the following commands to run demos:
```python
from midbench.envs import make
Env, Design, Condition = make("Airfoil2d-v0")

# Simulation
designs = Design('./midbench/envs/airfoil/airfoils_pred_cbegan_example.npy').meshgen()
conditions = Condition(**{'mach':0.7,'reynolds':7000000,'lift':0.350})
performances = ['lift', 'drag']

lift, drag = Env.simulate(conditions, designs, performances, './midbench/envs/airfoil/results_simu')

# Optimization
designs = Design('./midbench/envs/airfoil/airfoils_pred_cbegan_example.npy')
conditions = Condition(**{'mach':0.6,'reynolds':8000000,'lift':0.320})
objectives = ['drag', 'ld_ratio']

drag, ld_ratio = Env.optimize(conditions, designs, objectives, './midbench/envs/airfoil/results_opt')
```

__**NOTE**:__ The singuarity container also includes a 2D airfoil mesh generator `AirfoilGeometryConverter`. The generator will first convert the 2D coordinates of the airfoil curve points into mesh. The SU2 solver then takes the mesh for the follwoing CFD simulation and shape optimization. -->

## Docker Container

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.

Docker provides the ability to package and run an application in a loosely isolated environment called a container. The isolation and security allows you to run many containers simultaneously on a given host. Containers are lightweight and contain everything needed to run the application, so you do not need to rely on what is currently installed on the host. You can easily share containers while you work, and be sure that everyone you share with gets the same container that works in the same way.

Docker provides tooling and a platform to manage the lifecycle of your containers:

* Develop your application and its supporting components using containers.
* The container becomes the unit for distributing and testing your application.
* When you’re ready, deploy your application into your production environment, as a container or an orchestrated service. This works the same whether your production environment is a local data center, a cloud provider, or a hybrid of the two.

*For more information about Docker, please check the [official website](https://docs.docker.com/get-started/overview/).*

### Installing Docker

* **Linux Users:** Please use the following commands to install Docker:

```bash
$ sudo apt-get remove docker docker-engine docker.io && \
    apt-get update && \
    apt install docker.io
```

* **Windows and Mac Users:** Mac and Windows users should install the [Docker Toolbox](https://www.docker.com/products/docker-desktop/) (this is a simple one-click install). **_If running on Mac or Windows, make sure you run the following commands inside the Docker Quickstart Terminal._**

<!-- ### Usage

#### dolfin-adjoint with FEniCS Docker

##### To Run the MIDBench API Code:

* **Download and Unzip "MIDBenchmarkSuite.zip":**
```bash
!unzip MIDBenchmarkSuite.zip
```

* **Create a session that has access to the current folder from the host:**

* **Linux Users:**

```bash
$ cd /path/to/MIDBenchmarkSuite
$ sudo docker run -it -p 8887:8887 -v $(pwd):/home/fenics/shared quay.io/dolfinadjoint/pyadjoint
```

* **Windows and Mac Users:** If running on Mac or Windows, make sure you run the above commands inside the Docker Quickstart Terminal.


* **Install System Dependencies:**

```bash
$ sudo pip install dataclasses && \
    pip install typing_extensions && \
```
Reinstall `importlib-metadata`:

```bash
$ sudo pip uninstall importlib-metadata && \
    pip install importlib-metadata
```

* **Open jupyter notebook or jupyter lab:**
```bash
$ jupyter lab --no-browser --ip=0.0.0.0 --port=8887
```


* **Run MIDBench 2D Heat Exchanger Optimization Demo:** In the MIDBenchmarkSuite directory, there is an iPython notebook “midbench_api.ipynb”. Please open the notebook in jupyter lab or jupyter notebook. Please run the API demo code in the notebook cell by cell to check out the **_2D Heat Exchanger Optimization_** demo in your dolfin-adjoint FEniCS Docker container. The commands in the jupyter notebook are as follows:

```python
# Optimization
from midbench.envs import make
Env, Design, Condition = make("HeatExchanger2d-v0")

conditions = Condition(**{'volume':0.4,'length':0.5,'resolution':50})
designs = Design(**{'volume':0.4,'resolution':50}).output()
objectives = ['compliance']

compliance=Env.optimize(condition, designs, objectives)
``` -->

We use Docker container for our 2D heat exchanger optimization environment. Please find the usage of the dolfin-adjoint Docker in this [tutorial](tutorials/heat-fenics-docker.md).
