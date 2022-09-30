import unittest
import scipy.optimize as opt

class TestLinearProgrammingTricks(unittest.TestCase):

    def test_simple_LP(self):
        # Problem described https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
        # Minimize objective function = -x0 + 4x1
        # Constraint 1) -3x0 + x1 <= 6   -> 2d: y <= 6 + 3x
        # Constraint 2) -x0 - 2x1 >= -4  -> 2d: y >= 2 - 0.5x
        # Constraint 3) x1 >= -3  -> 2d: y >= 3

        # scipy only supports <=, thus Constr. 2) 3) has to be reformulated
        # Constraint 2) -x0 - 2x1 >= -4 -> x0 + 2x1 <= 4
        # Constraint 3) x1 >= -3 -> -x1 <= 3

        objFunc = [-1, 4]

        ALessEq = [
                        [-3, 1], # Constraint 1) -3x0 + x1 <= 6
                        [1, 2],  # Constraint 2) x0 + 2x1 <= 4
                        [0, -1]  # Constraint 3)  -x1 <= 3
                  ]
        bLessEq = [6, 4, 3]

        # The value range x0 and x1 can take.
        # IMPORTANT!!!! Default range is x >= 0. That is why in this example we explicitly state no bounds.
        # Note: Constraint 3) could be specified via bound as well
        theBounds = [(None, None), (None, None)]

        res = opt.linprog(c=objFunc, A_ub=ALessEq, b_ub=bLessEq, bounds=theBounds)

        self.assertAlmostEqual(res.fun, -22.0)
        self.assertAlmostEqual(res.x[0], 10)
        self.assertAlmostEqual(res.x[1], -3)


    def test_min_LP(self):
        # A simple example of finding min in a 2 by 2 rectangle with (0/0) in the center
        # x0 >= -1  ->   -x0 <= 1,  x0 <= 1,  x1 <= 1,  x1 >= -1  ->  -x1 <= 1
        AUb = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        bUb = [1, 1, 1, 1]

        noBounds = [(None, None), (None, None)]

        # minimize x0 + x1 -> [-1,-1] = -2
        objFunc = [1, 1]

        res = opt.linprog(c=objFunc, A_ub=AUb, b_ub=bUb, bounds=noBounds)

        self.assertAlmostEqual(res.fun, -2)
        self.assertAlmostEqual(res.x[0], -1)
        self.assertAlmostEqual(res.x[1], -1)


    def test_max_LP(self):
        # Find max in previous problem
        # x0 >= -1  ->   -x0 <= 1,  x0 <= 1,  x1 <= 1,  x1 >= -1  ->  -x1 <= 1
        AUb = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        bUb = [1, 1, 1, 1]

        noBounds = [(None, None), (None, None)]

        # maximize x0 + x1 -> [1,1] = 2
        # linprog minimizes - to maximize, Objective function has to be inverted!!
        objFunc = [-1, -1]

        res = opt.linprog(c=objFunc, A_ub=AUb, b_ub=bUb, bounds=noBounds)

        self.assertAlmostEqual(-res.fun, 2) # as objective function was inverted, function value has to be inverted as well
        self.assertAlmostEqual(res.x[0], 1)
        self.assertAlmostEqual(res.x[1], 1)


if __name__ == '__main__':
    unittest.main()