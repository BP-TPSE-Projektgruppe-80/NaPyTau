# General

The Core-module handles the mathematical logic and implementation of the underlying physical formulas. It is structured into several different collections of (helper-) methods. Each of these files either handles an abstraction layer of the physical calculation or functionality for an explicit mathematical construct, like polynomial functions. The exact responsibility for each of them can be found in [`file_responsibilities`](file_responsibilities.md).\
\
Overall, the goal is to calculate the lifetime $\tau_{final}$ via the weighted mean of $\tau_{i}$ and $\Delta\tau_{i}$. For a more in depth explanation of the physical background, please look at the [`napatau manual`](ressources/napatau_manual.pdf).