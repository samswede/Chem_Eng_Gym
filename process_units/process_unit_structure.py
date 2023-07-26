from abc import ABC, abstractmethod

class ProcessUnit(ABC):
    @abstractmethod
    def separate(self, mixture):
        pass

class Separator(ProcessUnit, ABC):
    @abstractmethod
    def separate(self, mixture):
        pass

    @abstractmethod
    def shut_down(self):
        pass

class DistillationColumn(Separator, ABC):
    @abstractmethod
    def control_temperature(self, temperature):
        pass

class Extractor(Separator, ABC):
    @abstractmethod
    def control_pressure(self, pressure):
        pass
