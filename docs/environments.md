MID Benchmark Suite -- Environments
---------------------
The environments in MIDBench serve as the *interface* between Python and the simulation & optimization (S&O) programs---be it a script running locally, or one running inside a Docker or Singularity container. Specifically, it should either perform simulation by taking the design variables and boundary conditions as input then yielding the performance metrics as requested, or perform optimization over the initial design variables by optimizing the performance metrics under the given boundary conditions. Since each S&O program is not necessarily written in Python, the design variables and boundary conditions need to be first transformed into a format readable to the program, and the resulting output of the program needs to be transformed back into Python variables. 

In short, the MIDBench Environments are for generating the $(\bm{d}, \bm{b}, \bm{p})$---design, condition, performance---tuples for inverse design learning.

# Basic Components
The MIDBench environments should complete their jobs with the following environment-specific Python classes---`Env`, `Design`, `Condition`, `Performance`---as components for easy management:

## Env
```python
class midbench.core.Env(specs: EnvSpec = None)
```
    
The parent class of the simulation/optimization environment, which serves as the interface between Python and the simulation/optimization program. In other words, it takes Python variables as inputs and outputs the results also in form of Python variables, while keeping the processing and running of the program under the hood. 

- Parameters:
    - specs (`EnvSpec`): The specifications for the initialization of the S&O program.

- Methods
    
    As its role suggests, `Env` should have either a "simulate" method, or a "optimize" method. Both are for generating the $(\bm{d}, \bm{b}, \bm{p})$ tuples for inverse design learning, but with different motivations. 

    - simulate(designs: Design, conditions: Condition, performances: Performance, specs: SimSpec) → DataEntry:
        
        *Motivation: Design & Condition → Performance*
        - Parameters
            - designs (`Design`) - An $N\times D$ tensor-liked object defining the design space and storing the set of design variables $\bm{d}$.
            - conditions (`Condition`) - An $N\times B$ or $1\times B$ tensor-liked object storing the set of boundary conditions $\bm{b}$. If the first dimension is of size $1$, it will be propagated to all $N$ designs.
            - performances (`Performance`) - An $N\times P$ or $1\times P$ tensor-liked object storing the set of performances. It should be empty, with only the ID of the performances to be evaluated specified. If the first dimension is of size $1$, it will be propagated to all $N$ designs.
            - specs (`SimSpec`) - The specifications for running the simulation. Should be a `Dict`-like object.
        - Returns
            - The `DataEntry` data logger storing the $(\bm{d}, \bm{b}, \bm{p})$ tuples, with the `SimSpec` instance included for simulation replicability.
    - optimize(designs: Design, conditions: Condition, performances: Performance, specs: OptSpec) → DataEntry:
  
        *Motivation: Performance & Condition → Design*
        - Parameters
            - designs (`Design`) - An $N\times D$ tensor-liked object defining the design space and storing the set of *initial* design variables $\bm{d}$.
            - conditions (`Condition`) - An $N\times B$ or $1\times B$ tensor-liked object storing the set of boundary conditions $\bm{b}$ under which the optimization is performed. If the first dimension is of size $1$, it will be propagated to all $N$ designs.
            - performances (`Performance`) - An $N\times P$ or $1\times P$ tensor-liked object storing the set of performances to be optimized. It should be empty, with only the ID of the performances to be evaluated specified. If the first dimension is of size $1$, it will be propagated to all $N$ designs.
            - specs (`OptSpec`): The specifications for running the optimization, including things like the number of iterations, tolerances, etc. Should be a `Dict`-like object.
        - Returns
            - The `DataEntry` data entry storing the $(\bm{d}^\star, \bm{b}, \bm{p}^\star)$ tuples for either the optimization final result or the entire optimization history, with the `OptSpec` instance included for optimization replicability.

- Attributes:
    - dbp (tuple): The tuple (Design, Condition, Performance) of classes dedicated to handling the data for this specific environment.

## Design

```python
class midbench.core.Design(data: array_like, specs: DesignSpec=None, dtype=None, **kwargs)
```

An ndarray subclass serving as the container and manager for the design variables $\bm{d}$ of a list of designs. We can develop environment-specific Designs by inheriting and overloading. 

- Arguments
    - data (`array_like`): The tensor of design variables or the directory of the design files.
    - specs (`DesignSpec`): A `dict`-like object containing the specifications of the current design variable space. For instance, the specifications of the control point spaces of Bezier curve or B-spline.
    - dtype (`data-type, optional`): dtype for ndarray.
    - kwargs: Optional keyword arguments used as key-value pairs to update the specifications in the `specs` attribute. Cannot be any key other than the existing keys in `specs`.
  
- Methods
    - convert(specs: DesignSpec) → Design:
        
        Convert the current design variables into a different design variable space.

        - Parameters
            - specs (`DesignSpec`): The specification of the target design variable space.
        - Returns
            - A new `Design` in the target design space.

    - output(specs: MeshSpec) → Mesh:
        
        Generate mesh file readable to the S&O program.
        
        - Parameters
            - specs (`MeshSpec`): The specifications of the mesh. 
        - Returns
            - A mesh file (or its directory) that is readable to the environment.

