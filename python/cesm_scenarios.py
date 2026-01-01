from counterfactual_effect_size_model import CESModel, compute_cesm_preds, compare_cesm_preds
from sympy.abc import A, B, C, D, E, R, U
from sympy import Symbol, symbols


tadeg_example = CESModel(
	actuals = {A, B, C, E},
	exovar_probs = {A: 0.1, B: 0.2, C: 0.4, D: 0.1},
	streq = {
		E: A & (B | C) & ~D
	}
)
# compute_cesm_preds(tadeg_example, [A], E, 0.7)

m2019_conj_cesm = CESModel(
	actuals = {A, B, E},
	exovar_probs = {A: 0.1, B: 0.9},
	streq = {
		E: A & B
	}
)
# compute_cesm_preds(m2019_conj_cesm, [A, B], E, 0.7)

m2019_disj_cesm = CESModel(
	actuals = {A, B, E},
	exovar_probs = {A: 0.1, B: 0.9},
	streq = {
		E: A | B
	}
)
# compute_cesm_preds(m2019_disj_cesm, [A, B], E, 0.7)

Win = Symbol("Win")

ql2023_exp1_cesm = CESModel(
	actuals = {A,B,C,D,Win},
	exovar_probs = {A: 0.1, B: 0.1, C: 0.9, D: 0.9},
	streq = {
		Win: (A+B+C+D >= 3)
	}
)

# compute_cesm_preds(ql2023_exp1_cesm, [A,C], Win, 0.1)
# compare_cesm_preds(ql2023_exp1_cesm, [A,C], Win, [0.1, 0.5, 0.9], 100000)

low, intermediate, high = symbols("low intermediate high")
ql2023_exp2a_cesm = CESModel(
	actuals = {low, intermediate, high, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)
# compute_cesm_preds(ql2023_exp2a_cesm, [low, intermediate, high], Win, 0.7)

# compare_cesm_preds(
# 	ql2023_exp2a_cesm,
# 	[low, intermediate, high],
# 	Win,
# 	[0.25, 0.5, 0.75]
# )

ql2023_exp2b_cesm = CESModel(
	actuals = {low, intermediate, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)
# compute_cesm_preds(ql2023_exp2b_cesm, [low, intermediate], Win, 0.7)
# compare_cesm_preds(
# 	ql2023_exp2b_cesm,
# 	[low, intermediate],
# 	Win,
# 	[0.25, 0.5, 0.75]
# )

purple_low, purple_high, orange = symbols("purple_low, purple_high, orange")
ql2023_exp3_two_cesm = CESModel(
	actuals = {purple_low, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
# compute_cesm_preds(ql2023_exp3_two_cesm, [purple_low, orange], Win, 0.7)
# compare_cesm_preds(
# 	ql2023_exp3_two_cesm,
# 	[purple_low, orange],
# 	Win,
# 	[0.2, 0.5, 0.8]
# )

ql2023_exp3_three_cesm = CESModel(
	actuals = {purple_low, purple_high, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
# compute_cesm_preds(ql2023_exp3_three_cesm, [purple_low, purple_high, orange], Win, 0.7)
# compare_cesm_preds(
# 	ql2023_exp3_three_cesm,
# 	[purple_low, purple_high, orange],
# 	Win,
# 	[0.2, 0.5, 0.8]
# )

top, left, right,  = symbols("top, left, right")
ql2023_exp4_cesm = []
for actuals in [{top, left, right, Win}, {top, left, Win}]:
	for ptop in [0.1, 0.9]:
		for pright in [0.1, 0.9]:
			ql2023_exp4_cesm.append(
				CESModel(
					actuals = actuals,
					exovar_probs = {top: ptop, left: 0.5, right: pright},
					streq = {
						Win: (top & left) | (~top & right)
					}
				)
			)
# for idx, model in enumerate(ql2023_exp4_cesm):
# 	print(compute_cesm_preds(model, [top], Win, 0.7))

gi2020_xor_cesm = [
	CESModel(
		actuals = {A, B, E},
		exovar_probs = {A: 0.8, B: 0.2},
		streq = {
			E: (A & ~B) | (~A & B)
		}
	),
	CESModel(
		actuals = set(),
		exovar_probs = {A: 0.8, B: 0.2},
		streq = {
			E: (A & ~B) | (~A & B)
		}
	)
]
# compute_cesm_preds(gi2020_xor_cesm[0], [A, B], E, 0.7)
# compute_cesm_preds(gi2020_xor_cesm[1], [A, B], E, 0.7)

oneill2025_dp_cesm = CESModel(
	actuals = {E, U, C, D},
	exovar_probs = {C:0.5, U: 0.1, D: 0.5},
	streq = {
		E: C & ~R,
		R: U & ~D
	}
)
# compute_cesm_preds(oneill2025_dp_cesm, [C, D], E, 0.7)

confounded_cesm = CESModel(
	actuals = {A, C, E},
	exovar_probs = {A: 0.9},
	streq = {
		E: A,
		C: A
	}
)
# compute_cesm_preds(confounded_cesm, [C], E, 0.7)

nonconfounded_cesm = CESModel(
	actuals = {A, C, E},
	exovar_probs = {A: 0.3, C: 0.6},
	streq = {
		E: A & C
	}
)
# compute_cesm_preds(nonconfounded_cesm, [C], E, 0.7)
# compute_cesm_preds(nonconfounded_cesm, [E], C, 0.7)

intconf_one_cesm = CESModel(
	actuals = {A, C, E},
	exovar_probs = {A: 0.5, B: 0.5},
	streq = {
		E: A | C,
		C: A | B
	}
)
# compute_cesm_preds(intconf_one_cesm, [A, C], E, 0.7)

intconf_two_cesm = CESModel(
	actuals = {A, B, C, E},
	exovar_probs = {A: 0.5, B: 0.5},
	streq = {
		E: A | C,
		C: A | B
	}
)
# compute_cesm_preds(intconf_two_cesm, [A, C], E, 0.7)
