import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt
from sympy import lambdify, Symbol
from dataclasses import dataclass
from structural_equation_model import SEModel, StrEq, compute_sem_preds

NUM_SIMULATIONS=500000

np.set_printoptions(threshold=10)

class CESModel(SEModel):
	def __init__(self, streq, exovar_probs, exovars=None, endovars=None):
		super().__init__(streq, exovars=exovars, endovars=endovars)

		if self.exovars != set(exovar_probs.keys()):
			raise Exception(f"Expected probababilities for all exovars {self.exovars}")
		else:
			self.exovar_probs = exovar_probs

	def __repr__(self):
		space = "\n\t"
		_streq = dict()
		for eq in self.streq:
			_streq[eq] = self.streq[eq].rhs
		return f"CESModel({space}exovars={self.exovars},{space}exovar_probs={self.exovar_probs},{space}endovars={self.endovars},{space}streq={_streq}\n)"

def compute_sampling_propensity(event:Symbol, prob:float, actual:set, stability:float=None):
	"""
	According to the discussion on Extended Structural Model
	from the section "A formal model of counterfactual sampling".
	"""
	if stability is None: stability = STABILITY
	delta = (event in actual)
	return stability*delta + (1-stability)*prob

def draw(event, num_simulations, actuals:set, p:float, stability:float):
	sp = compute_sampling_propensity(event, p, actuals, stability=stability)
	return r.binomial(1, size=num_simulations, p=sp)

def compute_cesm_preds(
		cesm:CESModel,
		num_simulations:int,
		actuals:set,
		candidate_causes:list,
		effect:Symbol,
		stability:float=0.73
):
	exovar_samples = dict()
	for var in cesm.exovars:
		exovar_samples[var] = draw(
			var, num_simulations, actuals, cesm.exovar_probs[var],
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
		strengths.append(strength)
	return strengths

def compare_cesm_scores(cesm:CESModel, actuals:set, causes:list, E:Symbol, stability:list, num_simulations:int = NUM_SIMULATIONS, plot=False):
	causal_scores = dict()
	cause_names = [c.name for c in causes]
	for s in stability:
		causal_scores[s] = list()
		scores = compute_cesm_preds(
			cesm, num_simulations, actuals, causes, E, s
		)
		for c, cs in zip(causes, scores):
			causal_scores[s].append(cs)
		plt.plot(cause_names, causal_scores[s], label="{:.1f}".format(s))
	plt.ylim(0,1)
	plt.legend()
	plt.show()
