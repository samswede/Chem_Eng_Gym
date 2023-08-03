from abc import ABC, abstractmethod
from typing import Dict, Any, final, List

class BaseProcessUnit(ABC):
    @abstractmethod
    def __init__(self, node_id: str, feed_in: Any, params: Dict[str, Any]):
        """
        Initialize a process unit.

        Args:
            id (str): Unique identifier for the process unit.
            operating_conditions (Dict[str, Any]): A dictionary containing the operating conditions.
        """
        # self._param_bounds = {}

        self._node_id = node_id
        self._input_validation(params)
        self._set_attributes_from_params(params)

    @final 
    def _set_attributes_from_params(self, params):
        """
        Unpack design parameters from a dictionary to instance attributes.

        Args:
            params (Dict[str, Any]): A dictionary containing the design parameters.
        """
        for key, value in params.items():
            setattr(self, key, value)
    
    @final
    @property
    def node_id(self):
        return self._node_id
    
    @abstractmethod
    def _input_validation(self, inputs: Dict[str, Any]):
        """
        Validate the input to the process unit.

        Args:
            inputs (Dict[str, Any]): A dictionary containing the inputs to the process unit.
        """
        pass

    @abstractmethod
    def _output_validation(self, outputs: Dict[str, Any]):
        """
        Validate the output from the process unit.

        Args:
            outputs (Dict[str, Any]): A dictionary containing the outputs from the process unit.
        """
        pass
    
    @abstractmethod
    def modify_params(self, new_params: Dict[str, Any]):
        """
        Set parameters of the process unit.

        Args:
            params (Dict[str, Any]): A dictionary containing the new parameters.
        """
        self._set_attributes_from_params(new_params)
        pass
    
    @property
    @abstractmethod
    def params(self) -> Dict[str, Any]:
        """
        Get parameters of the process unit.

        Returns:
            Dict[str, Any]: A dictionary containing the operating conditions.
        """
        pass

    @final
    @property
    def param_bounds(self) -> Dict[str, set]:
        """
        Get bounds of parameters of the process unit.

        Returns:
            Dict[str, Any]: A dictionary containing the the lower and upper bounds.
        """
        return self._param_bounds

    @property
    @abstractmethod
    def capex(self) -> float:
        """
        Calculate capital expenditure.

        Returns:
            float: The capital expenditure in thousands USD.
        """
        pass
    
    @property
    @abstractmethod
    def opex(self) -> float:
        """
        Calculate operating expenditure.

        Returns:
            float: The operating expenditure in thousands USD.
        """
        pass

    @abstractmethod
    def run(self, time: float) -> Dict[str, Any]:
        """
        Run the process unit for a certain time.

        Args:
            time (float): The amount of time to run the process unit.

        Returns:
            Dict[str, Any]: A dictionary containing the result of running the process unit.
        """
        pass



class ConcreteProcessUnit(BaseProcessUnit):
    def __init__(self, node_id, feed_in, params):

        self._param_bounds = {'param1': (0, 5),
                              'param2': (0, 5),
                              'param3': (0, 5),
                              'param4': (0, 5)
                              }
        
        self._node_id = node_id
        self._input_validation(params)
        self._set_attributes_from_params(params)
        #super().__init__(node_id, params)

    @property
    def node_id(self):
        return self._node_id

    def _input_validation(self, inputs):
        for param, value in inputs.items():
            if param in self._param_bounds:
                lower, upper = self._param_bounds[param]
                if not lower <= value <= upper:
                    raise ValueError(f"{param} value {value} is out of bounds [{lower}, {upper}]")
            else:
                raise ValueError(f"Parameter {param} is not recognized and does not have defined bounds.")

        
    def _output_validation(self, outputs):
        pass  # Do something to validate the outputs

    def modify_params(self, new_params: Dict[str, Any]) -> None:
        """
        Set parameters of the process unit.

        Args:
            params (Dict[str, Any]): A dictionary containing the new parameters.
        """
        self._set_attributes_from_params(new_params)
        pass

    @property
    def params(self):
        return {"param1": self.param1, "param2": self.param2}
    
    @property
    def capex(self) -> float:
        return self.param1 * self.param2 **2
    
    @property
    def opex(self) -> float:
        return self.param1 *365.0

    def run(self, time):
        pass  # Do something to simulate running the process unit
