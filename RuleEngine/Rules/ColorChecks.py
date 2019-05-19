import logging

from RuleEngine.Algorithms.compare_histograms import compare_histograms
from RuleEngine.Rules.Rule import Rule


class ColorChecks(Rule):
    def __init__(self, parameters):
        self._name_of_rule = 'color-checks'
        super(ColorChecks, self).__init__(parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        logger = logging.getLogger('ColorChecks')
        image_a = self.read_image(image_path_a)
        image_b = self.read_image(image_path_b)
        result = {}

        try:
            if image_a and image_b:
                print('Images read')
            else:
                return {'passed': False,
                        'message': 'Reading image'}
        except ValueError as e:
            """ Workaround, sometimes the image cannot be loaded and thus we cannot check with .all()"""

        logger.info('Executing Histogram Check')
        histogram_result = compare_histograms(image_a, image_b)


        if histogram_result:
            # Reminder: Larger is better
            correleation_result = histogram_result.get('Correlation') > self._parameters.get('threshold-correlation',
                                                                                             0.5)
            intersection_result = histogram_result.get('Intersection') > self._parameters.get('threshold-intersection',
                                                                                              2700)
            # Reminder: Lower is better
            chi_squared_result = histogram_result.get('Chi-Squared') < self._parameters.get('threshold-chi-squared',
                                                                                            1500)
            hellinger_result = histogram_result.get('Hellinger') < self._parameters.get('threshold-hellinger', 0.5)

            rule_result = {
                'Correlation': correleation_result,
                'Intersection': intersection_result,
                'Chi-Squared': chi_squared_result,
                'Hellinger': hellinger_result
            }

            result['histograms'] = histogram_result
            result['histograms']['passed'] = rule_result
            # We skip the other histogram comparisons as they are hard to judge, however we add them to the report
            result['passed'] = str(correleation_result)

        return result
