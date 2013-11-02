# pylint: disable=R0904,R0921,C0111

from att.test import TestCase
from att.classifier.bucket_aggregator import BucketAggregator

class BucketAggregatorTestCase(TestCase):
  def testSameKeys(self):
    bucket_aggregator = BucketAggregator(num_buckets=5)
    bucket_aggregator.Train(
        [(1, 1), (2, 1), (2, 2), (3, 3), (4, 4),
         (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
    self.assertAlmostEqual(bucket_aggregator.Get(2), 1.5)

  def testBuckets(self):
    bucket_aggregator = BucketAggregator(num_buckets=5)
    bucket_aggregator.Train(
        [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4),
         (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
    self.assertAlmostEqual(bucket_aggregator.Get(0), 0.5)
    self.assertAlmostEqual(bucket_aggregator.Get(2), 2.5)
    self.assertAlmostEqual(bucket_aggregator.Get(9), 8.5)

  def testSingletonBuckets(self):
    bucket_aggregator = BucketAggregator(num_buckets=10)
    bucket_aggregator.Train(
        [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4),
         (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])
    self.assertAlmostEqual(bucket_aggregator.Get(0), 0)
    self.assertAlmostEqual(bucket_aggregator.Get(2), 2)
    self.assertAlmostEqual(bucket_aggregator.Get(9), 9)

  def testSingleBucket(self):
    bucket_aggregator = BucketAggregator(num_buckets=5)
    bucket_aggregator.Train(
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
         (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)])
    self.assertAlmostEqual(bucket_aggregator.Get(-9), 0)
    self.assertAlmostEqual(bucket_aggregator.Get(0), 0)
    self.assertAlmostEqual(bucket_aggregator.Get(9), 0)
