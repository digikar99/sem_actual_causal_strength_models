from sympy import symbols, Symbol, Eq, Or, And, Not
from sympy.abc import A, B, C, D, E, F
from queue import Queue

def compute_normality(expr, streq:dict, roots_prob:dict):
	# TODO: Rename roots_prob to be something more meaningful
	"""
	literal: Literal for which the normality measure is to be computed
	streq: Structural Equations of the causal model
	roots_prob: Dictionary mapping literals to their probablities
	"""
	return compute_normality_functions[type(expr)](expr, streq, roots_prob)

def compute_normality_symbol(symbol:Symbol, streq:dict, roots_prob:dict):
	if symbol in roots_prob:
		return roots_prob[symbol]
	else:
		eqn = streq[symbol]
		rhs = eqn.rhs
		return compute_normality_functions[type(rhs)](rhs, streq, roots_prob)

def compute_normality_not(expr:Not, streq:dict, roots_prob:dict):
	arg0 = expr.args[0]
	normality_arg0 = compute_normality_functions[type(arg0)](arg0, streq, roots_prob)
	return  1 - normality_arg0

def compute_normality_and(expr:And, streq:dict, roots_prob:dict):
	if (len(expr.args) > 2):
		raise Exception(f"Normality computation only implemented for binary And, but was given {expr}")
	arg0 = expr.args[0]
	arg1 = expr.args[1]
	normality_arg0 = compute_normality_functions[type(arg0)](arg0, streq, roots_prob)
	normality_arg1 = compute_normality_functions[type(arg1)](arg1, streq, roots_prob)
	are_independent = check_independence(arg0, arg1, streq, roots_prob)
	if not are_independent:
		raise Exception(f"Cannot compute normality (probability) score for non-independent args. sub-expressions of {expr} were determined to be non-independent.")
	return normality_arg0 * normality_arg1

def get_ancestors(expr, streq):
	ancestors = set()
	q = Queue()
	if expr.is_symbol:
		q.put(expr)
	else:
		for arg in expr.args:
			q.put(arg)
	while not q.empty():
		current = q.get()
		ancestors.add(current)
		if current in streq:
			for arg in streq[current].rhs.args:
				q.put(arg)
	return ancestors

def check_independence(args1, args2, streq, roots_prob):
	anc1 = get_ancestors(args1, streq)
	anc2 = get_ancestors(args2, streq)
	if len(anc1 & anc2) > 0: return False
	else: return True

def compute_normality_or(expr:Or, streq:dict, roots_prob:dict):
	if (len(expr.args) > 2):
		raise Exception(f"Normality computation only implemented for binary Or, but was given {expr}")
	arg0 = expr.args[0]
	arg1 = expr.args[1]
	normality_arg0 = compute_normality_functions[type(arg0)](arg0, streq, roots_prob)
	normality_arg1 = compute_normality_functions[type(arg1)](arg1, streq, roots_prob)
	are_independent = check_independence(arg0, arg1, streq, roots_prob)
	if not are_independent:
		raise Exception(f"Cannot compute normality (probability) score for non-independent args. sub-expressions of {expr} were determined to be non-independent.")
	return normality_arg0 + normality_arg1 - normality_arg0 * normality_arg1

compute_normality_functions = {
	And: compute_normality_and,
	Or: compute_normality_or,
	Not: compute_normality_not,
	Symbol: compute_normality_symbol
}

