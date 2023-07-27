This is a planning section to keep track of ideas and progress

STANDARDISATION

    Docstring style
    - Google style:
        """
        Short description.

        Longer description if necessary.

        Args:
            arg1 (type): Description for arg1.
            arg2 (type): Description for arg2.

        Returns:
            type: Description of returned object.

        Raises:
            ErrorType: Description of conditions that cause this error.
        """

    - User stories
        - To keep development focused and keep track of scope and functionality I have included a user story template
        - This is to practice ATDD and to make it easier to opensource


IDEAS:
    - Make a dictionary that maps elements in node feature vector to corresponding properties
        - means that feature retrieval does not have to be hard coded, and is flexible in size and order
        - should me flexible to change as things develop
        - should be possible to make one automatically based on what process units, components and reactions are included

    Thermodynamics and Kinetic Data
    - Webscrape thermodynamic and kinetic data from NIST chemistry webbook
        - should be fun. A useful skill and fucking sick example.
        - should be able to automatically extract whatever info and store it in useful file formats to be loaded later.
        - could be reason to use a chemistry GPT model. 
    
    

    COSTING
    - Include costing as an instance method in the base_process_unit
    - include property decorators to create property attributes for process unit classes
        - e.g. volume from input dimensions of a reactor, 
        - if possible, make cost a property? Need to figure out what the drawbacks of that is.
    - can i upload a pdf of Rules of Thumb in Engineering and/or Towler & Sinnot and use GPT to extract capex and opex models? That would be insanely cool and useful. I also want to learn how to do that in general.


    DBPS and DAE solving
    - i need to automatically build the DAE formulations, and reduce to index 1. Quite a task, but if I can do that im god and would do very well in the exam.
    - can I add the models together from different process unit classes and try and solve the bigger DAE?
    - what does a recycle actually involve?
    - 

    Process File Formats
    - should be able to save as SFILE strings
    - need to think about efficient datastructures for replay buffers and saving experience
        - keeping track of the latest index was not a great solution
            - the 'info' part returned by the environment should be a dictionary that includes the latest added node or whatever.
    - what should the 'info' contain?

    Visualisation
    - It needs to look professional, but not dull like aspen.
    - 

    Process Analysis
    - Should be able to perform sensitivity analysis
    - Implement control regimes for batch reactors from DBPS
    - I want to be able to run simulations and plot results in graphs
    - Parameter estimation. Don't know what it is but need to know for exam, and what better way to learn than to do.


Test Driven Development


    
