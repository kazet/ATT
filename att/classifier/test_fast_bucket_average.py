# pylint: disable=R0904,R0921,C0111

from att.test import TestCase
from att.classifier.fast_bucket_average import FastBucketAverage

class FastBucketAverageTestCase(TestCase):
  def testMultipleBuckets(self):
    fast_bucket_average = FastBucketAverage(0, 10, 10)
    fast_bucket_average.Aggregate(0, 1)
    fast_bucket_average.Aggregate(0, 0)
    fast_bucket_average.Aggregate(1, 2)
    fast_bucket_average.Aggregate(1, 0)
    fast_bucket_average.Aggregate(1.5, 1)
    fast_bucket_average.Aggregate(2, 3)
    fast_bucket_average.Aggregate(2, 0)
    self.assertEqual(fast_bucket_average.Get(0), 0.5)
    self.assertEqual(fast_bucket_average.Get(1), 1)
    self.assertEqual(fast_bucket_average.Get(2), 1.5)
    self.assertEqual(fast_bucket_average.GetBuckets(),
                     [(0.5, 0.0, 1.0, 1.0, 2.0),
                      (1.0, 1.0, 2.0, 3.0, 3.0),
                      (1.5, 2.0, 3.0, 3.0, 2.0),
                      (0.0, 3.0, 4.0, 0.0, 0.0),
                      (0.0, 4.0, 5.0, 0.0, 0.0),
                      (0.0, 5.0, 6.0, 0.0, 0.0),
                      (0.0, 6.0, 7.0, 0.0, 0.0),
                      (0.0, 7.0, 8.0, 0.0, 0.0),
                      (0.0, 8.0, 9.0, 0.0, 0.0),
                      (0.0, 9.0, 10.0, 0.0, 0.0)])
