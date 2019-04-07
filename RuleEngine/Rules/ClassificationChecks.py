import cv2

from RuleEngine.Algorithms.edge_computations import calculate_canny_edges
from RuleEngine.Algorithms.edge_computations import compute_overlap
from RuleEngine.Algorithms.edge_computations import create_comparison_image
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
            result['matching-boundaries'] = {}
            edge_images = calculate_canny_edges(image_a, image_b)

            if create_comparison_image(edge_images) is not None:
                file_save_path = 'reports/comparison_image_' + self.create_file_path(combination) + '.png'
                cv2.imwrite(file_save_path, create_comparison_image(edge_images))
                result['matching-boundaries']['comparison-image'] = file_save_path

            edge_detect_result = compute_overlap(edge_images)
            if edge_detect_result:
                rule_state = edge_detect_result < float(self._parameters['matching-boundaries'])
                rule_state = 'passed' if rule_state else 'failed'
                result['matching-boundaries']['overlap-check'] = {
                    'rule': rule_state,
                    'percent-difference': str(edge_detect_result),
                }
            else:
                result['matching-boundaries']['overlap-check'] = 'Test was not able to run due to different image sizes'

        return result
