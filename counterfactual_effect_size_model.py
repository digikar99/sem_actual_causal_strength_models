import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt
from sympy import lambdify, Symbol
from dataclasses import dataclass
from structural_equation_model import SEModel, StrEq, compute_sem_preds
from factual_difference_making import FDMModel
from sys import platform
from pprint import pp

NUM_SIMULATIONS=500000

np.set_printoptions(threshold=10)
if platform == "darwin":
	import matplotlib
	matplotlib.use("qtagg")

class CESModel(SEModel):
	def __init__(self, actuals, streq, exovar_probs, exovars=None, endovars=None):
		super().__init__(streq, exovars=exovars, endovars=endovars)

		if self.exovars != set(exovar_probs.keys()):
			raise Exception(f"Expected probababilities for all exovars {self.exovars}")
		else:
			self.exovar_probs = exovar_probs
		self.actuals = actuals

	def __repr__(self):
		space = "\n\t"
		_streq = dict()
		for eq in self.streq:
			_streq[eq] = self.streq[eq].rhs
		return f"CESModel({space}actuals={self.actuals},{space}exovars={self.exovars},{space}exovar_probs={self.exovar_probs},{space}endovars={self.endovars},{space}streq={_streq}\n)"

def as_cesmodel(model):
	if type(model) == FDMModel:
		return CESModel(
			actuals = model.literals,
			streq = model._streq,
			exovar_probs = model.relative_normality
		)
	else:
		raise Exception("as_cesmodel not implemented for", type(model))

def compute_sampling_propensity(event:Symbol, prob:float, actuals:set, stability:float=None):
	"""
	According to the discussion on Extended Structural Model
	from the section "A formal model of counterfactual sampling".
	"""
	if stability is None: stability = STABILITY
	delta = (event in actuals)
	return stability*delta + (1-stability)*prob

def draw(event, num_simulations, actuals:set, p:float, stability:float):
	sp = compute_sampling_propensity(event, p, actuals, stability=stability)
	return r.binomial(1, size=num_simulations, p=sp).astype("int8")

def compute_cesm_preds(
		cesm:CESModel,
		num_simulations:int,
		candidate_causes:list,
		effect:Symbol,
		stability:float=0.73
):
	# int8 is the appropriate data type, because during the sum of the delta below,
	#   spurious positive and negative effects can then sum up to zero.
	# uint8 or bool would not allow such summing up the deltas to zero.
	exovar_samples = dict()
	for var in cesm.exovars:
		exovar_samples[var] = draw(
			var, num_simulations, cesm.actuals, cesm.exovar_probs[var],
			stability
		)

	initial_preds = compute_sem_preds(cesm, exovar_samples)

	strengths = []
	for var in candidate_causes:
		new_exovar_samples = exovar_samples.copy()
		new_exovar_samples[var] = 1 - initial_preds[var] # assume binary variables
		# counterfactual predictions
		new_preds = compute_sem_preds(cesm, new_exovar_samples)
		delta_var = initial_preds[var] - new_preds[var]
		delta_eff = initial_preds[effect] - new_preds[effect]
		std_var = np.std(initial_preds[var])
		std_eff = np.std(initial_preds[effect])
		strength = np.mean(
			delta_eff / delta_var * std_var / std_eff
		)
		# strength = np.sum(delta_eff / delta_var) * std_var / std_eff / num_simulations
		# strength = np.corrcoef(initial_preds[var], initial_preds[effect])[0,1]
		strengths.append(strength)
	return strengths

def compare_cesm_scores(cesm:CESModel, causes:list, effect:Symbol, stability:list, num_simulations:int = NUM_SIMULATIONS, plot=False):
	causal_scores = dict()
	cause_names = [c.name for c in causes]
	for s in stability:
		causal_scores[s] = list()
		scores = compute_cesm_preds(
			cesm, num_simulations, causes, effect, s
		)
		for c, cs in zip(causes, scores):
			causal_scores[s].append(cs)
		if plot:
			plt.plot(cause_names, causal_scores[s], label="{:.1f}".format(s))
	if plot:
		plt.ylim(0,1)
		plt.legend()
		plt.show()
	return causal_scores
