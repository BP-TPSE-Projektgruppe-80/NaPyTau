# Dataset

The `Dataset` class represents the top-level container for experimental data within the system. It encapsulates all relevant information associated with an experiment. This includes the following:

## Relative velocity

The [relative velocity](relative_velocity.md) the particles were moving at during the experiment.

## Datapoints

All [datapoints](datapoint_collection.md) collected during the experiment.

## Tau factor

The tau factor used during the calculation process. This may be set using the GUI or read from setup data.

## Weighted Mean Tau

The result of the calculation process. This is the weighted mean tau value for the experiment.

## Sampling Points

A list of sampling points used to split up the datapoints into smaller groups for calculation. A polynomial fit is performed on each group to calculate the tau value.

## Polynomial Count

The amount of polynomials used to fit the datapoints. This can be set using the GUI or read from setup data. It determines the number of sampling points used in the calculation process.

## Polynomials

A list of polynomials fit to the datapoints. These are used to calculate the tau value the experiment.