#  https://docs.ray.io/en/latest/tune/examples/includes/hyperband_function_example.html

# HyperBand Function Example

# Finish WSL 
#
#  2022-04-30 17:07:51,064 INFO tune.py:702 -- Total run time: 14.94 seconds (14.67 seconds for the tuning loop).
# Best hyperparameters found were:  {'height': 99.12911937221132}
#

#!/usr/bin/env python

import argparse
import json
import os

import numpy as np

import ray
from ray import tune
from ray.tune.schedulers import HyperBandScheduler


def train(config, checkpoint_dir=None):
    step = 0
    if checkpoint_dir:
        with open(os.path.join(checkpoint_dir, "checkpoint")) as f:
            step = json.loads(f.read())["timestep"]

    for timestep in range(step, 100):
        v = np.tanh(float(timestep) / config.get("width", 1))
        v *= config.get("height", 1)

        # Checkpoint the state of the training every 3 steps
        # Note that this is only required for certain schedulers
        if timestep % 3 == 0:
            with tune.checkpoint_dir(step=timestep) as checkpoint_dir:
                path = os.path.join(checkpoint_dir, "checkpoint")
                with open(path, "w") as f:
                    f.write(json.dumps({"timestep": timestep}))

        # Here we use `episode_reward_mean`, but you can also report other
        # objectives such as loss or accuracy.
        tune.report(episode_reward_mean=v)


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

    # Hyperband early stopping, configured with `episode_reward_mean` as the
    # objective and `training_iteration` as the time unit,
    # which is automatically filled by Tune.
    hyperband = HyperBandScheduler(max_t=200)

    analysis = tune.run(
        train,
        name="hyperband_test",
        num_samples=20,
        metric="episode_reward_mean",
        mode="max",
        stop={"training_iteration": 10 if args.smoke_test else 99999},
        config={"height": tune.uniform(0, 100)},
        scheduler=hyperband,
        fail_fast=True,
    )
    print("Best hyperparameters found were: ", analysis.best_config)
