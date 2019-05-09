import importlib

RULES_DIRECTORY = 'RuleEngine.Rules.'


class RuleFactory:
    __instance = None

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

    def create_rule(self, rule_name, parameters):
        pascal_case_rule_name = self.pascal_rule_name(rule_name)

        try:
            imported_module = importlib.import_module(RULES_DIRECTORY + pascal_case_rule_name)
            class_ = getattr(imported_module, pascal_case_rule_name)
        except ImportError:
            print('Rule not implemented - skipping')
            return None

        if pascal_case_rule_name is not None:
            return class_(parameters)

    @staticmethod
    def pascal_rule_name(name):
        pascal_rule = name.split('-')
        rule_name = ''
        for word in pascal_rule:
            rule_name += word.capitalize()
        return rule_name

