from structural_equation_model import ActualSEModel
from sem_actual_causal_strength_models import compute_cesm_preds, compute_nsm_preds, compare_stability, compare_preds
from sympy.abc import A, B, C, D, E, R, U
from sympy import Symbol, symbols


tadeg_example = ActualSEModel(
	actuals = {A, B, C, E},
	exovar_probs = {A: 0.1, B: 0.2, C: 0.4, D: 0.1},
	streq = {
		E: A & (B | C) & ~D
	}
)
print(tadeg_example)
print("CESM:", compute_cesm_preds(tadeg_example, [A], E, 0.7))

m2019_conj = ActualSEModel(
	actuals = {A, B, E},
	exovar_probs = {A: 0.1, B: 0.9},
	streq = {
		E: A & B
	}
)
# compute_cesm_preds(m2019_conj, [A, B], E, 0.7)

m2019_disj = ActualSEModel(
	actuals = {A, B, E},
	exovar_probs = {A: 0.1, B: 0.9},
	streq = {
		E: A | B
	}
)
# compute_cesm_preds(m2019_disj, [A, B], E, 0.7)

Win = Symbol("Win")

ql2023_exp1 = ActualSEModel(
	actuals = {A,B,C,D,Win},
	exovar_probs = {A: 0.1, B: 0.1, C: 0.9, D: 0.9},
	streq = {
		Win: (A+B+C+D >= 3)
	}
)

print(ql2023_exp1)
print("CESM:", compute_cesm_preds(ql2023_exp1, [A,C], Win, 0.7))
compare_stability("cesm", ql2023_exp1, [A,C], Win, [0.1, 0.5, 0.9], 100000, plot=False)
print("NSM", compute_nsm_preds(ql2023_exp1, [A,C], Win, 0.15))

low, intermediate, high = symbols("low intermediate high")
ql2023_exp2a = ActualSEModel(
	actuals = {low, intermediate, high, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)
compare_preds(["cesm", "nsm"], ql2023_exp2a, [low, intermediate, high], Win, 0.73)

ql2023_exp2b = ActualSEModel(
	actuals = {low, intermediate, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)

compare_preds(["cesm", "nsm"], ql2023_exp2b, [low, intermediate], Win, 0.73)

purple_low, purple_high, orange = symbols("purple_low, purple_high, orange")
ql2023_exp3_two = ActualSEModel(
	actuals = {purple_low, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
compare_preds(["cesm", "nsm"], ql2023_exp3_two, [purple_low, orange], Win, 0.73)

ql2023_exp3_three = ActualSEModel(
	actuals = {purple_low, purple_high, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
compare_preds(["cesm", "nsm"], ql2023_exp3_three, [purple_low, purple_high, orange], Win, 0.73)

top, left, right,  = symbols("top, left, right")
ql2023_exp4 = []
for actuals in [{top, left, right, Win}, {top, left, Win}]:
	for ptop in [0.1, 0.9]:
		for pright in [0.1, 0.9]:
			ql2023_exp4.append(
				ActualSEModel(
					actuals = actuals,
					exovar_probs = {top: ptop, left: 0.5, right: pright},
					streq = {
						Win: (top & left) | (~top & right)
					}
				)
			)

for idx, model in enumerate(ql2023_exp4):
	compare_preds(["CESM", "NSM"], model, [top], Win, 0.7)

# Gerstenberg & Icard (2020): Expectations Affect Physical Causation Judgments
gi2020_xor = [
	ActualSEModel(
		actuals = {A, B, E},
		exovar_probs = {A: 0.8, B: 0.2},
		streq = {
			E: (A & ~B) | (~A & B)
		}
	),
	ActualSEModel(
		actuals = set(),
		exovar_probs = {A: 0.8, B: 0.2},
		streq = {
			E: (A & ~B) | (~A & B)
		}
	)
]
compare_preds(["CESM",],  gi2020_xor[0], [A, B], E, 0.7)
compare_preds(["CESM",],  gi2020_xor[1], [A, B], E, 0.7)

oneill2025_dp = ActualSEModel(
	actuals = {E, U, C, D},
	exovar_probs = {C:0.5, U: 0.1, D: 0.5},
	streq = {
		E: C & ~R,
		R: U & ~D
	}
)
compare_preds(["CESM"], oneill2025_dp, [C, D], E, 0.7)

confounded = ActualSEModel(
	actuals = {A, C, E},
	exovar_probs = {A: 0.9},
	streq = {
		E: A,
		C: A
	}
)
compare_preds(["CESM"], confounded, [C], E, 0.7)

nonconfounded = ActualSEModel(
	actuals = {A, C, E},
	exovar_probs = {A: 0.3, C: 0.6},
	streq = {
		E: A & C
	}
)
compare_preds(["CESM"], nonconfounded, [C], E, 0.7)

intconf_one = ActualSEModel(
	actuals = {A, C, E},
	exovar_probs = {A: 0.5, B: 0.5},
	streq = {
		E: A | C,
		C: A | B
	}
)
compare_preds(["CESM"], intconf_one, [A, C], E, 0.7)

intconf_two = ActualSEModel(
	actuals = {A, B, C, E},
	exovar_probs = {A: 0.5, B: 0.5},
	streq = {
		E: A | C,
		C: A | B
	}
)
compare_preds(["CESM"], intconf_two, [A, C], E, 0.7)
