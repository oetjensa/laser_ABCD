# laser_ABCD
Laser Beam propagation with ABCD matrices employing beam parameter and M^2


Beam Propagation is the main programm and this is the only one that needs to be run


ABCD_utensils contains all functions to compute the beam radius.

The Input files Input_param.txt and Lenses_param.txt are the ones that need to be changed to customize the beam and the placement of the optics.

Input_param.txt contains the measured beam profile parameter like M², w_0, rad1 (initial beam radius can be approximated to ~w_0), convergence (this needs to be in radians),...
For the lasers tested during this study the parameters are summarized below (note that the divergence needs to converted to radians):


<img width="225" alt="image" src="https://github.com/oetjensa/laser_ABCD/assets/54310884/cb8bf6d7-2a09-44ce-8e99-35854c95764b">



To include lenses in the beam path, have a look at the Lenses_param.txt file. Here, you can add lenses according to position and focal length.
All distances are in mm.

Examples for the current (as of 2022) setup (grey squares indicate position of the boxes along the path):

<img width="496" alt="image" src="https://github.com/oetjensa/laser_ABCD/assets/54310884/9eef7b52-e894-4128-9d34-c11b57080979">





