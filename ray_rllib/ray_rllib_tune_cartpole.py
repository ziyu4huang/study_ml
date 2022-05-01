

# https://docs.ray.io/en/latest/rllib/rllib-training.html

# pass on M1/TF2.8

# All RLlib trainers are compatible with the Tune API. This enables
# them to be easily used in experiments with Tune. For example, the
# following code performs a simple hyperparam sweep of PPO:
import ray
from ray import tune

if __name__ == "__main__":
    import platform_util
    ipv4, gpu, cpu = platform_util.check_platform()

    #region parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gpu",
        type=int,
        default=gpu,
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
    #endregion parser

    if args.server_address == "auto":
        ray.init(address="auto", configure_logging=False)
    else:
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)

    tune.run(
        "PPO",
        # stop behavior see: https://docs.ray.io/en/latest/tune/tutorials/tune-stopping.html#tune-stopping-ref
        stop={
            "training_iteration": 7,
            "episode_reward_mean": 200,
            "time_total_s": 600
        },
        # common hypterparametrer see: https://github.com/ray-project/ray/blob/master/rllib/agents/trainer.py
        config={
            "framework": "tf2",
            "env": "CartPole-v0",
            "num_gpus": gpu,
            "num_workers": 1,
            "disable_env_checking": True,
            # to much grid for smoke test
            # "lr": tune.grid_search([0.01, 0.001, 0.0001]),
            "lr": tune.grid_search([0.1, 0.001]),
        },
    )
