from counterfactual_effect_size_model import StrEq, CESModel
import numpy.random as r
import numpy as np


STABILITY = 0.73

def compute_sampling_propensity(event:str, prob:float, actual:set, stability:float=None):
	"""
	According to the discussion on Extended Structural Model
	from the section "A formal model of counterfactual sampling".
	"""
	if stability is None: stability = STABILITY
	delta = (event in actual)
	return stability*delta + (1-stability)*prob



def make_survival_cesm(base_prob):
	def survival(poison, antidote, **kwargs):
		return np.logical_or(1-poison, antidote).astype(poison.dtype)

	def poison(num_simulations, actuals:set, stability=None, **kwargs):
		sp = compute_sampling_propensity(
			"poison", base_prob["poison"], actuals, stability=stability
		)
		return r.binomial(1, size=num_simulations, p=sp)

	def antidote(num_simulations, actuals:set, stability=None, **kwargs):
		sp = compute_sampling_propensity(
			"antidote", base_prob["antidote"], actuals, stability=stability
		)
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
	def draw(event, num_simulations, actuals:set, p:float, stability:float):
		sp = compute_sampling_propensity(event, p, actuals, stability=stability)
		return r.binomial(1, size=num_simulations, p=sp)

	def first(num_simulations, actuals:set, **kwargs):
		return draw("first", num_simulations, actuals, base_prob["first"], kwargs["stability"])
	def second(num_simulations, actuals:set, **kwargs):
		return draw("second", num_simulations, actuals, base_prob["second"], kwargs["stability"])
	def third(num_simulations, actuals:set, **kwargs):
		return draw("third", num_simulations, actuals, base_prob["third"], kwargs["stability"])
	def fourth(num_simulations, actuals:set, **kwargs):
		return draw("fourth", num_simulations, actuals, base_prob["fourth"], kwargs["stability"])

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
cesm_study1 = make_cesm_study1()

def make_cesm_study2():
	base_prob = {"low":0.05, "intermediate": 0.5, "high": 0.95}
	def draw(event, num_simulations, actuals:set, p:float, stability:float):
		sp = compute_sampling_propensity(event, p, actuals, stability=stability)
		return r.binomial(1, size=num_simulations, p=sp)

	def low(num_simulations, actuals:set, **kwargs):
		return draw(
			"low", num_simulations, actuals, base_prob["low"],
			stability=kwargs["stability"]
		)
	def intermediate(num_simulations, actuals:set, **kwargs):
		return draw(
			"intermediate", num_simulations, actuals, base_prob["intermediate"],
			stability=kwargs["stability"]
		)
	def high(num_simulations, actuals:set, **kwargs):
		return draw(
			"high", num_simulations, actuals, base_prob["high"],
			stability=kwargs["stability"]
		)

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
cesm_study2 = make_cesm_study2()


def make_cesm_study3_three():
	base_prob = {"purple_low":0.05, "purple_high": 0.9, "orange": 0.95}
	def draw(event, num_simulations, actuals:set, p:float, stability:float):
		sp = compute_sampling_propensity(event, p, actuals, stability=stability)
		return r.binomial(1, size=num_simulations, p=sp)

	def purple_low(num_simulations, actuals:set, **kwargs):
		return draw(
			"purple_low", num_simulations, actuals, base_prob["purple_low"],
			stability=kwargs["stability"]
		)
	def purple_high(num_simulations, actuals:set, **kwargs):
		return draw(
			"purple_high", num_simulations, actuals, base_prob["purple_high"],
			stability=kwargs["stability"]
		)
	def orange(num_simulations, actuals:set, **kwargs):
		return draw(
			"orange", num_simulations, actuals, base_prob["orange"],
			stability=kwargs["stability"]
		)

	def win(purple_low, purple_high, orange):
		return ((np.logical_or(purple_low, purple_high)) + orange >= 2).astype(purple_low.dtype)

	return CESModel(
		exovars={"purple_low", "purple_high", "orange"},
		endovars={"win"},
		base_prob=base_prob,
		streq={
			"purple_low": purple_low,
			"purple_high": purple_high,
			"orange": orange,
			"win": StrEq({"purple_low", "purple_high", "orange"}, win)
		}
	)
cesm_study3_three = make_cesm_study3_three()
