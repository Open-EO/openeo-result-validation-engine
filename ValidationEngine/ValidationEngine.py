
class ValidationEngine:
    def __init__(self, rule_engine, process_results):
        self.processResults = process_results
        self.ruleEngine = rule_engine
        self.report = []

    def validate(self):
        """ Grabs the next validation rule and calls the function with the arguments """
        current_rule = self.ruleEngine.next_rule()
        if current_rule:
            print('Working on: ' + current_rule.get_rule_type())
            current_rule.set_results(self.processResults)
            current_rule.apply()
            print('Result of rule: ' + str(current_rule.has_passed()))
            self.validate()
        else:
            print('Validation done, results are in!')

