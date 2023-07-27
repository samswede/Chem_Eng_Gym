from abc import ABC, abstractmethod
from typing import NoReturn, List, Dict

class ProcessUnit(ABC):
    @abstractmethod
    def __input_validation__(self, *args, **kwargs) -> None:
        """
        
        """
        pass

    @abstractmethod
    def __output_validation__(self, *args, **kwargs) -> None:
        """
        
        """
        pass

    @abstractmethod
    def CAPEX(self, *args, **kwargs) -> float:
        """
        
        """
        pass

