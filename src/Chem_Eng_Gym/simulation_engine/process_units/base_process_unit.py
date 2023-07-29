from abc import ABC, abstractmethod
from typing import Dict, Any, final

class ProcessUnit(ABC):
    @abstractmethod
    def __init__(self, node_id: str, design_params: Dict[str, Any]):
        """
        Initialize a process unit.

        Args:
            id (str): Unique identifier for the process unit.
            operating_conditions (Dict[str, Any]): A dictionary containing the operating conditions.
        """
        self._node_id = node_id
        self._input_validation(design_params)
        self._set_attributes_from_params(design_params)

    @final 
    def _set_attributes_from_params(self, params):
        """
        Unpack design parameters from a dictionary to instance attributes.

        Args:
            design_params (Dict[str, Any]): A dictionary containing the design parameters.
        """
        for key, value in params.items():
            setattr(self, key, value)
    
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
    def modify_params(self, params: Dict[str, Any]):
        """
        Set parameters of the process unit.

        Args:
            params (Dict[str, Any]): A dictionary containing the new operating conditions.
        """
        self._set_attributes_from_params(params)
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

    @property
    @abstractmethod
    def CAPEX(self) -> float:
        """
        Calculate capital expenditure.

        Returns:
            float: The capital expenditure in thousands USD.
        """
        pass
    
    @property
    @abstractmethod
    def OPEX(self) -> float:
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



class ConcreteProcessUnit(ProcessUnit):
    def __init__(self, id, design_params):
        super().__init__(id, design_params)
    
    def _input_validation(self, inputs):
        pass  # Do something to validate the inputs
    
    def _output_validation(self, outputs):
        pass  # Do something to validate the outputs

    @property
    def params(self):
        return {"param1": self.param1, "param2": self.param2}
    
    @property
    def CAPEX(self):
        pass  # Calculate capital expenditure
    
    @property
    def OPEX(self):
        pass  # Calculate operating expenditure

    def run(self, time):
        pass  # Do something to simulate running the process unit