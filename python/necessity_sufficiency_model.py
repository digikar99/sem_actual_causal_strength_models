import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt
from sympy import Symbol
from structural_equation_model import SEModel, compute_sem_preds
from factual_difference_making import FDMModel
from sys import platform
from pprint import pp

NUM_SIMULATIONS=500000
EPS=1e-7

np.set_printoptions(threshold=10)

if platform == "darwin":
	import matplotlib
	matplotlib.use("qtagg")

class NSModel(SEModel):
	"""
	Encodes the actual causal scenario.

	- actuals: a set of symbols
	- exovar_probs: a dict mapping a symbol representing an exogeneous variable
		to its probability of occurrence
	- streq: a dict mapping each endogeneous variable to the RHS of the structural equation

	See nsm_scenarios.py for examples.
	"""
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
		return f"NSModel({space}actuals={self.actuals},{space}exovars={self.exovars},{space}exovar_probs={self.exovar_probs},{space}endovars={self.endovars},{space}streq={_streq}\n)"


def as_nsmodel(model):
	if type(model) == FDMModel:
		return NSModel(
			actuals = model.literals,
			streq = model._streq,
			exovar_probs = model.relative_normality
		)
	else:
		raise Exception("as_nsmodel not implemented for", type(model))

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

def compute_nsm_preds(
		nsm:NSModel,
		candidate_causes:list,
		effect:Symbol,
		stability:float = 0.73,
		num_simulations:int = NUM_SIMULATIONS
):
	"""
	Takes in the following arguments and returns a list of CES causal judgments for each of the candidate causes:

	- nsm: an instance of NSModel
	- candidate_causes: a list of symbols representing the causes of which judgments are to be computed
	- effect: a symbol towards which causal judgment is to be computed
	- stability: the stability parameter of CES Model, default value 0.73
	- num_simulations: an integer, default value 500000

	"""

	necessity_samples = dict()
	for var in nsm.exovar_probs:
		necessity_samples[var] = np.array([(var in nsm.actuals)], dtype="int8")

	# int8 is the appropriate data type for ces, because during the sum of the delta below,
	#   spurious positive and negative effects can then sum up to zero.
	# uint8 or bool would not allow such summing up the deltas to zero.
	exovar_samples = dict()
	for var in nsm.exovars:
		exovar_samples[var] = draw(
			var, num_simulations, nsm.actuals, nsm.exovar_probs[var],
			stability
		)

	initial_preds = compute_sem_preds(nsm, exovar_samples)

	E = effect
	strengths = []

	for C in candidate_causes:

		# Quillien & Lucas (2023), supplementary information:
		#   necessity is 1 iff C was necessary for E in the actual world
		# Icard et al. (2017): In our specific case, we assume this involves setting C to 0,
		#   holding fixed A = 1, and checking whether this is enough to make E = 0.
		necessity_counterfactual = necessity_samples.copy()
		necessity_counterfactual[C] = np.array([0], dtype="int8") # assume binary variables
		necessity_preds = compute_sem_preds(nsm, necessity_counterfactual)
		necessity = np.all(necessity_preds[E] == 0)


		sufficiency_counterfactuals = exovar_samples.copy()
		sufficiency_counterfactuals[C] = 1 - initial_preds[C] # assume binary variables
		sufficiency_preds = compute_sem_preds(nsm, sufficiency_counterfactuals)

		# sufficiency is P(E=1|do(C), C=0, E=0)
		smask = (initial_preds[C] == 0) * (initial_preds[E] == 0)
		sufficiency = np.mean(sufficiency_preds[E], where=smask)

		sp = compute_sampling_propensity(
			C, nsm.exovar_probs[C], nsm.actuals, stability=stability
		)
		print(C, necessity, sp, np.sum(smask))
		strength = (1 - sp) * necessity + sp * sufficiency

		strength = abs(strength)
		strengths.append(strength)
	return strengths


def compare_causal_scores(nsm:NSModel, actuals:set, causes:list, E:str, stability:list, num_simulations:int = NUM_SIMULATIONS, plot=False):
	causal_scores = dict()
	for s in stability:
		causal_scores[s] = list()
		for c in causes:
			cs = causal_score(nsm, actuals, c, E, num_simulations, stability=s)
			causal_scores[s].append(cs)
		plt.plot(causes, causal_scores[s], label="{:.1f}".format(s))
	plt.ylim(0,1)
	plt.legend()
	plt.show()
