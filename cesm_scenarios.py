from counterfactual_effect_size_model import StrEq, CESModel
import numpy.random as r
import numpy as np


STABILITY = 0.73
# STABILITY = 0

def compute_sampling_propensity(event:str, prob:float, actual:set):
	"""
	According to the discussion on Extended Structural Model
	from the section "A formal model of counterfactual sampling".
	"""
	delta = (event in actual)
	return STABILITY*delta + (1-STABILITY)*prob



def make_survival_cesm(base_prob):
	def survival(poison, antidote, **kwargs):
		return np.logical_or(1-poison, antidote).astype(poison.dtype)

	def poison(num_simulations, actuals:set, **kwargs):
		sp = compute_sampling_propensity("poison", base_prob["poison"], actuals)
		return r.binomial(1, size=num_simulations, p=sp)

	def antidote(num_simulations, actuals:set, **kwargs):
		sp = compute_sampling_propensity("antidote", base_prob["antidote"], actuals)
		return r.binomial(1, size=num_simulations, p=sp)

	return CESModel(
		exovars = {"poison", "antidote"},
		endovars = {"survival"},
		base_prob = base_prob,
		streq = {
			"poison": poison,
			"antidote": antidote,
			"survival": StrEq({"poison", "antidote"}, survival)
		}
	)


def make_cesm_study1():
	base_prob = {"first":0.1, "second": 0.1, "third": 0.9, "fourth": 0.9}
	def draw(event, num_simulations, actuals:set, p:float):
		sp = compute_sampling_propensity(event, p, actuals)
		return r.binomial(1, size=num_simulations, p=sp)

	def first(num_simulations, actuals:set, **kwargs):
		return draw("first", num_simulations, actuals, base_prob["first"])
	def second(num_simulations, actuals:set, **kwargs):
		return draw("second", num_simulations, actuals, base_prob["second"])
	def third(num_simulations, actuals:set, **kwargs):
		return draw("third", num_simulations, actuals, base_prob["third"])
	def fourth(num_simulations, actuals:set, **kwargs):
		return draw("fourth", num_simulations, actuals, base_prob["fourth"])

	def win(first, second, third, fourth, **kwargs):
		return ((first + second + third + fourth) >= 3).astype(first.dtype)

	return CESModel(
		exovars = {"first", "second", "third", "fourth"},
		endovars = {"win"},
		base_prob = base_prob,
		streq = {
			"first": first,
			"second": second,
			"third": third,
			"fourth": fourth,
			"win": StrEq({"first", "second", "third", "fourth"}, win)
		}
	)

def make_cesm_study2():
	base_prob = {"low":0.05, "intermediate": 0.5, "high": 0.95}
	def draw(event, num_simulations, actuals:set, p:float):
		sp = compute_sampling_propensity(event, p, actuals)
		return r.binomial(1, size=num_simulations, p=sp)

	def low(num_simulations, actuals:set, **kwargs):
		return draw("low", num_simulations, actuals, base_prob["low"])
	def intermediate(num_simulations, actuals:set, **kwargs):
		return draw("intermediate", num_simulations, actuals, base_prob["intermediate"])
	def high(num_simulations, actuals:set, **kwargs):
		return draw("high", num_simulations, actuals, base_prob["high"])

	def win(low, intermediate, high):
		return ((low + intermediate + high) >= 2).astype(low.dtype)

	return CESModel(
		exovars={"low", "intermediate", "high"},
		endovars={"win"},
		base_prob=base_prob,
		streq={
			"low": low,
			"intermediate": intermediate,
			"high": high,
			"win": StrEq({"low", "intermediate", "high"}, win)
		}
	)
