from abc import ABC, abstractmethod

class BaseKineticModel(ABC):
    @abstractmethod
    def calculate_rate(self, *args, **kwargs):
        pass