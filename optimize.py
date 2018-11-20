from functools import partial
import logging
import click
from hyperopt import fmin, tpe, Trials
import run_simulation
import sample_space


def objective(args, args_file):
    '''
    Scores a point in some sample space.

    Acts as the objective function hyperopt uses, feeding sampled points into
    score_design to achieve minimization.
    '''
    logging.info('Evaluating objective with args: {}'.format(args))
    args_file.write(str(args) + '\n')
    return run_simulation.score_design(**sample_space.parse_args(args))


@click.command()
@click.option('--max_trials', prompt='Max trials', default=1000,
              help='maximum number of times to run simulation')
@click.option('--space',
              prompt='Sample space\n├─ 0: body only\n├─ 1: few free\n'
              '├─ 2: most free\n└─ 3: all free',
              default=0, help='which sample space to use')
def run_optimization(max_trials, space):
    name_base = 'hyperopt_runs/{}_{}'.format(max_trials, space)
    logging.basicConfig(filename='{}.log'.format(name_base),
                        level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s: %(message)s')
    logging.info('Starting a run with max_trials {} and sample space {}'
                 .format(max_trials, space))

    with open('{}.args'.format(name_base), 'w+') as args_file:
        objective_fn = partial(objective, args_file=args_file)
        trials = Trials()
        space = [sample_space.space_body,
                 sample_space.space_few,
                 sample_space.space_most,
                 sample_space.space_all][space]
        best = fmin(objective_fn,
                    space=space,
                    algo=tpe.suggest,
                    max_evals=max_trials,
                    trials=trials)

    with open('{}.losses'.format(name_base), 'w+') as losses_file:
        for loss in trials.losses():
            losses_file.write(str(loss) + '\n')

    logging.info('Done!')
    logging.info('Best point found: {}'.format(best))


if __name__ == '__main__':
    run_optimization()
