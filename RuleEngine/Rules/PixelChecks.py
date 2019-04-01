import cv2
import logging

from RuleEngine.Algorithms.check_channel_mapping import check_channel_mapping
from RuleEngine.Algorithms.compare_histograms import compare_histograms
from RuleEngine.Algorithms.compare_resolution import compare_resolution
from RuleEngine.Algorithms.image_similiarity_measures import image_similarity_measures
from RuleEngine.Rules.Rule import Rule


class PixelChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(PixelChecks, self).__init__(rule_type, parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        logger = logging.getLogger('PixelChecks')
        """ Has two image paths as input, the threshold comes from the instantiation of the rule"""
        image_a = cv2.imread(image_path_a)
        image_b = cv2.imread(image_path_b)
        result = {}

        if self._parameters['allow-different-channel-map'] == 'False':
            result['check-channel-mapping']= check_channel_mapping(image_a, image_b)

        if self._parameters['image-similarity-measures'] == 'True':
            logger.info('Executing Histogram Check')
            result['compare_histograms'] = compare_histograms(image_a, image_b)
            result['compare_resolution'] = compare_resolution(image_a, image_b)
            if result['compare_resolution'] == (1.0, 1.0, 1.0):
                logger.info('Executing Image Similarity measures')
                # ToDo: Create proper naming for the difference image
                combination = ((combination[0].strip('.png')).strip('.jpg') +
                               '_' + (combination[1].strip('.png')).strip('.jpg')).replace('/', '_')
                combination = 'reports/SSIM' + combination

                result['image-similarity-measures'] = image_similarity_measures(image_a, image_b, combination,
                                                                                self._parameters['threshold'])
            else:
                result['image-similarity-measures'] = 'The test was not able to run for this combination'

        return result
