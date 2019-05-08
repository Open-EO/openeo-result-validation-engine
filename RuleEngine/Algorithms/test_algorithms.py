from unittest import TestCase

import numpy as np

from RuleEngine.Algorithms.compare_file_extensions import compare_file_extensions
from RuleEngine.Algorithms.compare_resolution import compare_resolution
from RuleEngine.Algorithms.edge_computations import compute_overlap
from RuleEngine.Algorithms.image_similiarity_measures import image_similarity_measures


class TestAlgorithms(TestCase):

    def test_run_image_similarity_measures(self):
        image_a = np.zeros((512, 512, 3), np.uint8)
        image_b = np.zeros((512, 512, 3), np.uint8)
        result, diff_image = image_similarity_measures(image_a, image_b)
        self.assertEqual(diff_image.all(), np.ones((512, 512, 1)).all())

    def test_compare_resolution(self):
        result = compare_resolution(np.zeros((512, 512, 3)), np.zeros((512, 512, 3)))
        self.assertEqual(result['resolution_factors'], [1.0, 1.0, 1.0])

        result = compare_resolution(np.zeros((512, 512, 3)), np.zeros((1024, 1024, 3)))
        self.assertEqual(result['resolution_factors'], [0.5, 0.5, 1.0])

        result = compare_resolution(np.zeros((1024, 1024, 3)), np.zeros((512, 512, 3)))
        self.assertEqual(result['resolution_factors'], [2.0, 2.0, 1.0])

        result = compare_resolution(np.zeros((1024, 1024, 3)), np.zeros((512, 512)))
        self.assertEqual(result['resolution_factors'], None)

    def test_compare_filenames(self):
        file_a = 'test/test.png'
        res = compare_file_extensions(file_a, 'test.png')
        self.assertEqual(res, True)

        file_a = 'test.tiff'
        res = compare_file_extensions(file_a, 'test.png')
        self.assertEqual(res, False)

        file_a = 'test.tiff'
        res = compare_file_extensions(file_a, 'test.tiff')
        self.assertEqual(res, True)

        file_a = 'test.tiff'
        res = compare_file_extensions(file_a, 'test.TIFF')
        self.assertEqual(res, True)

    def test_compute_overlap(self):
        image_a = np.zeros((2, 3), np.uint8)
        image_b = np.zeros((2, 3), np.uint8)
        image_a[0:2, 0:2] = 1
        image_b[0:2, 1:3] = 1
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 1/3)

        image_a = np.zeros((2,2), np.uint8)
        image_b = np.zeros((2,2), np.uint8)
        image_a[0:1, 0:2] = 1
        image_b[0:1, 0:2] = 1
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 1.0)

        image_a = np.zeros((2,2), np.uint8)
        image_b = np.zeros((2,2), np.uint8)
        image_a[0:1, 0:2] = 1
        image_b[0:1, 1:2] = 1
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 0.5)

        image_a = np.zeros((4,4), np.uint8)
        image_b = np.zeros((4,4), np.uint8)
        image_a[:2, :2] = 1
        image_b[:1, :2] = 1
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 0.5)

        image_a = np.zeros((4,4), np.uint8)
        image_b = np.zeros((4,4), np.uint8)
        image_a[1:3, :4] = 1
        image_b[1:2, :3] = 1
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 0.375)

        image_a = np.ones((4,4), np.uint8)
        image_b = np.ones((4,4), np.uint8)
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 1)

        image_a = np.zeros((6,6), np.uint8)
        image_b = np.zeros((6,6), np.uint8)
        image_a[1:3, :4] = 1
        image_b[1:3, :4] = 1
        image_a[4:6, :4] = 1
        edges = [image_b, image_a]
        res = compute_overlap(edges)
        self.assertEqual(res, 0.5)

