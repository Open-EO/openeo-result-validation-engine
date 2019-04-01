from RuleEngine.Rules.PixelChecks import PixelChecks
from RuleEngine.Rules.ClassificationChecks import ClassificationChecks
from RuleEngine.Rules.InputDataChecks import InputDataChecks
from RuleEngine.Rules.OutputDataChecks import OutputDataChecks


class RuleFactory:
    __instance = None

    rules = {
        'pixel-checks': PixelChecks,
        'input-data-checks': InputDataChecks,
        'output-data-checks': OutputDataChecks,
        'classification-checks': ClassificationChecks
    }

    def __init__(self):
        if RuleFactory.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            RuleFactory.__instance = self

    @staticmethod
    def get_instance():
        if RuleFactory.__instance is None:
            RuleFactory()
        return RuleFactory.__instance

    def create_rule(self, output_format, rulename, parameters):
        # ToDo: Remove special case and add return None for all rules that do not exist
        if rulename == 'output-data-checks':
            return self.rules[rulename](rulename, parameters, output_format)
        elif rulename in self.rules:
            return self.rules[rulename](rulename, parameters)
        else:
            return None

