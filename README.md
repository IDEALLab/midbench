# The Maryland Inverse Design Benchmark Suite

The **Maryland Inverse Design (MID) Benchmark Suite** is a set of libraries for running computational experiments on Machine Learning models for *Inverse Design* across a wide variety of domains and metrics. Its goal is to facilitate reproducible research in this area and help broaden the applicability of various ID algorithms across many applications by making it easy to run otherwise complex engineering design simulations using a common interface specification. It also provides a set of metrics that are relevant to different aspects of ID performance commonly used in research papers. In this way, if a researcher designs a new kind of ID algorithm, they will be able to use this repository to run a large set of tests across common examples of increasing range and complexity.

You can read more about the library at [its documentation website](https://ideal.umd.edu/midbench).

# Contents
Specifically, this repository contains the following:
- A set of Engineering Design Environments (see `env` folder) that provides containerized simulation environments in which researchers can run their ID algorithm across a variety of multi-physics simulation and optimization platforms. These will implement a range of applications from Aerodynamic Optimization to Power Electronics to Medical Devices to Photonics to Heat Transfer, among others as we develop and deploy those environments. Currently available environments are in the `env` folder.
- Code that links to/downloads a set of pre-built datasets generated from the above environments that you can use for training your Inverse Design algorithm. These are helpful if you just wish to train an Inverse Design model directly from an existing dataset without needing to run any simulation or design optimization code (which is typical time consuming). While you will not be able to calculate certain ID metrics without using the containerized environments mentioned above, there are certain metrics that you can compute using only the dataset, making this is a useful and lower-cost starting point for many researchers.
- A set of Python files for computing a common set of ID performance metrics (`metrics.py`). These include simpler metrics like those that measure closeness of distribution to test data, along with more complex metrics that require access to a design environment or simulator, such as Instantaneous Optimality Gap and Cumulative Optimality Gap which is useful for judging how well ID warm starts existing optimization routines.


# Installation

```bash
pip install midbench
```

However, to use specific design environments will require installing either Singularity or Docker and using our pre-build images defined within that environment's singularity container file (*i.e.*, the `.sif` file). These are described further in the documentation pages.

# Usage

Using the benchmark suite has essentially three steps, some of which may be optional depending on how you prefer to use the library:
1. (Optional) Load an existing ID dataset and train an ID model on that dataset. Alternatively, you can load a pre-trained model.
2. Specify a set of input conditions over which you wish to generate predictions/designs and then generate sample designs for those inputs. These typically include requirements for the design that the ID outputs should satisfy.
3. Analyze how well the generated designs do us with respect to various ID metrics, such as MMD, Instantaneous Optimality Gap and Cumulative Optimality Gap.

An example usage case is provided in the `tutorials\` folder.
