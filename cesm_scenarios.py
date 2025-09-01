from counterfactual_effect_size_model import CESModel
from sympy.abc import A, B, C, D
from sympy import Symbol, symbols

poison, antidote, survival = symbols("poison, antidote, survival")
survival_cesm = CESModel(
	actuals = {~poison, antidote},
	exovar_probs = {poison: 0.1, antidote: 0.1},
	streq = {
		survival: antidote | (~poison)
	}
)
# compare_cesm_scores(
# 	survival_cesm,
# 	[poison, antidote],
# 	survival,
# 	[0.2, 0.5, 0.8]
# )

Win = Symbol("Win")

ql2023_exp1_cesm = CESModel(
	actuals = {A,B,C,D,Win},
	exovar_probs = {A: 0.1, B: 0.1, C: 0.9, D: 0.9},
	streq = {
		Win: (A+B+C+D >= 3)
	}
)

# compute_cesm_preds(ql2023_exp1_cesm, 100000, [A,C], Win, 0.1)
# compare_cesm_scores(ql2023_exp1_cesm, [A,C], Win, [0.1, 0.5, 0.9], 100000)

low, intermediate, high = symbols("low intermediate high")
ql2023_exp2a_cesm = CESModel(
	actuals = {low, intermediate, high, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)

# compare_cesm_scores(
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
# compare_cesm_scores(
# 	ql2023_exp2b_cesm,
# 	[low, intermediate],
# 	Win,
# 	[0.25, 0.5, 0.75]
# )

low_intermediate, intermediate_high, low_high = symbols(
	"low_intermediate intermediate_high low_high"
)
can_exp1_nonholistic = ql2023_exp2a_cesm
can_exp1_holistic = CESModel(
	actuals = {low, intermediate, high},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		low_intermediate: (low & intermediate),
		intermediate_high: (intermediate & high),
		low_high: (low & high),
		Win: (low_intermediate | intermediate_high | low_high)
	}
)

# FIXME: Debug
# compute_cesm_preds(
# 	can_exp1_holistic,
# 	10000,
# 	[low, intermediate, high, low_intermediate, intermediate_high, low_high],
# 	Win,
# 	stability=0.1
# )
# compare_cesm_scores(
# 	can_exp1_holistic,
# 	[low, intermediate, high, low_intermediate, intermediate_high, low_high],
# 	Win,
# 	stability=np.arange(0,1.1,0.33)
# )

purple_low, purple_high, orange = symbols("purple_low, purple_high, orange")
ql2023_exp3_two_cesm = CESModel(
	actuals = {purple_low, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
# compare_cesm_scores(
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
# compare_cesm_scores(
# 	ql2023_exp3_three_cesm,
# 	[purple_low, purple_high, orange],
# 	Win,
# 	[0.2, 0.5, 0.8]
# )
