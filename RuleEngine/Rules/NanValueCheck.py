from RuleEngine.Algorithms.check_nan_value import check_nan_value
from RuleEngine.Rules.Rule import Rule


class NanValueCheck(Rule):
    def __init__(self, parameters):
        self._files = []
        self._name_of_rule = 'nan-value-check'
        super(NanValueCheck, self).__init__(parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        """ Has two image paths as inputs, calls functions that concern the use case of validating classifications """
        image_a = self.read_image(image_path_a)
        image_b = self.read_image(image_path_b)

        try:
            if image_a and image_b:
                print('Images read')
            else:
                return {'passed': False,
                        'message': 'Reading image'}
        except ValueError as e:
            """ Workaround, sometimes the image cannot be loaded and thus we cannot check with .all()"""

        result = {
            'passed': str(True)
        }

        if self._parameters.get('allow-nan', None) is False:
            result_check_nan = check_nan_value(image_a, image_b)
            if result_check_nan:
                passed = True if result_check_nan['file_a'] == result_check_nan['file_b'] else False
                result = {
                    'nan-value-comparison': result_check_nan,
                    'passed': str(passed)
                    }

        return result
