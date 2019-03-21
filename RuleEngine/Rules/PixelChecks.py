from RuleEngine.Rules.Rule import Rule
from RuleEngine.Algorithms.check_channel_mapping import check_channel_mapping
from RuleEngine.Algorithms.image_similiarity_measures import run_image_similarity_measures
from RuleEngine.Algorithms.compare_resolution import compare_resolution
from RuleEngine.Algorithms.compare_histograms import compare_histograms

import cv2


class PixelChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(PixelChecks, self).__init__(rule_type, parameters)

    def apply(self):
        result_dict = {}
        for combination in self.get_result_combinations():
            combination_result = self.check_rule(combination[0], combination[1])
            result_dict[combination] = combination_result
        return result_dict

    def check_rule(self, image_path_a, image_path_b):
        """ Has two image paths as input, the threshold comes from the instantiation of the rule"""
        threshold = self.parameters['threshold']
        image_a = cv2.imread(image_path_a)
        image_b = cv2.imread(image_path_b)
        result = {}

        if self.parameters['allow-different-channel-map'] == 'False':
            result['check-channel-mapping']= check_channel_mapping(image_a, image_b)

        if self.parameters['image-similarity-measures'] == 'True':
            result['compare_histograms'] = compare_histograms(image_a, image_b)

            if compare_resolution(image_a, image_b) == (1.0, 1.0, 1.0):
                result['image-similarity-measures'] = run_image_similarity_measures(image_a, image_b, threshold)
            else:
                result['image-similarity-measures'] = 'The test was not able to run for this combination'

        return result


