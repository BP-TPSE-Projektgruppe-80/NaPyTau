# Current Issues & Limitations

### Current Issues
At the moment the program does not yet calculate the end result correctly. Since most of the functionality was at one point unit tested, the margin for error in how the calculations are implemented is very slim. This suggests that at least one necessary part of the calculation is probably missing. If we look at the old perl code from "napatau" this suspicion hardens. The lifetime itself is at least close to the order of magnitude of the expected result but the uncertainty is way off.

### Hypotheses
One of the most promising hypotheses is that while "napytau" first does the fit and calculates the coefficients on that basis and then optimizes $\tilde{t}^{hyp}$, "napatau" somehow fits and optimizes at the same time. Even though we previously did it similarly, we haven't quite figured out, how "napatau" handles this functionality exactly.\
Another idea is that the scipy library function for the $\chi^{2}$ minimization does not work as we expect it to. We weren't quite able to verify the behaviour of this function 100%, so there is room for a faulty implementation there.\
As a third and final starting point for possible bug fixes the fitting itself should be looked at. As we are again relying heavily on library functions it was difficult for us to verify correct behaviour.