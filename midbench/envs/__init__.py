from midbench.envs.registration import load_env_plugins as _load_env_plugins
from midbench.envs.registration import make, register, spec

# Hook to load plugins from entry points
_load_env_plugins()


# Classic
# ----------------------------------------

register(
    id="Airfoil2d-v0",
    entry_point="midbench.envs.airfoil.airfoil2d:Airfoil2dEnv",
    designs = "midbench.envs.airfoil.airfoil2d:Airfoil2dDesign",
    conditions = "midbench.envs.airfoil.airfoil2d:Airfoil2dCondition",
)

register(
    id="HeatConduction2d-v0",
    entry_point="midbench.envs.heatconduction.heatconduction2d:Heatconduction2dEnv",
    designs = "midbench.envs.heatconduction.heatconduction2d:Heatconduction2dDesign",
    conditions = "midbench.envs.heatconduction.heatconduction2d:Heatconduction2dCondition",
)
