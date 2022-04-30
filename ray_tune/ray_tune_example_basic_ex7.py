# https://docs.ray.io/en/latest/tune/examples/includes/genetic_example.html

# Genetic Search Example

"""This example demonstrates the usage of GeneticSearch with Ray Tune.

It also checks that it is usable with a separate scheduler.
"""
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.automl import GeneticSearch
from ray.tune.automl import ContinuousSpace, DiscreteSpace, SearchSpace


def michalewicz_function(config, reporter):
    """f(x) = -sum{sin(xi) * [sin(i*xi^2 / pi)]^(2m)}"""
    import numpy as np

    x = np.array([config["x1"], config["x2"],
                 config["x3"], config["x4"], config["x5"]])
    sin_x = np.sin(x)
    z = np.arange(1, 6) / np.pi * (x * x)
    sin_z = np.power(np.sin(z), 20)  # let m = 20
    y = np.dot(sin_x, sin_z)

    # Negate y since we want to minimize y value
    tune.report(timesteps_total=1, neg_mean_loss=-y)


if __name__ == "__main__":
    import ray
    import platform_util
    ipv4, gpu, cpu = platform_util.check_platform()

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-test", action="store_true", help="Finish quickly for testing"
    )
    parser.add_argument(
        "--server-address",
        type=str,
        default=ipv4,
        required=False,
        help="The address of server to connect to if using Ray Client.",
    )
    parser.add_argument(
        "--server-port",
        type=str,
        default=10001,
    )
    args, _ = parser.parse_known_args()

    if args.server_address is not None:
        # ray.init(f"ray://{args.server_address}")
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)
    else:
        ray.init(num_cpus=4 if args.smoke_test else None)

    space = SearchSpace(
        {
            ContinuousSpace("x1", 0, 4, 100),
            ContinuousSpace("x2", -2, 2, 100),
            ContinuousSpace("x3", 1, 5, 100),
            ContinuousSpace("x4", -3, 3, 100),
            DiscreteSpace("x5", [-1, 0, 1, 2, 3]),
        }
    )

    algo = GeneticSearch(
        space,
        reward_attr="neg_mean_loss",
        max_generation=2 if args.smoke_test else 10,
        population_size=10 if args.smoke_test else 50,
    )
    scheduler = AsyncHyperBandScheduler()
    analysis = tune.run(
        michalewicz_function,
        metric="neg_mean_loss",
        mode="max",
        name="my_exp",
        search_alg=algo,
        scheduler=scheduler,
        # stop={"training_iteration": 100},
        stop={"training_iteration": 1},
    )

    print("Best hyperparameters found were: ", analysis.best_config)
