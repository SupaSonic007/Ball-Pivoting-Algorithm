class Edge:

    def __init__(self, p1, p2) -> None:

        self.p1 = p1
        self.p2 = p2
        self.edge = (p1, p2)
        
    def get_points(self) -> tuple:
        """
        Return the points for each edge
        :return: A tuple containing the two points connected as the edge
        """
        return (self.p1, self.p2)