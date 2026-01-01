from sympy import Symbol, symbols, And, Or, Not, Eq
from numpy.random import binomial
from numpy import mean, std, abs

STABILITY=0.73
NUM_SAMPLES=100000

Poison, Antidote, Survival = symbols("Poison, Antidote, Survival")

def compute_sampling_propensity(event:Symbol, prob:float, actual:set):
	"""
	According to the discussion on Extended Structural Model
	from the section "A formal model of counterfactual sampling".
	"""
	delta = (event in actual)
	return STABILITY*delta + (1-STABILITY)*prob

def compute_causal_effect(event, counterfactual_event, cause, counterfactual_cause):
	"Compute delta-E / delta-C"
	return (counterfactual_event - event) / (counterfactual_cause - cause)

def simulate_analogous_scenario(scenario, event_is_cause):
	prob = {Poison: 0.1, Antidote:0.5}
	if scenario == "survival": actual = {Not(Poison), Antidote}
	elif scenario == "death": actual = {Poison, Not(Antidote)}
	sp = {
		Poison: compute_sampling_propensity(Poison, prob[Poison], actual),
		Antidote: compute_sampling_propensity(Antidote, prob[Antidote], actual),
	}
	poison_samples = binomial(1, size=NUM_SAMPLES, p=sp[Poison])
	antidote_samples = binomial(1, size=NUM_SAMPLES, p=sp[Antidote])

	# survival = not(poison) or antidote
	survival_samples = (1-poison_samples) | antidote_samples
	death_samples = 1-survival_samples
	outcome = survival_samples

	poison_sd = std(poison_samples)
	antidote_sd = std(antidote_samples)
	outcome_sd = std(outcome)

	if event_is_cause == Poison:
		poison_twin_samples = 1 - poison_samples
		counterfactual_samples = (1 - poison_twin_samples) | antidote_samples
		causal_effect = compute_causal_effect(
			survival_samples, counterfactual_samples, poison_samples, poison_twin_samples
		)
		cause_sd = poison_sd
	elif event_is_cause == Antidote:
		antidote_twin_samples = 1 - antidote_samples
		counterfactual_samples = (1 - poison_samples) | antidote_twin_samples
		causal_effect = compute_causal_effect(
			survival_samples, counterfactual_samples, antidote_samples, antidote_twin_samples
		)
		cause_sd = antidote_sd

	causal_effect = abs(causal_effect)
	return mean(causal_effect) * outcome_sd / cause_sd

if __name__ == "__main__":
	print("Survival Scenario")
	print("\tPoison (or its lack) is a cause:", simulate_analogous_scenario("survival", Poison))
	print("\tAntidote (or its lack) is a cause:", simulate_analogous_scenario("survival", Antidote))
	print("Death Scenario")
	print("\tPoison (or its lack) is a cause:", simulate_analogous_scenario("death", Poison))
	print("\tAntidote (or its lack) is a cause:", simulate_analogous_scenario("death", Antidote))
