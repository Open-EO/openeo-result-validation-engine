from RuleEngine.Rules.Rule import Rule


class InputDataChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(InputDataChecks, self).__init__(rule_type, parameters)

    # ToDo: Think how the input data could be tested, e.g. comparing against reference data?
