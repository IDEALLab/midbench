### Usage

#### dolfin-adjoint with FEniCS Docker

##### Run the MIDBench API Code

* **Install midbench:**
```bash
pip install midbench
```

* **Create a session that has access to the current folder from the host:**

* **Linux Users:**

```bash
$ cd /path/to/midbench
$ sudo docker run -it -p 8887:8887 -v $(pwd):/home/fenics/shared quay.io/dolfinadjoint/pyadjoint
```

* **Windows and Mac Users:** If running on Mac or Windows, make sure you run the above commands inside the Docker Quickstart Terminal.


* **Open jupyter notebook or jupyter lab:**
```bash
$ jupyter lab --no-browser --ip=0.0.0.0 --port=8887
```


* **Run MIDBench 2D Heat Conduction Simualtion and Optimization Demos:** In the tutorials, there is an iPython notebook [**"example_usage.ipynb"**](../tutorials/example_usage.ipynb). Please open the notebook in jupyter lab or jupyter notebook. Please run the API demo code in the notebook cell by cell to check out the **_2D Heat Conduction Simulation and Optimization_** demo in your dolfin-adjoint FEniCS Docker container. The commands in the jupyter notebook are as follows:

**Simulation**
    
```python
# Simulation
from midbench.envs import make

# Direct to the Environment of 2D heat conduction
Env, Design, Condition = make("HeatConduction2d-v0")

# Boundary condition setup for simulation
conditions = Condition(**{'volume':0.4,'length':0.5,'resolution':50})

# Design initialization
designs = Design(**{'volume':0.4,'resolution':50}).output()

# Target performances (e.g., compliance)
performances = ['compliance']

# Execute simulation
compliance=Env.simulate(conditions, designs, performances)
```

**Optimization**

```python
# Optimization
# Boundary condition setup for optimization
conditions = Condition(**{'volume':0.4,'length':0.5,'resolution':50})

# Design initialization
designs = Design(**{'volume':0.4,'resolution':50}).output()

# Objectives (e.g., compliance)
objectives = ['compliance']

# Execute optimization
compliance=Env.optimize(conditions, designs, objectives)
```
