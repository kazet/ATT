# pylint: disable=R0904,R0921,C0111

import random
from att.test import TestCase
from att.classifier.linear_regression import LinearRegression

class LinearRegressionTestCase(TestCase):
  def testNoError(self):
    # y = alpha + beta * x
    alpha, beta = LinearRegression([(0, 1), (1, 3), (2, 5)])
    self.assertAlmostEqual(alpha, 1)
    self.assertAlmostEqual(beta, 2)

  def testWithError(self):
    points = [(i + random.uniform(-0.01, 0.01),
               3 * i + 7 + random.uniform(-0.01, 0.01))
              for i in range(0, 10000)]
    alpha, beta = LinearRegression(points)
    self.assertAlmostEqual(alpha, 7, places=2)
    self.assertAlmostEqual(beta, 3, places=2)
