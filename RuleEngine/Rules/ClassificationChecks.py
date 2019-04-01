import cv2

from RuleEngine.Algorithms.compare_edges import calculate_canny_edges
from RuleEngine.Rules.Rule import Rule


class ClassificationChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(ClassificationChecks, self).__init__(rule_type, parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        """ Has two image paths as inputs, calls functions that concern the use case of validating classifications """
        image_a = cv2.imread(image_path_a)
        image_b = cv2.imread(image_path_b)
        result = {}

        if self._parameters['matching-boundaries']:
            result = calculate_canny_edges(image_a, image_b, combination, self._parameters['matching-boundaries'])
        # if self._parameters['color-band-check']:
        # ToDo: The amount of colors could be checked here, this may be similar to a histogram check [Have to check]

        return result
