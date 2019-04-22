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

        result = {}
        if self._parameters.get('allow-nan', None) is True:
            result['nan-value-comparison'] = check_nan_value(image_a, image_b),

        return result
