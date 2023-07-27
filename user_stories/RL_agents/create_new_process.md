# Create new process

## Description

As a graph neural network RL agent,
I want to reset the environment and receive an observation of the process as a graph object,
so that I can start building a new chemical process from the initially available chemical streams (represented as open nodes in the graph object).

## Business Value

Describe why this feature is important from a project or business perspective.

## Acceptance Criteria

- [ ] The system should reset to the specified initial state whenever the reset method is called, ensuring that all previous modifications are wiped clean and the state is exactly as initially defined.

- [ ] The initial state of the system should be properly defined by an external method or class, and the system should be able to retrieve this state information correctly.

- [ ] Upon resetting, the system should return an accurate representation of the initial state as a graph object, with all the relevant details properly encoded.

- [ ] The graph object representation should correctly identify open nodes as available chemical streams and appropriately reflect other state details.

- [ ] If there are any rules or conditions governing the initial state (e.g., certain streams should always/never be open), the system should adhere to these rules every time it resets.

- [ ] The reset operation should be efficient and not cause undue delay, particularly if the environment will need to be reset frequently during the RL agent's learning process. 


## Dependencies

List any dependencies this user story has on other parts of the system or other user stories.

## Notes

Any additional information or context about the user story.

## Progress

- [ ] Not started
- [ ] In progress
- [x] Completed

## Effort Estimate

Provide an estimate of the effort required to implement this user story, if possible.

## Tests

Describe the tests that need to be written for this user story, if any.

## Mockups or Diagrams

Include any visual representations of the feature, if applicable.

## Discussion

Link to a discussion thread or issue for this user story, if one exists.
