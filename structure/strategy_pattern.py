"""
In object-oriented programming, an interface is a contract for a class that specifies what methods the class should implement. It's a way of ensuring that a class adheres to a certain contract and thus ensures that an object can perform a certain set of actions.

In some languages like Java or C#, interfaces are a key language feature. In Python, however, there's no explicit "interface" construct. Instead, the concept of an interface is often represented via base classes or abstract base classes (ABCs), with methods that are intended to be overridden by subclasses.

In our example, SeparationStrategy is the "base strategy interface". It's a class that defines a common interface for all its subclasses, here represented by the separate method. Subclasses such as DistillationStrategy, ExtractionStrategy, CrystallisationStrategy each provide their own implementation of the separate method.
"""

from abc import ABC, abstractmethod

class SeparationStrategy(ABC):
    @abstractmethod
    def separate(self, mixture):
        pass

class DistillationStrategy(SeparationStrategy):
    def separate(self, mixture):
        return "Separated by distillation"

"""
In the example above, SeparationStrategy is defined as an abstract base class (with the ABC metaclass and the abstractmethod decorator), 
which means it can't be instantiated on its own and exists purely to be subclassed.
"""
