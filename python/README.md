
This repository (directory) was originally planned to house a python implementation of [Factual Difference-Making](https://www.mario-guenther.com/_files/ugd/70b9dd_60f7073085db46c8bb9c23aae03b9e4e.pdf). This lies at:

- [./factual\_difference\_making.py](./factual_difference_making.py) with
    - some scenarios encoded in [./fdm\_scenarios.py](./fdm_scenarios.py) and tests in [./fdm\_tests.py](./fdm_tests.py). 

But the repository (directory) has since expanded to also contain:

- [structural\_equation\_model.py](./structural_equation_model.py)): a basic implementation of structural equations
- [counterfactual\_effect\_size\_model.py](./counterfactual_effect_size_model.py): a (WIP?) implementation of the CES model of counterfactual judgments, with empirical work described [here](https://www.pure.ed.ac.uk/ws/portalfiles/portal/431176760/Counterfactuals_QUILLIEN_DOA16022023_AFV_CC_BY.pdf) and implementation described [here](https://osf.io/h42f7/files/vnh84). 
    - A number of scenarios are encoded in [cesm\_scenarios.py](./cesm_scenarios.py). Thanks to Tadeg for providing the R implementation for many of these. The R implementation of CES and NS models of causal judgments is at [tadegquillien/causal-judgment](https://github.com/tadegquillien/causal-judgment).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Setting up the programming environment](#setting-up-the-programming-environment)
    - [1. Installing python and packages](#1-installing-python-and-packages)
        - [1a. Using command line](#1a-using-command-line)
        - [1b. Using GUI](#1b-using-gui)
    - [2. Cloning repository](#2-cloning-repository)
    - [3. Check installation](#3-check-installation)
    - [4. Other tools](#4-other-tools)
- [Sympy: A Quick Tutorial](#sympy-a-quick-tutorial)
- [Demonstration of factual\_difference\_making](#demonstration-of-factual_difference_making)
- [Counterfactual Effect Size Model (CESM)](#counterfactual-effect-size-model-cesm)
    - [Example usage](#example-usage)
    - [Given scenarios](#given-scenarios)
- [References](#references)

<!-- markdown-toc end -->

### Setting up the programming environment

The program is currently developed in python. Python package dependencies are listed in [requirements.txt](./requirements.txt). 

#### 1. Installing python and packages

##### 1a. Using command line

Users familiar with terminals or command line applications should try out [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) to install python, its packages and manage its virtual environments.

```
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
micromamba create --name fdm --file requirements.txt
micromamba activate fdm
```

The benefits of micromamba over miniconda, conda, and anaconda is that micromamba is very lightweight and incredibly fast.

##### 1b. Using GUI

[Anaconda](https://www.anaconda.com/download) provides a GUI interface called Anaconda Navigator. They also provide nice documentation and the following two pages should be sufficient to set up python and a virtual environment:

- https://www.anaconda.com/docs/getting-started/getting-started
- https://www.anaconda.com/docs/tools/anaconda-navigator/getting-started

#### 2. Cloning repository

Open the terminal in a suitable directory.

```
git clone https://github.com/digikar99/factual_difference_making
```

This should create a directory named `factual_difference_making` with the code in this repository. This is necessary for quickly downloading changes, or making changes. Further changes can be "downloaded" by starting the terminal inside the `factual_difference_making` directory and running:

```
git pull
```

For a quick test run, one can also download [a zip file of the repository](https://github.com/digikar99/factual_difference_making/archive/refs/heads/main.zip). However, this step needs to be performed manually in case of any new changes.

Alternatively, one can use the [Github Desktop Application](https://github.com/apps/desktop) instead of using `git` from the terminal.

#### 3. Check installation

If everything is installed successfully, you should be able to run the tests from the `factual_difference_making` directory.

```sh
python3 fdm_tests.py -v
```

This should produce the below output:

```
test_A_causes_E (__main__.AbnormalDeflation) ... ok
test_C_causes_E (__main__.AbnormalDeflation) ... ok
test_C_more_causal_than_A (__main__.AbnormalDeflation) ... ok
test_C_causes_E (__main__.AbnormalInflation) ... ok
test_F_does_not_cause_notE (__main__.BogusPrevention) ... ok
test_notD_does_not_cause_notE (__main__.BogusPrevention) ... ok
test_D_causes_notE (__main__.BoulderScenario) ... ok
test_F_does_not_cause_notE (__main__.BoulderScenario) ... ok
test_A_does_not_cause_E (__main__.EarlyPreemption) ... ok
test_C_causes_E (__main__.EarlyPreemption) ... ok
test_A_does_not_cause_E (__main__.LatePreemption) ... ok
test_C_causes_E (__main__.LatePreemption) ... ok
test_C_does_not_cause_E (__main__.NoSupersessionDisjunction) ... ok
test_notF_does_not_cause_E (__main__.Omission) ... ok
test_A_causes_E (__main__.Overdetermination) ... ok
test_A_does_not_cause_C (__main__.Overdetermination) ... ok
test_C_causes_E (__main__.Overdetermination) ... ok
test_C_does_not_cause_A (__main__.Overdetermination) ... ok
test_BD_more_causal_than_AC (__main__.QL2023_Exp1) ... ok
test_causes (__main__.QL2023_Exp1) ... ok
test_B_more_causal_than_AC (__main__.QL2023_Exp2a) ... ok
test_causes (__main__.QL2023_Exp2a) ... ok
test_B_more_causal_than_A (__main__.QL2023_Exp2b) ... ok
test_causes (__main__.QL2023_Exp2b) ... ok
test_B_more_causal_than_A (__main__.QL2023_Exp3_Three) ... FAIL
test_causes (__main__.QL2023_Exp3_Three) ... ok
test_B_more_causal_than_A (__main__.QL2023_Exp3_Two) ... ok
test_causes (__main__.QL2023_Exp3_Two) ... ok
test_A_causes_E (__main__.Supersession) ... ok
test_C_does_not_cause_E_failure (__main__.Supersession) ... ok
test_C_less_causal_than_A (__main__.Supersession) ... ok

======================================================================
FAIL: test_B_more_causal_than_A (__main__.QL2023_Exp3_Three)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/path/to/factual-difference-making/fdm_test.py", line 121, in test_B_more_causal_than_A
    self.assertEqual([C, B, A], ordered_causes)
AssertionError: Lists differ: [C, B, A] != [B, C, A]

First differing element 0:
C
B

- [C, B, A]
+ [B, C, A]

----------------------------------------------------------------------
Ran 31 tests in 5.682s

FAILED (failures=1)
```

#### 4. Other tools

**IPython or Jupyter Lab**

Optionally, one can install ipython or jupyterlab:

```
micromamba install ipython jupyterlab
```

Ipython can be started by typing `ipython` from the terminal. [Jupyter Lab](https://docs.jupyter.org/en/latest/) can be started by typing `jupyter-lab` at the terminal; one can then create a Python 3 Notebook to play around the code.

**PyCharm**

[PyCharm](https://www.jetbrains.com/pycharm/) can be useful as a heavy-weight replacement (storage space: 1.1G+!) for both ipython or jupyter-lab. 

**Emacs**

All the above should be considered impoverished versions of [Emacs](https://www.gnu.org/software/emacs/tour/), which gets you:

- [org-mode](https://orgmode.org/)
- an interactive-REPL driven python development (need a simple demo video!) 
- [literate programming](https://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html)

One can get started through one of its community maintained [Starter Kits](https://github.com/emacs-tw/awesome-emacs?tab=readme-ov-file#starter-kit).

Admittedly, PyCharm is useful for navigating larger codebases. But the code here is much smaller.

These days, you also have access to a Python/Julia-like language called [Moonli](https://moonli-lang.github.io/) that transpiles to Common Lisp under the hood.

### Sympy: A Quick Tutorial

The code primarily relies on [sympy](https://www.sympy.org/). See [here](https://docs.sympy.org/latest/tutorials/intro-tutorial/intro.html) for a more detailed tutorial and [here](https://docs.sympy.org/latest/modules/logic.html) for documentation on its Logic module.

Here is a quick sample of the relevant parts of Sympy. To run, start `ipython` or any python REPL and run each line after `>>> `:

```py
>>> import sympy
>>> from sympy import symbols
>>> A, E, C = symbols("A, E, C")
>>> A
A
>>> type(A)
<class 'sympy.core.symbol.Symbol'>
>>> sympy.Or(A, C) # A∨C
A | C
>>> A | C
A | C
>>> type(A|C)
Or
>>> A.is_symbol
True
>>> (A|C).is_symbol
False
>>> Sympy.Not(A)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'Sympy' is not defined. Did you mean: 'sympy'?
>>> sympy.Not(A)
~A
>>> ~A
~A
>>> sympy.And(A, C) # A∧C
A & C
>>> sympy.Eq(E, sympy.Or(A, C)) # E = A∨C
Eq(E, A | C)
>>> from sympy import symbols, Not, And, Or, Eq
>>> Eq(E, Or(A, C))
Eq(E, A | C)
>>>
```

### Demonstration of factual\_difference\_making

```py
from fdm_scenarios import overdetermination
from factual_difference_making import is_cause
from sympy.abc import A, E, C

print(overdetermination)
# Prints: FDMModel(streq={E: Eq(E, A | C)}, literals={A, E, C}, normals=set())

print(is_cause(overdetermination, literal=A, effect=C, preliminary=True))
# Prints: False

print(is_cause(overdetermination, literal=A, effect=E, preliminary=True))
# Prints: FDMModel(streq={E: Eq(E, A | C)}, literals=set(), normals=set())
# This is the minimally unsettled model (M', V') that the paper requires.
```

The crucial check for clauses 4 and 5 of the settling conditional is located [here](https://github.com/digikar99/factual_difference_making/blob/6da343f7531dca8617e3c8aeb2f5097f23fef40a/factual_difference_making.py#L131-L155).

Several scenarios are included in [./fdm\_scenarios.py](./fdm_scenarios.py) and associated tests in [./fdm\_tests.py](./fdm_tests.py). These can be run using `python fdm_tests.py -v`.

### Counterfactual Effect Size Model (CESM)

A version of the CESM described in the supplementary information to Quillien & Lucas (2023) is implemented in [counterfactual\_effect\_size\_model.py](./counterfactual_effect_size_model.py) with scenarios in [cesm\_scenarios.py](cesm_scenarios.py). There are three main functionalities:

- [CESModel](./counterfactual_effect_size_model.py#L18-L43): This is the python class to encode the actual causal scenarios
- [compute\_cesm\_preds](./counterfactual_effect_size_model.py#L68-L114): This function takes in the following arguments and returns a list of CES causal judgments for each of the candidate causes:
    - cesm: an instance of CESModel
    - candidate_causes: a list of symbols representing the causes of which judgments are to be computed
    - effect: a symbol towards which causal judgment is to be computed
    - stability: the stability parameter of CES Model, default value 0.73
    - num_simulations: an integer, default value 500000
- [compare\_cesm\_preds](./counterfactual_effect_size_model.py#L116-L142): This is similar to `compute_cesm_preds` but it takes in a *list* of stability values instead of a single parameter. Additionally, it also has a `plot` parameter. If `plot` is `True`, the predictions across different stability values are plotted on the graph.

#### Example usage

Example usage of the above three functions follows:

```python
import pprint
from sympy.abc import A, B, C, D, E
from counterfactual_effect_size_model import CESModel, compute_cesm_preds, compare_cesm_scores

cesm_example = CESModel(
	actuals = {A, B, C, E},
	exovar_probs = {A: 0.1, B: 0.2, C: 0.4, D: 0.1},
	streq = {
		E: A & (B | C) & ~D
	}
)

scores = compute_cesm_preds(cesm_example, [A, B, C, D], E, 0.7)

multiple_scores = compare_cesm_scores(cesm_example, [A, D], E, [0.1, 0.5, 0.9], plot=True)

print(cesm_example)
pprint.pp(scores)
pprint.pp(multiple_scores)
```

The above will print the following:

```
CESModel(
	actuals={B, E, A, C},
	exovars={B, A, D, C},
	exovar_probs={A: 0.1, B: 0.2, C: 0.4, D: 0.1},
	endovars={E},
	streq={E: A & ~D & (B | C)}
)
[0.8822947310136721,
 0.11661130611234129,
 0.13924593447358163,
 0.2537049270209159]
{0.1: [0.20072910878713288, 0.10833964333745462],
 0.5: [0.19160244467423573, 0.2110518532388487],
 0.9: [0.057301934427855535, 0.29894824528730846]}
```

And plot the graph:

![cesm\_example.svg](./cesm_example.svg)

#### Given scenarios

A number of scenarios are encoded as CESModels in [cesm\_scenarios.py](./cesm_scenarios.py). These can be tried out by starting the python REPL (say, ipython) in the current directory.

```
ipython
```

And then loading the file with `%load` magic command:

```
Python 3.10.14 (main, Mar 21 2024, 16:24:04) [GCC 11.2.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.20.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: %load cesm_scenarios.py
.
.
.
   ...: 

In [3]: compute_cesm_preds(tadeg_example, [A], E, 0.7)
Out[3]: [0.8815847792486272]

In [4]: compare_cesm_preds(tadeg_example, [B,D], E, [0.1, 0.5, 0.9])
Out[4]: 
{0.1: [0.13621218857748088, 0.10773595682399688],
 0.5: [0.15434755362037963, 0.21211084515899076],
 0.9: [0.04779874182336246, 0.29568345646915256]}

In [5]: compare_cesm_preds(tadeg_example, [B,D], E, [0.1, 0.5, 0.9], plot=True)
Out[5]: 
{0.1: [0.13620669467752805, 0.10857909539791742],
 0.5: [0.15388884915057188, 0.21066856586803984],
 0.9: [0.04846425807415143, 0.2962318523452058]}

```

# References

- Andreas, Holger and Gunther, Mario (2025). "Factual Difference-Making".
- Quillien, T & Lucas, CG 2023, 'Counterfactuals and the Logic of Causal Selection', Psychological Review, pp. 1-27. https://doi.org/10.1037/rev0000428
