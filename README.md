# parsec-possum
**Parallax Optimization Software and Somewhat Uncertain Measurements**

Using Bayesian optimization via Hyperopt to maximize rocket height and stability through repeated simulation.

Dependencies:
 - scipy ecosystem
 - hyperopt
 - click
 - pyautogui
 - RASAero (Windows-only standalone program)

## Running optimization
The optimization script is invoked with `python3 optimize.py`.
RASAero must be running in a Windows left-split for cached mouse locations to work.
Logs, sample points, and losses are recorded under `hyperopt_runs` throughout.

## Learned parameters
TODO

## Citations
Hyperopt can be found at https://github.com/hyperopt/hyperopt.
