import bpa

def main(radius:float = 0.003, file_location:str = 'stanford-bunny.obj', iterations:int = None):

    bpa = bpa.BallPivotingAlgorithm(radius=radius, file_location=file_location, iterations=iterations)
    bpa.run()


if __name__ == '__main__':
    # Change these values to your liking to change parameters of the algorithm
    # Radius -> The radius to search for the third point from a given edge
    # File Location -> The location of the point cloud to use (obj file) | If the obj file has faces, it will strip it down to vertices, as seen with the stanford bunny
    # Iterations -> The amount of faces to create | If no iterations are specified, the entire point cloud will be used and this can take a while

    # To run the code:
    # Change the values below to your liking, including using different objects, radius and iterations
    radius = 0.003
    file_location = 'stanford-bunny.obj'
    iterations = 50 
    main(radius=radius, file_location=file_location, iterations=iterations)