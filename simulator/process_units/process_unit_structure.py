from abc import ABC, abstractmethod
from typing import Dict, Any

class ProcessUnit(ABC):
    @abstractmethod
    def __init__(self, id: str, design_params: Dict[str, Any]):
        """
        Initialize a process unit.

        Args:
            id (str): Unique identifier for the process unit.
            operating_conditions (Dict[str, Any]): A dictionary containing the operating conditions.
        """
        self.id = id
        self.design_params = design_params
    
    @abstractmethod
    def input_validation(self, inputs: Dict[str, Any]):
        """
        Validate the input to the process unit.

        Args:
            inputs (Dict[str, Any]): A dictionary containing the inputs to the process unit.
        """
        pass

    @abstractmethod
    def output_validation(self, outputs: Dict[str, Any]):
        """
        Validate the output from the process unit.

        Args:
            outputs (Dict[str, Any]): A dictionary containing the outputs from the process unit.
        """
        pass
    
    @abstractmethod
    def set_operating_conditions(self, conditions: Dict[str, Any]):
        """
        Set operating conditions of the process unit.

        Args:
            conditions (Dict[str, Any]): A dictionary containing the new operating conditions.
        """
        pass

    @abstractmethod
    def get_operating_conditions(self) -> Dict[str, Any]:
        """
        Get operating conditions of the process unit.

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
