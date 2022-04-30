# https://docs.ray.io/en/latest/tune/examples/includes/logging_example.html


# Logging Example

#!/usr/bin/env python

import argparse
import time

from ray import tune
from ray.tune.logger import LoggerCallback


class TestLoggerCallback(LoggerCallback):
    def on_trial_result(self, iteration, trials, trial, result, **info):
        print(f"TestLogger for trial {trial}: {result}")


def trial_str_creator(trial):
    return "{}_{}_123".format(trial.trainable_name, trial.trial_id)


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
    import ray
    import platform_util
    ipv4, gpu, cpu = platform_util.check_platform()

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

    analysis = tune.run(
        easy_objective,
        name="hyperband_test",
        metric="mean_loss",
        mode="min",
        num_samples=5,
        trial_name_creator=trial_str_creator,
        callbacks=[TestLoggerCallback()],
        stop={"training_iteration": 1 if args.smoke_test else 100},
        config={
            "steps": 100,
            "width": tune.randint(10, 100),
            "height": tune.loguniform(10, 100),
        },
    )
    print("Best hyperparameters: ", analysis.best_config)
