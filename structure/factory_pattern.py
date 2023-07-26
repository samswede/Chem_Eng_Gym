"""
The Factory Pattern allows you to create objects without specifying the exact class of object that will be created. 
This is done by creating objects by calling a factory method—either specified in an interface and implemented by child classes, or implemented in a base class and optionally overridden by derived classes—rather than by calling a constructor.

In your case, let's say you want to make it easy for others to add new types of Separator units. 
You can define a SeparatorFactory class that has a method create_separator. 
This method takes as input the type of separator to create, and returns an instance of the corresponding class.

Here's a simple example of how you can implement this:
"""


class SeparatorFactory:
    separator_classes = {
        'distillation': DistillationColumn,
        'extraction': ExtractionColumn,
        # Add more classes as they become available...
    }

    @classmethod
    def create_separator(cls, separator_type):
        SeparatorClass = cls.separator_classes.get(separator_type)
        if SeparatorClass is None:
            raise ValueError(f"Invalid separator type: {separator_type}")
        return SeparatorClass()

"""
Now, to add a new type of Separator, someone just needs to define the new class and add it to the separator_classes dictionary in SeparatorFactory.

For instance, if someone has defined a new CrystallisationColumn class, they can add it to the factory like this:
"""

class CrystallisationColumn(Separator):
    # Implementation of abstract methods goes here...

SeparatorFactory.separator_classes['crystallisation'] = CrystallisationColumn

"""
And then you can create an instance of this new class using the factory:
"""

separator = SeparatorFactory.create_separator('crystallisation')

"""
This factory pattern abstracts away the details of how separators are created, making it easier for others to extend your codebase with new types of separators.

Remember to document clearly what interface (i.e., what abstract methods) each new Separator class should implement. This will help others understand how to add new types of separators correctly.
"""