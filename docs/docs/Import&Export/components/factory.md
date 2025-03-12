# Factory

The Factory submodule is responsible for handling the conversion of various supported data formats from their raw text representations into the system’s common internal data model. This transformation ensures that all imported data adheres to a unified structure, making it compatible with the rest of the system.

Each factory within this submodule is designed to:

Define the expected structure of its respective raw data format.
Validate that the provided data conforms to these expectations before processing.
Transform the validated data into the standardized internal representation.
By enforcing these constraints, the factory ensures that all imported datasets are correctly structured and ready for further processing by other modules.

Additionally, each factory must be capable of incorporating separately stored setup data into an already created dataset. This allows for incremental data enrichment, where additional configuration or metadata can be merged with existing datasets to provide a complete and accurate representation.