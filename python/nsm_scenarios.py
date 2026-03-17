from necessity_sufficiency_model import NSModel, compute_nsm_preds, compare_nsm_preds
from sympy.abc import A, B, C, D, E, R, U
from sympy import Symbol, symbols

Win = Symbol("Win")

ql2023_exp1_nsm = NSModel(
	actuals = {A,B,C,D,Win},
	exovar_probs = {A: 0.1, B: 0.1, C: 0.9, D: 0.9},
	streq = {
		Win: (A+B+C+D >= 3)
	}
)

# compute_nsm_preds(ql2023_exp1_nsm, [A,C], Win)

low, intermediate, high = symbols("low intermediate high")
ql2023_exp2a_nsm = NSModel(
	actuals = {low, intermediate, high, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)

# compute_nsm_preds(ql2023_exp2a_nsm, [low, intermediate, high], Win, 0.15)

ql2023_exp2b_nsm = NSModel(
	actuals = {low, intermediate, Win},
	exovar_probs = {low: 0.05, intermediate: 0.5, high: 0.95},
	streq = {
		Win: (low + intermediate + high >= 2)
	}
)

# compute_nsm_preds(ql2023_exp2b_nsm, [low, intermediate], Win, 0.15)

purple_low, purple_high, orange = symbols("purple_low, purple_high, orange")
ql2023_exp3_two_nsm = NSModel(
	actuals = {purple_low, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
# compute_nsm_preds(ql2023_exp3_two_nsm, [purple_low, orange], Win, 0.15)

ql2023_exp3_three_nsm = NSModel(
	actuals = {purple_low, purple_high, orange, Win},
	exovar_probs = {purple_low: 0.05, purple_high: 0.9, orange: 0.95},
	streq = {
		Win: ((purple_low | purple_high) & orange)
	}
)
# compute_nsm_preds(ql2023_exp3_three_nsm, [purple_low, purple_high, orange], Win, 0.15)
