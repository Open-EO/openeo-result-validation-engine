from RuleEngine.Rules.Rule import Rule
from RuleEngine.Algorithms.check_channel_mapping import check_channel_mapping
from RuleEngine.Algorithms.image_similiarity_measures import run_image_similarity_measures
from RuleEngine.Algorithms.compare_resolution import compare_resolution

import cv2


class PixelChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(PixelChecks, self).__init__(rule_type, parameters)

    def apply(self):
        result_array = []
        for combination in self.get_result_combinations():
            image_combination, scores, result, difference_image = self.check_rule(combination[0], combination[1])
            result_array.append((image_combination, scores, result, difference_image))
        return result_array

    def check_rule(self, image_path_a, image_path_b):
        """ Has two image paths as input, the threshold comes from the instantiation of the rule"""
        threshold = self.parameters['threshold']
        image_a = cv2.imread(image_path_a)
        image_b = cv2.imread(image_path_b)

        if self.parameters['allow-different-channel-map'] == 'False':
            print(check_channel_mapping(image_a, image_b))

        if self.parameters['image-similarity-measures'] == 'True':
            if compare_resolution(image_a, image_b) == (1.0, 1.0, 1.0):
                scores, result, difference_image = run_image_similarity_measures(image_a, image_b, threshold)
            else:
                print('The test was not able to run for this combination: ' + image_path_a + ' and ' + image_path_b)
                scores = []
                result = 'failed'
                difference_image = []


        try:
            if result == 'failed' and image_path_a == image_path_b:
                raise Exception('the check should never fail if the input images are the same')
        except Exception as error:
            print(error)

        return (image_path_a, image_path_b), scores, result, difference_image


