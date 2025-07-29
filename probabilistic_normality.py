from sympy import symbols, Symbol, Eq, Or, And, Not
from sympy.abc import A, B, C, D, E, F

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
	are_independent = check_independence(roots_prob, arg0, arg1)
	if not are_independent:
		raise Exception(f"Cannot compute normality (probability) score for non-independent args. sub-expressions of {expr} were determined to be non-independent.")
	return normality_arg0 * normality_arg1

def check_independence(roots_prob, *args):
	return all(map(lambda arg: arg.is_symbol and arg in roots_prob, args))

def compute_normality_or(expr:Or, streq:dict, roots_prob:dict):
	if (len(expr.args) > 2):
		raise Exception(f"Normality computation only implemented for binary Or, but was given {expr}")
	arg0 = expr.args[0]
	arg1 = expr.args[1]
	normality_arg0 = compute_normality_functions[type(arg0)](arg0, streq, roots_prob)
	normality_arg1 = compute_normality_functions[type(arg1)](arg1, streq, roots_prob)
	are_independent = check_independence(roots_prob, arg0, arg1)
	if not are_independent:
		raise Exception(f"Cannot compute normality (probability) score for non-independent args. sub-expressions of {expr} were determined to be non-independent.")
	return normality_arg0 + normality_arg1 - normality_arg0 * normality_arg1

compute_normality_functions = {
	And: compute_normality_and,
	Or: compute_normality_or,
	Not: compute_normality_not,
	Symbol: compute_normality_symbol
}

