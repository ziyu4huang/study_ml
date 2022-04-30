# https://docs.ray.io/en/latest/tune/examples/includes/pb2_example.html


# PB2 Example


# Traceback (most recent call last):
#   File "ray_tune_example_basic_ex5.py", line 63, in <module>
#     "lr": [0.0001, 0.02],
#   File "/home/ziyu4huang/tf1dml/lib/python3.7/site-packages/ray/tune/schedulers/pb2.py", line 288, in __init__
#     raise RuntimeError("Please install GPy to use PB2.")
# RuntimeError: Please install GPy to use PB2.

#!/usr/bin/env python

import argparse

import ray
from ray import tune
from ray.tune.schedulers.pb2 import PB2
from ray.tune.examples.pbt_function import pbt_function

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
    if args.smoke_test:
        ray.init(num_cpus=2)  # force pausing to happen for test
    else:
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)
        # if args.server_address:
        #     ray.init(f"ray://{args.server_address}")
        # else:
        #     ray.init()

    pbt = PB2(
        perturbation_interval=20,
        hyperparam_bounds={
            # hyperparameter bounds.
            "lr": [0.0001, 0.02],
        },
    )

    analysis = tune.run(
        pbt_function,
        name="pbt_test",
        scheduler=pbt,
        metric="mean_accuracy",
        mode="max",
        verbose=False,
        stop={
            "training_iteration": 30,
        },
        num_samples=8,
        fail_fast=True,
        config={
            "lr": 0.0001,
            # note: this parameter is perturbed but has no effect on
            # the model training in this example
            "some_other_factor": 1,
        },
    )

    print("Best hyperparameters found were: ", analysis.best_config)


