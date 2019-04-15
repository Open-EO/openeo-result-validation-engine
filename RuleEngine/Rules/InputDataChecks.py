from RuleEngine.Rules.Rule import Rule


class InputDataChecks(Rule):
    def __init__(self, parameters):
        self._name_of_rule = 'input-data-checks'
        super(InputDataChecks, self).__init__(parameters)

    # ToDo: Think how the input data could be tested, e.g. comparing against reference data?
