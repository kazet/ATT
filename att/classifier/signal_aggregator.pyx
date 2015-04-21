from libc.stdlib cimport calloc, free, rand
from att.utils import First, Second
import sys
cimport cython

cdef extern from "limits.h":
    int INT_MAX

def __cinit__():
  pass

#  Returns a list of weights that maximizes the number of correct
#  decisions - decision per object is calculated as
#  signal1 * weight1 + ... + signaln * weightn > 1 ? 1 : 0
# 
#  Args:
#  - signals: a list of pairs: (signal values, decision)
#  - decisions: a list of binary decisions, aligned or not, for each record
#  - num_iterations: number of simulated annealing iterations
#  - initial_temp: initial simulated annealing temperature
#  - temp_decrease: how much should be the temperature decreased
#       (multiplied by (1.0 - temp_decrease)) every temp_decrease_every
#  - temp_decrease_every: every how much steps should the temperature
#       be multiplied by (1.0 - temp_decrease)
# 
#  Returns:
#  - an array of floats: the weights, one per signal
def TuneWeights(inputs,
                num_iterations=20000,
                initial_temp=10,
                temp_decrease=0.01,
                temp_decrease_every=20):
  if len(inputs) == 0:
    raise Exception("Inputs for weight tuning should be non-empty")
  num_signals = len(First(inputs[0]))
  cdef float* csignals = <float*> calloc(sizeof(float), num_signals * len(inputs))
  cdef int* cdecisions = <int*> calloc(sizeof(int), len(inputs))
  for i in range(0, len(inputs)):
    for j in range(0, num_signals):
      csignals[i * num_signals + j] = First(inputs[i])[j]
    cdecisions[i] = Second(inputs[i])

  cdef float* cweights = CTuneWeights(
      csignals,
      cdecisions,
      num_signals,
      len(inputs),
      num_iterations,
      initial_temp,
      temp_decrease,
      temp_decrease_every)

  cdef float quality = CEvaluateWeights(
      num_signals,
      len(inputs),
      csignals,
      cweights,
      cdecisions)

  weights = []
  for i in range(0, num_signals):
    weights.append(cweights[i])
  free(cweights)
  free(csignals)
  free(cdecisions)

  return (weights, quality)

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef CRandFloat(float mi, float ma):
  return mi + (ma - mi) * rand() / float(INT_MAX)

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef float* CTuneWeights(
    float* signals,
    int* decisions,
    int num_signals,
    int num_records,
    int num_iterations,
    float initial_temp,
    float temp_decrease,
    float temp_decrease_every):
  cdef float* weights = <float*> calloc(sizeof(float), num_signals)
  cdef int i
  for i in range(num_signals):
    weights[i] = CRandFloat(-0.5, 0.5) + 1.0 / num_signals

  cdef float temp = initial_temp
  cdef float base_quality = CEvaluateWeights(num_signals,
                                             num_records,
                                             signals,
                                             weights,
                                             decisions)
  cdef int weight
  cdef float base_weight_value
  cdef float expt_quality
  cdef int iter
  for iter in range(num_iterations):
    if iter % 100 == 0:
      sys.stdout.write("iter=%d, base_quality=%.3f, expt_quality=%.3f, temp=%.9f" % (
                       iter,
                       base_quality * 100.0,
                       expt_quality * 100.0,
                       temp))
      for weight in range(num_signals):
        sys.stdout.write(", weights[%d]=%.3f" % (weight, weights[weight]))
      sys.stdout.write("\n")

    weight = rand() % num_signals
    base_weight_value = weights[weight]
    weights[weight] += CRandFloat(-temp, temp) 
    expt_quality = CEvaluateWeights(num_signals,
                                    num_records,
                                    signals,
                                    weights,
                                    decisions)
    if expt_quality >= base_quality:
      base_quality = expt_quality
    else:
      weights[weight] = base_weight_value

    if iter % temp_decrease_every == 0:
      temp = temp * (1.0 - temp_decrease)
  return weights

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef float CEvaluateWeights(
  int num_signals,
  int num_records,
  float* signals,
  float* weights,
  int* decisions):
  cdef int decision
  cdef float combined_signals
  cdef int count = 0
  cdef int record
  cdef int signal
  for record in range(num_records):
    combined_signals = 0
    for signal in range(num_signals):
      combined_signals += weights[signal] * signals[record * num_signals + signal]
    decision = combined_signals > 1.0
    if decision == decisions[record]:
      count += 1
  return count / (1.0 * num_records)
