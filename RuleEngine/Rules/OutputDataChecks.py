from RuleEngine.Rules.Rule import Rule


class OutputDataChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(OutputDataChecks, self).__init__(rule_type, parameters)

    # ToDo: Check file size between results

    # ToDo: Check file extension between results
