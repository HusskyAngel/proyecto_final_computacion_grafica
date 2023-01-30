from drone_vision.point import point


class PointEntering:

    def __init__(self, P: point, intersection: bool, entering: bool = False, incomplete: bool = False, is_single: bool = False):
        """
        Defines wheter or not a point 'P' is a intersection point between a pair of segments, furthermore, in case its
        a intersection the direction of the vector is defined by 'entering'.
        """

        self.P = P
        self.intersection = intersection
        self.entering = entering
        self.incomplete = incomplete
        self.is_single = is_single

    def print(self):
        print(
            f"{self.P.to_string()} intersection: {self.intersection}; entering: {self.entering}; incomplete: {self.incomplete}; single: {self.is_single}")

    def equal(self, Q: 'PointEntering') -> bool:
        """
        Returns wheter or not this PointEntering is equal to another one.
        """

        if(self.P.equal(Q.P) and (self.entering == Q.entering) and (self.intersection == self.intersection)):
            return True
        return False
