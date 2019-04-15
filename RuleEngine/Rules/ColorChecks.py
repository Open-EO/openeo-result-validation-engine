import logging

import cv2

from RuleEngine.Algorithms.compare_histograms import compare_histograms
from RuleEngine.Rules.Rule import Rule


class ColorChecks(Rule):
    def __init__(self, parameters):
        self._name_of_rule = 'color-checks'
        super(ColorChecks, self).__init__(parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        logger = logging.getLogger('ColorChecks')
        image_a = cv2.imread(image_path_a)
        image_b = cv2.imread(image_path_b)
        result = {}

        logger.info('Executing Histogram Check')
        histogram_result = compare_histograms(image_a, image_b)

        # Reminder: Larger is better
        correleation_result = histogram_result.get('Correlation') > 0.5
        intersection_result = histogram_result.get('Intersection') > 1500
        # Reminder: Lower is better
        chi_squared_result = histogram_result.get('Chi-Squared') < 2700
        hellinger_result = histogram_result.get('Hellinger') < 0.50

        rule_result = {
            'Correlation': correleation_result,
            'Intersection': intersection_result,
            'Chi-Squared': chi_squared_result,
            'Hellinger': hellinger_result
        }

        result['compare_histograms'] = histogram_result
        result['compare_histograms']['passed?'] = rule_result
        return result
