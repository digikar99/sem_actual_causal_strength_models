
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

A version of the CESM described by Quillien & Lucas (2023) is implemented in [cesm\_analogous\_scenario.py](cesm_analogous_scenario.py).

```sh
$ python cesm_analogous_scenario.py
Survival Scenario
    Poison (or its lack) is a cause: 0.048166222824911176
    Antidote (or its lack) is a cause: 0.004782446789884183
Death Scenario
    Poison (or its lack) is a cause: 0.960360193169354
    Antidote (or its lack) is a cause: 1.0531141052550403
```

# References

- Andreas, Holger and Gunther, Mario (2025). "Factual Difference-Making".
- Quillien, T & Lucas, CG 2023, 'Counterfactuals and the Logic of Causal Selection', Psychological Review, pp. 1-27. https://doi.org/10.1037/rev0000428