- Attributes
    - specs (`DesignSpec`): The specifications of the current design space. 
    - Env (`Type`): The `Env` class that this `Design` class is built for.
    - Spec(`Type`): The `DesignSpec` class dedicated to this `Design` class. A mandatory attribute in the definition of `Design` subclass.
    
## Condition

```python
class midbench.core.Condition(data: array_like, specs: ConditionSpec=None, dtype=None, **kwargs)
```

The container and manager for boundary conditions. This is the parent class of every other env-specific Condition. 

- Arguments
    - data (`array_like`): The values of the boundary conditions.
    - specs (`ConditionSpec`): An `OrderedDict`-like object containing the names and units of the values, and also specifying their order. Can be ignored if we only use the default metric system. 
    - dtype (`data-type, optional`): dtype for ndarray.
    - kwargs: Optional keyword arguments used as key-value pairs to update the specifications in the `specs` attribute. Cannot be any key other than the existing keys in `specs`.
     
- Methods
    - output():
        
        Transform it to the format that the S&O program can read. 
        
        - Returns
          - The file or string that the S&O program can read.
    
    - convert(specs: ConditionSpec) → Condition:
        - Parameters
            - specs (`ConditionSpec`): The metric system to be converted to. 
        - Returns
            - New `Condition` instance with the given units.
           
    - \_\_repr\_\_() → str:
      - The string representation of the conditions for `print()`, should be one showing both the values and the corresponding units.
       
- Attributes
    - specs (`ConditionSpec`): The specifications of the current design space. 
    - Env (`Type`): The `Env` class that this `Condition` class is built for.
    - Spec(`Type`): The `ConditionSpec` class dedicated to this `Condition` class. A mandatory attribute in the definition of `Condition` subclass.
    - names (`tuple`): The names of the boundary conditions, which determines the order of the values.
    - units (`tuple`): The units of the boundary conditions.

## Performance

```python
class midbench.core.Performance(data: array_like, specs: PerformanceSpec=None, dtype=None, **kwargs)
``` 
The container and manager for performances. This is the parent class of every other env-specific Performance. 

It may do two jobs:

1. Storing the performance data produced by `simulate()` and `optimize()`. Empty values will be filled with `NaN`.
2. Indicating the performances to be simulated or optimized (may need to add an additional attribute to `PerformanceSpec`).

- Arguments
    - data (`array_like`): The values of the performances.
    - specs (`PerformanceSpec`): The units of the values. Can be ignored if we only use the default metric system.
    - dtype (`data-type, optional`): dtype for ndarray.
    - kwargs: Optional keyword arguments used as key-value pairs to update the specifications in the `specs` attribute. Cannot be any key other than the existing keys in `specs`.
    
- Methods
    - output(): 

        Transform it to the format that the S&O program can read. 
        
        - Returns
          - The file or string that the S&O program can read.

    - convert(specs: PerformanceSpec) → Performance:
        - Parameters
            - specs (`PerformanceSpec`): The units to be converted to. 
        - Returns
            - New `Performance` instance with the given units.
    
    - \_\_repr\_\_() → str:
    
        The string representation of the performances for `print()`, should be one showing both the values and the corresponding units.
    
- Attributes
    - specs (`PerformanceSpec`): The specifications of the current design space. 
    - Env (`Type`): The `Env` class that this `Performance` class is built for.
    - Spec(`Type`): The `PerformanceSpec` class dedicated to this `Performance` class. A mandatory attribute in the definition of `Performance` subclass.
    - names (`tuple`): The names of the performances, which determines the order of the values.
    - units (`tuple`): The units of the performances.

# Specifications
There might be a tremendous amount of specifications related to each environment components above. To efficiently manage them, enhance the tracability of simulations and optimizations, and improve the compatibility between different subclasses of the environment components, we use the instances of `_Spec` and `_OrderedSpec` to record, process and migrate all these specifications. 

`_Spec` and `_OrderedSpec` are `dict`-like and `OrderedDict`-like objects, respectively. Their main difference to dictionaries---which is also the reason for the introduction of them---is that they have default keys and values, and their keys are immutable, which makes good sense for specifications. In addition, the specifications is also the defining characteristic of each subclass of the environment components, so it is a necessary attribute of each subclass and it is mandatory to specify it in the definition of each subclass. 

## _Spec
This class is for storing the specifications whose order does not matter. For instance, the `DesignSpec` of `Design` stores the specifications about the design variable space like the number of control points of the Bezier curve, and we do not care about their order. 

### Subclasses
`DesignSpec`, `SimSpec`, `OptSpec`, `EnvSpec`, `MeshSpec`...

## _OrderedSpec
This is a subclass of `_Spec` for storing specifications whose order matters. For instance, for `Condition` and `Performance`, if we want to specify the unit of each dimension of these arrays, we had better also keep this info in a fixed order to remind us of the meaning of each dimension.

### Subclasses
`ConditionSpec`, `PerformanceSpec`...

## Compatibility
There are two ways to create a new `_Spec` instance, one is to specify explicity what the value of each key is, another is to take an existing `_Spec` instance as input and copy its values. The latter comes with a problem that two specifications might not have the same set of keys, so that a brainless copy between them is confusing for the fact that the keys of `_Spec` are fixed. However, this is to our benefit, as every `Design`, `Condition` and `Performance` subclass has a dedicated immutable `_Spec` which is part of its identity, and we can use this to determine which two subclasses are compatible. 