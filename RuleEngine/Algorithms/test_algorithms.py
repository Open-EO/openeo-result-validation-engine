from unittest import TestCase

import numpy as np

from RuleEngine.Algorithms.check_channel_mapping import check_channel_mapping
from RuleEngine.Algorithms.compare_file_extensions import compare_file_extensions
from RuleEngine.Algorithms.compare_resolution import compare_resolution
from RuleEngine.Algorithms.edge_computations import compute_overlap
from RuleEngine.Algorithms.image_similiarity_measures import image_similarity_measures


class TestAlgorithms(TestCase):

    def test_run_image_similarity_measures(self):
        image_a = np.zeros((512, 512, 3), np.uint8)
        image_b = np.zeros((512, 512, 3), np.uint8)
        result = image_similarity_measures(image_a, image_b)
        # ToDo: Reimplement proper test

    def test_check_channel_mapping(self):
        image_a = np.zeros((512, 512, 3), np.uint8)
        image_b = np.zeros((512, 512, 3), np.uint8)
        result = check_channel_mapping(image_a, image_b)
        self.assertEqual(result, False, 'The result should be false')

    def test_compare_resolution(self):
        result = compare_resolution(np.zeros((512, 512, 3)), np.zeros((512, 512, 3)))
        self.assertEqual(result, {'widthFactor': 1,
                                  'heightFactor': 1,
                                  'bandsFactor': 1})

        result = compare_resolution(np.zeros((512, 512, 3)), np.zeros((1024, 1024, 3)))
        self.assertEqual(result, {'widthFactor': 0.5,
                                  'heightFactor': 0.5,
                                  'bandsFactor': 1})

        result = compare_resolution(np.zeros((1024, 1024, 3)), np.zeros((512, 512, 3)))
        self.assertEqual(result, {'widthFactor': 2.0,
                                  'heightFactor': 2.0,
                                  'bandsFactor': 1})

        result = compare_resolution(np.zeros((1024, 1024, 3)), np.zeros((512, 512)))
        self.assertEqual(result, {'widthFactor': None,
                                  'heightFactor': None,
                                  'bandsFactor': None})

    def test_compare_filenames(self):
        file_a = 'test/test.png'
        res = compare_file_extensions(file_a, 'png')
        self.assertEqual(res, True)

        file_a = 'test.tiff'
        res = compare_file_extensions(file_a, 'png')
        self.assertEqual(res, False)

        file_a = 'test.tiff'
        res = compare_file_extensions(file_a, 'tiff')
        self.assertEqual(res, True)

        file_a = 'test.tiff'
        res = compare_file_extensions(file_a, 'TIFF')
        self.assertEqual(res, True)

    def test_compute_overlap(self):
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
        print(image_a)
        print(image_b)
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 0.375)

        image_a = np.ones((4,4), np.uint8)
        image_b = np.ones((4,4), np.uint8)
        print(image_a)
        print(image_b)
        edges = [image_a, image_b]
        res = compute_overlap(edges)
        self.assertEqual(res, 1)
