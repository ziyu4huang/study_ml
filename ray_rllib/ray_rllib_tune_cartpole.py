

# https://docs.ray.io/en/latest/rllib/rllib-training.html

# All RLlib trainers are compatible with the Tune API. This enables 
# them to be easily used in experiments with Tune. For example, the 
# following code performs a simple hyperparam sweep of PPO:
import ray
from ray import tune

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

    if args.server_address == "auto"
        ray.init(address="auto", configure_logging=False)
    else:
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)

    tune.run(
        "PPO",
        stop={"episode_reward_mean": 200},
        config={
            "env": "CartPole-v0",
            "num_gpus": gpu,
            "num_workers": 1,
            "lr": tune.grid_search([0.01, 0.001, 0.0001]),
        },
    )