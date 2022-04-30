# https://docs.ray.io/en/latest/tune/examples/includes/tune_basic_example.html


# Can be done in CPU mode , WSL, here is result
#
# (run pid=8848) 2022-04-30 16:54:20,074  INFO tune.py:702 -- Total run time: 220.75 seconds (220.50 seconds for the tuning loop).
# Best hyperparameters found were:  {'steps': 100, 'width': 13.416895766246435, 'height': -98.8100134116277, 'activation': 'tanh'}
#

"""This example demonstrates basic Ray Tune random search and grid search."""
import time

import ray
from ray import tune


def evaluation_fn(step, width, height):
    time.sleep(0.1)
    return (0.1 + width * step / 100) ** (-1) + height * 0.1


def easy_objective(config):
    # Hyperparameters
    width, height = config["width"], config["height"]

    for step in range(config["steps"]):
        # Iterative training function - can be any arbitrary training procedure
        intermediate_score = evaluation_fn(step, width, height)
        # Feed the score back back to Tune.
        tune.report(iterations=step, mean_loss=intermediate_score)


if __name__ == "__main__":
    import platform_util
    ipv4, gpu, cpu = platform_util.check_platform()

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gpu",
        type=int,
        default=gpu,
    )
    parser.add_argument(
        "--cpu",
        type=int,
        default=cpu,
    )
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
    ),
    args, _ = parser.parse_known_args()
    if args.server_address is not None:
        # ray.init(f"ray://{args.server_address}")
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)
    else:
        ray.init(configure_logging=False)

    # This will do a grid search over the `activation` parameter. This means
    # that each of the two values (`relu` and `tanh`) will be sampled once
    # for each sample (`num_samples`). We end up with 2 * 50 = 100 samples.
    # The `width` and `height` parameters are sampled randomly.
    # `steps` is a constant parameter.

    analysis = tune.run(
        easy_objective,
        metric="mean_loss",
        mode="min",
        num_samples=5 if args.smoke_test else 50,
        config={
            "steps": 5 if args.smoke_test else 100,
            "width": tune.uniform(0, 20),
            "height": tune.uniform(-100, 100),
            "activation": tune.grid_search(["relu", "tanh"]),
        },
    )

    print("Best hyperparameters found were: ", analysis.best_config)