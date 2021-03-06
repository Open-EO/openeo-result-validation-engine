import os

import cv2

from RuleEngine.Algorithms.edge_computations import calculate_canny_edges
from RuleEngine.Algorithms.edge_computations import compute_overlap
from RuleEngine.Algorithms.edge_computations import create_comparison_image
from RuleEngine.Rules.Rule import Rule


class ClassificationChecks(Rule):
    def __init__(self, parameters):
        self._name_of_rule = 'classification-checks'
        super(ClassificationChecks, self).__init__(parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        """ Has two image paths as inputs, calls functions that concern the use case of validating classifications """

        image_a = self.read_image(image_path_a)
        image_b = self.read_image(image_path_b)
        result = {'passed': str(False)}
        resize_factor = self._parameters.get('resize-factor')
        try:
            if image_a and image_b:
                print('Images read')
            else:
                return {'passed': False,
                        'message': 'Reading image'}
        except ValueError as e:
            """ Workaround, sometimes the image cannot be loaded and thus we cannot check with .all()"""

        if resize_factor:
            image_a = cv2.resize(image_a, None, fx=resize_factor, fy=resize_factor)
            image_b = cv2.resize(image_b, None, fx=resize_factor, fy=resize_factor)

        # check if X and Y resolution match, some results might already be grayscale while some are RGB images
        if self._parameters.get('matching-boundaries', None) is not None and (image_a.shape[0] == image_b.shape[0]
                                                                              and image_a.shape[1] == image_a.shape[1]):
            result['matching-boundaries'] = {}
            edge_images = calculate_canny_edges(image_a, image_b, align_images=True)
            if create_comparison_image(edge_images) is not None:
                file_save_path = self.create_file_path(combination, 'comparison_image_', '.png')
                cv2.imwrite(file_save_path, create_comparison_image(edge_images))
                result['matching-boundaries']['comparison-image'] = os.path.split(file_save_path)[1]

                edge_detect_result = compute_overlap(edge_images)
                rule_state = edge_detect_result > self._parameters['matching-boundaries']
                result['matching-boundaries']['passed'] = str(rule_state)
                result['passed'] = str(rule_state)
                result['matching-boundaries']['overlap-percentage'] = str(edge_detect_result)

        return result
