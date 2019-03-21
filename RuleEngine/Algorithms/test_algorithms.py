from unittest import TestCase
from RuleEngine.Algorithms.image_similiarity_measures import run_image_similarity_measures
from RuleEngine.Algorithms.check_channel_mapping import check_channel_mapping
from RuleEngine.Algorithms.compare_resolution import compare_resolution

import numpy as np


class TestAlgorithms(TestCase):

    def test_run_image_similarity_measures(self):
        image_a = np.zeros((512, 512, 3), np.uint8)
        image_b = np.zeros((512, 512, 3), np.uint8)
        scores, result, difference_image = run_image_similarity_measures(image_a, image_b, 1.0)
        self.assertEqual(scores[0], ('compare_mse', 0.0))
        # ('compare_nrmse', 0.0), ('compare_psnr', float('inf')), ('compare_ssim', 1.0)])
        self.assertEqual(result, 'passed')
        # ToDo: Check the binary image 'difference_image'

    def test_check_channel_mapping(self):
        image_a = np.zeros((512, 512, 3), np.uint8)
        image_b = np.zeros((512, 512, 3), np.uint8)
        result = check_channel_mapping(image_a, image_b)
        self.assertEqual(result, False, 'The result should be false')

    def test_compare_resolution(self):
        width_factor, height_factor, band_factor = compare_resolution(np.zeros((512, 512, 3)), np.zeros((512, 512, 3)))
        self.assertEqual(width_factor, 1.0)
        self.assertEqual(height_factor, 1.0)
        self.assertEqual(band_factor, 1.0)

        width_factor, height_factor, band_factor = compare_resolution(np.zeros((512, 512, 3)), np.zeros((1024, 1024, 3)))
        self.assertEqual(width_factor, 0.5)
        self.assertEqual(height_factor, 0.5)
        self.assertEqual(band_factor, 1.0)

        width_factor, height_factor, band_factor = compare_resolution(np.zeros((1024, 1024, 3)), np.zeros((512, 512, 3)))
        self.assertEqual(width_factor, 2.0)
        self.assertEqual(height_factor, 2.0)
        self.assertEqual(band_factor, 1.0)

        width_factor, height_factor, band_factor = compare_resolution(np.zeros((1024, 1024, 3)), np.zeros((512, 512)))
        self.assertEqual(width_factor, float('inf'))
        self.assertEqual(height_factor, float('inf'))
        self.assertEqual(band_factor, float('inf'))
