from counterfactual_effect_size_model import CESModel
from sympy.abc import A, B, C, D
from sympy import Symbol, symbols

poison, antidote, survival = symbols("poison, antidote, survival")
survival_cesm = CESModel(
	exovar_probs = {poison: 0.1, antidote: 0.1},
	streq = {
		survival: antidote | (~poison)
	}
)
# compare_cesm_scores(
# 	survival_cesm,
# 	{~poison, antidote},
# 	[poison, antidote],
# 	survival,
# 	[0.2, 0.5, 0.8]
# )

Win = Symbol("Win")

ql2023_exp1_cesm = CESModel(
	exovar_probs = {A: 0.1, B: 0.1, C: 0.9, D: 0.9},
	streq = {
		Win: (A+B+C+D >= 3)
	}
)

# compute_cesm_preds(ql2023_exp1_cesm, 100000, {A,B,C,D,Win}, [A,C], Win, 0.1)
# compare_cesm_scores(ql2023_exp1_cesm, {A,B,C,D,Win}, [A,C], Win, [0.1, 0.5, 0.9], 100000)

low, intermediate, high = symbols("low intermediate high")
ql2023_exp2_cesm = CESModel(
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)

# compare_cesm_scores(
# 	ql2023_exp2_cesm,
# 	{low, intermediate, high, Win},
# 	[low, intermediate, high],
# 	Win,
# 	[0.25, 0.5, 0.75]
# )
# compare_cesm_scores(
# 	ql2023_exp2_cesm,
# 	{low, intermediate, Win},
# 	[low, intermediate],
# 	Win,
# 	[0.25, 0.5, 0.75]
# )

low_intermediate, intermediate_high, low_high = symbols(
	"low_intermediate intermediate_high low_high"
)
can_exp1_nonholistic = ql2023_exp2_cesm
can_exp1_holistic = CESModel(
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
# 	{low, intermediate, high},
# 	[low, intermediate, high, low_intermediate, intermediate_high, low_high],
# 	Win,
# 	stability=0.1
# )
# compare_cesm_scores(
# 	can_exp1_holistic,
# 	{low, intermediate, high},
# 	[low, intermediate, high, low_intermediate, intermediate_high, low_high],
# 	Win,
# 	stability=np.arange(0,1.1,0.33)
# )

purple_low, purple_high, orange = symbols("purple_low, purple_high, orange")
ql2023_exp3_cesm = CESModel(
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
# compare_cesm_scores(
# 	ql2023_exp3_cesm,
# 	{purple_low, orange, Win},
# 	[purple_low, orange],
# 	Win,
# 	[0.2, 0.5, 0.8]
# )
# compare_cesm_scores(
# 	ql2023_exp3_cesm,
# 	{purple_low, purple_high, orange, Win},
# 	[purple_low, purple_high, orange],
# 	Win,
# 	[0.2, 0.5, 0.8]
# )
