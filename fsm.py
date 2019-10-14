"""This is the finite state machine"""

class Rule:
    """Ruleclass"""

    state1 = ''
    state2 = ''
    signal = None
    action = None

    def __init__(self, state1, state2, signal, action):
        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action

class FSM:
    """FSM"""
    current_state = 0
    KPC = None
    rules = []

    all_symbols = '0123456789*#'
    all_digits = '0123456789'

    def reset_state(self):
        """Resets state"""
        self.current_state = 'S_init'

    def set_state(self, rule):
        """Sets state"""
        self.current_state = rule.state2

    def apply_rule(self, rule, input_signal):
        """Check's condition for one rule"""
        return self.current_state == rule.state1 and input_signal in rule.signal

    def get_next_signal(self):
        """Gets next signal"""
        return self.KPC.get_next_signal()

    def run_rules(self, input_symbol):
        """Checks all rules"""
        for rule in self.rules:
            if self.apply_rule(rule, input_symbol):
                self.fire_rule(rule)

    def main_loop(self):
        """Loop that runs forever"""
        self.reset_state()
        while True:
            next_signal = self.get_next_signal
            self.run_rules(next_signal)

    def fire_rule(self, rule):
        """Calls the rules action function"""
        self.set_state(rule)
        rule.action()

    def __init__(self, kpc):

        self.KPC = kpc
        self.rules = [
            Rule('S_init', 'S-read1', self.all_symbols, self.KPC.reset_password_accumulator),
            Rule('S-read1', 'S-read1', self.all_digits, self.KPC.append_next_password_digit),
            Rule('S-read1', 'S-verify', '*', self.KPC.verify_password),
            Rule('S-read1', 'S-init', self.all_digits, self.KPC.reset_agent),
            Rule('S-verify', 'S-init', self.all_digits, self.KPC.reset_agent),
            Rule('S-verify', 'S-Active', 'Y', self.KPC.fully_activate_agent),

            Rule('S-Active', 'S-read2', '*', self.KPC.reset_password_accumulator),
            Rule('S-read2', 'S-Active', '#', self.KPC.refresh),
            Rule('S-read2', 'S-read2', self.all_digits, self.KPC.append_next_password_digit),
            Rule('S-read2', 'S-read3', '*', self.KPC.cache_first_new_passord),
            Rule('S-read3', 'S-read3', self.all_digits, self.KPC.append_next_password_digit),
            Rule('S-read3', 'S-Active', '*', self.KPC.compare_new_password)]
