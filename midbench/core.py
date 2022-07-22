"""Core API for Environment."""
class Env:
    r"""The main MIDbench class.

    The main API methods that users of this class need to know are:

    - :meth:`simulate` - Implement simulation of environments.
    - :meth:`optimization` - Implement optimization of environments.
    
    """
    
    def simulate(self, designs, conditions, performances, results_dir_simu):
        raise NotImplementedError
        
    def optimize(self, designs, conditions, objectives, results_dir_opt):
        raise NotImplementedError
        
    @property
    def unwrapped(self) -> "Env":
        """Returns the base non-wrapped environment.
        Returns:
            Env: The base non-wrapped midbench.Env instance
        """
        return self 


class Design:
        
    @property
    def unwrapped(self) -> "Design":
        """Returns the base non-wrapped environment.
        Returns:
            Design: The base non-wrapped midbench.Design instance
        """
        return self 
    

class Condition(object):
        
    @property
    def unwrapped(self) -> "Condition":
        """Returns the base non-wrapped environment.
        Returns:
            Condition: The base non-wrapped midbench.Condition instance
        """
        return self 