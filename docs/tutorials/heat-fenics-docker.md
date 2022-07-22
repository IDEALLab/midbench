### Usage

#### dolfin-adjoint with FEniCS Docker

##### To Run the MIDBench API Code:

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


* **Run MIDBench 2D Heat Conduction Optimization Demo:** In the midbench directory, there is an iPython notebook "example_usage.ipynb". Please open the notebook in jupyter lab or jupyter notebook. Please run the API demo code in the notebook cell by cell to check out the **_2D Heat Conduction Optimization_** demo in your dolfin-adjoint FEniCS Docker container. The commands in the jupyter notebook are as follows:

```python
# Optimization
from midbench.envs import make
Env, Design, Condition = make("HeatConduction2d-v0")

conditions = Condition(**{'volume':0.4,'length':0.5,'resolution':50})
designs = Design(**{'volume':0.4,'resolution':50}).output()
objectives = ['compliance']

compliance=Env.optimize(conditions, designs, objectives)
```
