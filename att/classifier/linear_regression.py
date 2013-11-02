from att.utils import Average

def LinearRegression(data):
  """Performs the linear regression.
  Args:
    data: a list of pairs: (x, y), each pair corresponding to
    one point from the data you want to approximate.

  Returns:
    a pair, (alpha, beta), such that y = alpha + beta * x is the best
    approximation of the data provided.
  """
  x_coords = [x for x, unused_y in data]
  x_coords_squared = [x * x for x, unused_y in data]
  y_coords = [y for unused_x, y in data]
  beta = ((Average([x * y for x, y in data]) -
          Average(x_coords) * Average(y_coords)) /
          (Average(x_coords_squared) - (Average(x_coords) ** 2)))
  alpha = Average(y_coords) - beta * Average(x_coords)
  return (alpha, beta)
