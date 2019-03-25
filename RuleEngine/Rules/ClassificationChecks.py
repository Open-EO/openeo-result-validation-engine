import cv2

from RuleEngine.Algorithms.compare_edges import calculate_canny_edges
from RuleEngine.Rules.Rule import Rule


class ClassificationChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(ClassificationChecks, self).__init__(rule_type, parameters)

    def apply(self):
        result_dict = {}
        for combination in self.get_result_combinations():
            combination_result = self.check_rule(combination[0], combination[1])
            result_dict[str(combination)] = combination_result
        return result_dict

    def check_rule(self, image_path_a, image_path_b):
        """ Has two image paths as input, the threshold comes from the instantiation of the rule"""
        image_a = cv2.imread(image_path_a)
        image_b = cv2.imread(image_path_b)
        result = {}

        # Check boundaries
        if self._parameters['matching-boundaries']:
            difference_edges_factor, diff_image = calculate_canny_edges(image_a, image_b)

            if difference_edges_factor < float(self._parameters['matching-boundaries']):
                result['matching-boundaries'] = ['passed', 'Edge-diff: ' + str(difference_edges_factor)]
            else:
                result['matching-boundaries'] = ['failed', 'Edge-diff-factor: ' + str(difference_edges_factor)]

        return result
