# Ball Pivoting Algorithm

## How does it work?
An algorithm for reconstructing surfaces of a mesh.

* The algorithm works by checking a radius around a point to find another point and link them to create an edge.
* The algorithm then finds a third point from that edge in a certain radius to create a face.
* The algorithm then continues to use a new edge formed from a face to find a third point and create a new face.

* It works from a seed triangle and continues to create faces and edges until there are no more points left.

**To run** -> initialise the class with a point cloud and radius, then call run() to run the algorithm. Other options are available to modify the user experience.

## How to use the implementation
The implementation can be demonstrated by running bpa-demo.py. This will run the algorithm on a point cloud and display the results and allow the parameters to be modified to work with different a different radius, point cloud and number of iterations.

## Notes
* All of the code is commented such that you can follow where it's going and why it does what it does.
* The algorithm is slow as it has been optimised from previous versions, but is not fully optimised, and I am planning to optimise it further.