import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt
from sympy import Symbol
from structural_equation_model import ActualSEModel, compute_sem_preds
from factual_difference_making import FDMModel
from sys import platform
from pprint import pp

NUM_SIMULATIONS=500000

np.set_printoptions(threshold=10)
if platform == "darwin":
	import matplotlib
	matplotlib.use("qtagg")

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
		model:ActualSEModel,
		candidate_causes:list,
		effect:Symbol,
		stability:float = 0.73,
		num_simulations:int = NUM_SIMULATIONS
):
	"""
	Takes in the following arguments and returns a list of CES causal judgments for each of the candidate causes:

	- model: an instance of ActualSEModel
	- candidate_causes: a list of symbols representing the causes of which judgments are to be computed
	- effect: a symbol towards which causal judgment is to be computed
	- stability: the stability parameter of CES Model, default value 0.73
	- num_simulations: an integer, default value 500000

	"""
	# int8 is the appropriate data type, because during the sum of the delta below,
	#   spurious positive and negative effects can then sum up to zero.
	# uint8 or bool would not allow such summing up the deltas to zero.
	exovar_samples = dict()
	for var in model.exovars:
		exovar_samples[var] = draw(
			var, num_simulations, model.actuals, model.exovar_probs[var],
			stability
		)

	initial_preds = compute_sem_preds(model, exovar_samples)

	strengths = []
	for var in candidate_causes:
		new_exovar_samples = exovar_samples.copy()
		new_exovar_samples[var] = 1 - initial_preds[var] # assume binary variables
		# counterfactual predictions
		new_preds = compute_sem_preds(model, new_exovar_samples)
		delta_var = initial_preds[var] - new_preds[var]
		delta_eff = initial_preds[effect] - new_preds[effect]
		std_var = np.std(initial_preds[var])
		std_eff = np.std(initial_preds[effect])
		strength = np.mean(
			delta_eff / delta_var * std_var / std_eff
		)
		# strength = np.sum(delta_eff / delta_var) * std_var / std_eff / num_simulations
		# strength = np.corrcoef(initial_preds[var], initial_preds[effect])[0,1]
		strength = abs(strength)
		strengths.append(strength)
	return strengths

def compute_nsm_preds(
		model:ActualSEModel,
		candidate_causes:list,
		effect:Symbol,
		stability:float = 0.73,
		num_simulations:int = NUM_SIMULATIONS
):
	"""
	Takes in the following arguments and returns a list of CES causal judgments for each of the candidate causes:

	- model: an instance of ActualSEModel
	- candidate_causes: a list of symbols representing the causes of which judgments are to be computed
	- effect: a symbol towards which causal judgment is to be computed
	- stability: the stability parameter of CES Model, default value 0.73
	- num_simulations: an integer, default value 500000

	"""

	necessity_samples = dict()
	for var in model.exovar_probs:
		necessity_samples[var] = np.array([(var in model.actuals)], dtype="int8")

	# int8 is the appropriate data type for ces, because during the sum of the delta below,
	#   spurious positive and negative effects can then sum up to zero.
	# uint8 or bool would not allow such summing up the deltas to zero.
	exovar_samples = dict()
	for var in model.exovars:
		exovar_samples[var] = draw(
			var, num_simulations, model.actuals, model.exovar_probs[var],
			stability
		)

	initial_preds = compute_sem_preds(model, exovar_samples)

	E = effect
	strengths = []

	for C in candidate_causes:

		# Quillien & Lucas (2023), supplementary information:
		#   necessity is 1 iff C was necessary for E in the actual world
		# Icard et al. (2017): In our specific case, we assume this involves setting C to 0,
		#   holding fixed A = 1, and checking whether this is enough to make E = 0.
		necessity_counterfactual = necessity_samples.copy()
		necessity_counterfactual[C] = np.array([0], dtype="int8") # assume binary variables
		necessity_preds = compute_sem_preds(model, necessity_counterfactual)
		necessity = np.all(necessity_preds[E] == 0)


		sufficiency_counterfactuals = exovar_samples.copy()
		sufficiency_counterfactuals[C] = 1 - initial_preds[C] # assume binary variables
		sufficiency_preds = compute_sem_preds(model, sufficiency_counterfactuals)

		# sufficiency is P(E=1|do(C), C=0, E=0)
		smask = (initial_preds[C] == 0) * (initial_preds[E] == 0)
		sufficiency = np.mean(sufficiency_preds[E], where=smask)

		sp = compute_sampling_propensity(
			C, model.exovar_probs[C], model.actuals, stability=stability
		)
		# print(C, necessity, sp, np.sum(smask))
		strength = (1 - sp) * necessity + sp * sufficiency

		strength = abs(strength)
		strengths.append(strength)
	return strengths

def ensure_method(method):
	if method == "cesm" or method == "CESM":
		method = ("CESM", compute_cesm_preds)
	elif method == "nsm" or method == "NSM":
		method = ("NSM", compute_nsm_preds)
	else:
		method = (method.__name__, method)
	return method


def compare_stability(method, model:ActualSEModel, causes:list, effect:Symbol, stability:list, num_simulations:int = NUM_SIMULATIONS, plot=False):
	"""
	Takes in the following arguments and returns a list of CES causal judgments for each of the candidate causes:

	- model: an instance of ActualSEModel
	- causes: a list of symbols representing the causes of which judgments are to be computed
	- effect: a symbol towards which causal judgment is to be computed
	- stability: a list of stability parameters for which the causal judgments are to be computed or plotted
	- num_simulations: an integer, default value 500000
	- plot: whether the judgments should be plotted on a graph; default value False
	"""
	causal_scores = dict()
	cause_names = [c.name for c in causes]
	method = ensure_method(method)[1]
	for s in stability:
		causal_scores[s] = list()
		scores = method(
			model, causes, effect, s, num_simulations
		)
		for c, cs in zip(causes, scores):
			causal_scores[s].append(cs)
		if plot:
			plt.plot(cause_names, causal_scores[s], label="{:.1f}".format(s))
		causal_scores_list = causal_scores[s]
		causal_scores[s] = dict()
		for c, cs in zip(causes, scores):
			causal_scores[s][c] = cs
	if plot:
		plt.ylim(0,1)
		plt.legend()
		plt.show()
	return causal_scores

def compare_preds(methods, model, causes, effect, stability):
	methods = list(map(ensure_method, methods))
	print(model)
	print("Respective causal strengths towards", effect, "\n  of the causes", causes, "are:")
	for name, m in methods:
		print(" ", name, "\t:", end=" ")
		for score in m(model, causes, effect, stability):
			print("{:.2f}".format(score), end=", ")
		print()
	print()
