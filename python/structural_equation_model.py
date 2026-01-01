import numpy as np
from sympy import lambdify, Symbol, Eq
from dataclasses import dataclass
import pprint

@dataclass
class StrEq:
	lhs: Symbol
	rhs: object
	fn: callable
	args: set


class SEModel:

	def __init__(self, streq, exovars=None, endovars=None):
		check_endovars(self, streq, endovars)
		self.streq = process_streq(streq)
		check_exovars(self, streq, exovars)

	def __repr__(self):
		space = "\n\t"
		_streq = dict()
		for eq in self.streq:
			_streq[eq] = self.streq[eq].rhs
		return f"SEModel({space}exovars={self.exovars},{space}endovars={self.endovars},{space}streq={_streq}\n)"

def check_endovars(sem:SEModel, streq, endovars):
	inferred_endovars = set(streq.keys())
	if endovars != None and endovars != inferred_endovars:
		raise Exception(f"endovars {endovars} do not match structural equations\n{streq}")
	else:
		sem.endovars = inferred_endovars

def process_streq(streq):
	processed_streq = dict()
	for lhs in streq:
		rhs = streq[lhs]
		seq = StrEq(
			lhs = lhs,
			rhs = rhs,
			fn = lambdify(list(rhs.free_symbols), rhs, modules="numpy"),
			args = rhs.free_symbols
		)
		processed_streq[lhs] = seq
	return processed_streq

def check_exovars(sem:SEModel, streq, exovars):
	all_free_symbols = set()
	for var in streq:
		all_free_symbols = all_free_symbols | streq[var].free_symbols
	inferred_exovars = all_free_symbols - sem.endovars
	if exovars != None and exovars != inferred_exovars:
		raise Exception(f"exovars {exovars} do not match structural equations\n{streq}")
	else:
		sem.exovars = inferred_exovars

def compute_sem_preds(sem:SEModel, exovars:dict):
	"Given the values of exovars, returns a dictionary containing values of all variables of the SEM."
	if not set(sem.exovars) <= set(exovars.keys()):
		raise Exception(f"Supplied exovars {exovars} do not cover exovars of the SEM\n{sem}")

	result = dict()
	for var in exovars:
		result[var] = np.array(exovars[var], dtype="int8")
	result_vars = set(exovars.keys())

	def _compute(seq:StrEq):
		rem_vars = seq.args - result_vars
		while len(rem_vars) != 0:
			var = rem_vars.pop()
			_compute(sem.streq[var])
		kwargs = dict()
		for arg in seq.args:
			kwargs[arg.name] = result[arg]
		result[seq.lhs] = (seq.fn(**kwargs)).astype("int8")

	for var in (sem.endovars - result_vars):
		_compute(sem.streq[var])

	return result


# from sympy.abc import A,B,C,D,E

# AandB = SEModel(
# 	streq={
# 		C: A&B,
# 		D: ~C
# 	}
# )

# pprint.pp(compute(AandB, {A:[1,0], B:[1,1]}))
