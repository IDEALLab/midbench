MID Benchmark Suite -- Metrics
-----------------------------

The metrics are functions for evaluating the performance of the inverse design models and the quality of the dataset. Because of the difference between their roles and their underlying mechanisms, they are divided into three different categories in MID.

# Internal Distribution Metrics

This set of metrics could evaluate the performance of inverse design model purely using the existing dataset by relying on statistics, without running the MIDBench environments to do time-consuming simulation or optimization.

```python
def midbench.metrics.maximum_mean_discrepancy(gen_func: Function, X_test: Ndarray)
```
For evaluating the maximum mean discrepancy between the inverse design generator distribution and the dataset empirical distribution.

- Parameters
    - gen_func (Function): The generator function which produces certain amount of samples when called.
    - X_test (Ndarray): The dataset in the form of numpy array.
- Returns
    - The score.


```python
def midbench.metrics.consistency(gen_func, latent_dim, bounds)
```
For evaluating the latent space consistency of the generator function inside the given latent space.

- Parameters
    - gen_func (Function): The generator function which produces certain amount of samples when called.
    - latent_dim (int): The dataset in the form of numpy array.
    - bounds (list)
- Returns
    - The score.


```python
def midbench.metrics.rsmth(gen_func, X_test, N=2000)
```
For evaluating the generator function's relative variance of difference against the dataset.

- Parameters
    - gen_func (Function): The generator function which produces certain amount of samples when called.
    - X_test (Ndarray): The dataset in the form of numpy array.
    - N (int): The number of samples to be generated for the evaluation.
- Returns
    - The score.


```python
def midbench.metrics.rdiv(gen_func, X_train, d=None, k=None, bounds=None)
```
For evaluating the generator function's relative diversity against the dataset.

- Parameters
    - gen_func (Function): The generator function which produces certain amount of samples when called.
    - X_test (Ndarray): The dataset in the form of numpy array.
- Returns
    - The score.


```python
def midbench.metrics.mean_log_likelihood(gen_func, X_test, N=2000)
```
This metric first fits the generator's samples with a kernel density estimation function, then take the dataset's log likelihood on this KDE model as the score.

- Parameters
    - gen_func (Function): The generator function which produces certain amount of samples when called.
    - X_test (Ndarray): The dataset in the form of numpy array.
    - N (int): The number of samples to be generated for the evaluation.
- Returns
    - The score.

# External Performance Metrics

This set of metrics directly evaluates the quality of inverse design model with the MIDBench environment by computing quantities like the Cumulative Optimality Gap and the Instantaneous Optimality Gap. These are currently not yet implemented in the public library but we will update here when these are available.




# Dataset Metrics

This set of metrics for evaluating the quality of the dataset or generated samples, such as the diversity of it. Can be used for `Database` curation.

# Utils
```python
def confidence_interval(metric: Function) → Function
```
A decorator function for turning any non-deterministic metric into one evaluating the confidence interval instead.

- Parameters
    - metric (`Function`): A metric function with certain input.
- Returns
    - ci_metric (`Function`): A function that accepts an additional `ci_n` as the first positional argument for the number of sampling batches. The subsequent input arguments are the same as `metric`'s.
