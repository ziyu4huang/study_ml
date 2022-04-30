# https://docs.ray.io/en/latest/tune/examples/includes/async_hyperband_example.html

# Asynchronous HyperBand Example


# == Status ==
# Current time: 2022-04-30 16:56:45 (running for 00:00:59.96)
# Memory usage on this node: 3.5/7.7 GiB
# Using AsyncHyperBand: num_stopped=20
# Bracket: Iter 80.000: -0.8708948307695279 | Iter 20.000: -0.9799420065482168 | Iter 5.000: -2.3450945826232954
# Resources requested: 0/16 CPUs, 0/0 GPUs, 0.0/3.49 GiB heap, 0.0/1.75 GiB objects
# Current best trial: 52b74_00004 with mean_loss=0.6136968183091228 and parameters={'steps': 100, 'width': 20.961359105506055, 'height': 5.657392025159047}
# Result logdir: /home/ziyu4huang/ray_results/asynchyperband_test
# Number of trials: 20/20 (20 TERMINATED)


# 2022-04-30 16:56:45,749 INFO tune.py:702 -- Total run time: 60.09 seconds (59.96 seconds for the tuning loop).
# Best hyperparameters found were:  {'steps': 100, 'width': 20.961359105506055, 'height': 5.657392025159047}

#!/usr/bin/env python

import argparse
import time

import ray
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler


def evaluation_fn(step, width, height):
    time.sleep(0.1)
    return (0.1 + width * step / 100) ** (-1) + height * 0.1


def easy_objective(config):
    # Hyperparameters
    width, height = config["width"], config["height"]

    for step in range(config["steps"]):
        # Iterative training function - can be an arbitrary training procedure
        intermediate_score = evaluation_fn(step, width, height)
        # Feed the score back back to Tune.
        tune.report(iterations=step, mean_loss=intermediate_score)


if __name__ == "__main__":
    import platform_util
    ipv4, gpu, cpu = platform_util.check_platform()

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
        "--ray-address",
        help="Address of Ray cluster for seamless distributed execution.",
        required=False,
    )
    parser.add_argument(
        "--server-address",
        type=str,
        default=None,
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
        ray.init(address=args.ray_address)

    # AsyncHyperBand enables aggressive early stopping of bad trials.
    scheduler = AsyncHyperBandScheduler(grace_period=5, max_t=100)

    # 'training_iteration' is incremented every time `trainable.step` is called
    stopping_criteria = {"training_iteration": 1 if args.smoke_test else 9999}

    analysis = tune.run(
        easy_objective,
        name="asynchyperband_test",
        metric="mean_loss",
        mode="min",
        scheduler=scheduler,
        stop=stopping_criteria,
        num_samples=20,
        verbose=1,
        resources_per_trial={"cpu": cpu, "gpu": gpu},
        config={  # Hyperparameter space
            "steps": 100,
            "width": tune.uniform(10, 100),
            "height": tune.uniform(0, 100),
        },
    )
    print("Best hyperparameters found were: ", analysis.best_config)
