import numpy as np
import pprint
from dataclasses import dataclass

NUM_SIMULATIONS=500000
EPS=1e-7

np.set_printoptions(threshold=10)

@dataclass
class StrEq:
	deps: set
	eqn: callable # function

@dataclass
class CESModel:
	exovars: set
	endovars: set
	base_prob: dict
	streq: dict
	# def __init__(self, exovars:set, endovars:set, streq:dict):
	# 	self.exovars  = exovars  # exogeneous variables
	# 	self.endovars = endovars # endogeneous variables
	# 	self.streq = streq


def simulate(cesm:CESModel, actuals:set, num_simulations:int, C, stability:float):
	results = dict()

	def _simulate(var):
		if var in cesm.exovars:
			result = cesm.streq[var](num_simulations, actuals, stability=stability, **results)
		else:
			streq = cesm.streq[var]
			deps = streq.deps
			for v in deps:
				if v not in results: _simulate(v)
			if var not in results: result = streq.eqn(**results)
			else: return results[var]
		results[var] = result
		return result

	for var in cesm.streq: _simulate(var)
	simulation_results = results

	# Repeat
	results = dict()
	# for var in cesm.streq: _simulate(var)
	# results[C] = np.logical_and(simulation_results[E] == 0,
	# 							simulation_results[C] == 0)
	# results[C] = 1 - results[C] #
	# for var in cesm.endovars: results.pop(var)
	# print(results)
	results[C] = 1 - simulation_results[C]
	for var in cesm.exovars: results[var] = simulation_results[var]

	def _simulate_counterfactuals(var):
		if var in cesm.exovars:
			return results[var]
		else:
			streq = cesm.streq[var]
			deps = streq.deps
			for v in deps:
				if v not in results: _simulate(v)
			result = streq.eqn(**results)
		results[var] = result
		return result

	for var in cesm.streq: _simulate_counterfactuals(var)
	counterfactual_results = results

	return simulation_results, counterfactual_results



def causal_score(cesm:CESModel, actuals:set, C:str, E:str, num_simulations:int = NUM_SIMULATIONS, stability:float = None):
	"Computes the causal score k_{C \\to E} of C on E."
	simulation_results, counterfactual_results = simulate(
		cesm, actuals, num_simulations, C, stability
	)
	# pprint.pp(simulation_results)
	# pprint.pp(counterfactual_results)
	# selection = np.logical_and(simulation_results[E]==0, simulation_results[C]==0)
	deltaC = np.abs(counterfactual_results[C] - simulation_results[C])
	deltaE = np.abs(counterfactual_results[E] - simulation_results[E])
	stdC = np.std(simulation_results[C])
	stdE = np.std(simulation_results[E])
	# score = np.sum(deltaE / deltaC)/num_simulations * stdC / (stdE+EPS)
	score = np.corrcoef(simulation_results[C], simulation_results[E])
	# /num_simulations * stdC / (stdE+EPS)
	return score
