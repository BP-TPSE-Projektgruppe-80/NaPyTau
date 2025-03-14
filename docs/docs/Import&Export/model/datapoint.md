# Datapoint

The `Datapoint` class represents a single measurement taken during the course of an experiment. Each datapoint is uniquely identified by the distance it was measured at. The datapoint should always contain the following information:

| **Name**             |**Description** | **Type of data**   |
|--------------|--------------|-----------------|
| `distance`|The distance this datapoint was measured at| [floating point number with error](error_value_pair.md)       |
| `calibration`|The calibration of this datapoint| [floating point number with error](error_value_pair.md)       |
| `shifted_intensity`|The shifted intensity measured at this datapoint| [floating point number with error](error_value_pair.md)       |
| `unshifted_intensity`|The unshifted intensity measured at this datapoint| [floating point number with error](error_value_pair.md)       |
| `active`|Indicates if this datapoint should be considered during calculation| boolean         |


It may also contain the following information, depending on the input data and the state of calculation:

| **Name**             |**Description**| **Type of data**   |
|-----------------|-----------|-----------------|
| `feeding_shifted_intensity`|The feeding shifted intensity measured at this datapoint| [floating point number with error](error_value_pair.md) |  [floating point number with error](error_value_pair.md)       |
| `feeding_unshifted_intensity`|The feeding unshifted intensity measured at this datapoint| [floating point number with error](error_value_pair.md) |  [floating point number with error](error_value_pair.md)|
| `tau`|The tau value calculated for this datapoint|  [floating point number with error](error_value_pair.md)       |