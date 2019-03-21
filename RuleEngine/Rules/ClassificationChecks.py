from RuleEngine.Rules.Rule import Rule


class ClassificationChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(ClassificationChecks, self).__init__(rule_type, parameters)

    # ToDo: Check results between calls of 'compare_edges' as they should be equal or close to equal
