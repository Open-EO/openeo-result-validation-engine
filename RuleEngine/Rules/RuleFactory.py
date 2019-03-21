from RuleEngine.Rules.PixelChecks import PixelChecks
from RuleEngine.Rules.ClassificationChecks import ClassificationChecks
from RuleEngine.Rules.InputDataChecks import InputDataChecks
from RuleEngine.Rules.OutputDataChecks import OutputDataChecks


class RuleFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_rule(outputformat, rulename, parameters):
        if rulename == 'pixel-checks':
            return PixelChecks(rulename, parameters)
        elif rulename == 'input-data-checks':
            return InputDataChecks(rulename, parameters)
        elif rulename == 'output-data-checks':
            return OutputDataChecks(rulename, parameters)
        elif rulename == 'classification-checks':
            return ClassificationChecks(rulename, parameters)
        else:
            return None
