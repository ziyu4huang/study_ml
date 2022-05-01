"""
Example showing how you can use your trained policy for inference
(computing actions) in an environment.

Includes options for LSTM-based models (--use-lstm), attention-net models
(--use-attention), and plain (non-recurrent) models.

This is from [Github permlink](https://github.com/ray-project/ray/blob/bb4e5cb70a53a50654211136e5bff26dfdfc25a7/rllib/examples/inference_and_serving/policy_inference_after_training.py)


Run this on M1: with option --- 
I gave up, I can't make this run using M1 GPU
export RLLIB_NUM_GPUS=6
  -num-gpus 6
   
This take very long to run Mac M1:
  about : 
"""
import argparse
import gym
import os

import ray
from ray import tune
from ray.rllib.agents.registry import get_trainer_class

import platform_util
ipv4, gpu, cpu = platform_util.check_platform()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--run", type=str, default="PPO", help="The RLlib-registered algorithm to use."
)
parser.add_argument("--num-cpus", type=int, default=8)
parser.add_argument("--num-gpus", type=int, default=1)
parser.add_argument(
    "--framework",
    choices=["tf", "tf2", "tfe", "torch"],
    default="tf2",
    help="The DL framework specifier.",
)
parser.add_argument("--eager-tracing", action="store_true")
parser.add_argument(
    "--stop-iters",
    type=int,
    default=50,
    help="Number of iterations to train before we do inference.",
)
parser.add_argument(
    "--stop-timesteps",
    type=int,
    default=100000,
    help="Number of timesteps to train before we do inference.",
)
parser.add_argument(
    "--stop-reward",
    type=float,
    default=150.0,
    help="Reward at which we stop training before we do inference.",
)
parser.add_argument(
    "--explore-during-inference",
    action="store_true",
    help="Whether the trained policy should use exploration during action "
    "inference.",
)
parser.add_argument(
    "--num-episodes-during-inference",
    type=int,
    default=10,
    help="Number of episodes to do inference over after training.",
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

if __name__ == "__main__":
    args = parser.parse_args()

    if args.server_address == "auto":
        ray.init(address="auto", configure_logging=False)
        #ray.init(num_cpus=args.num_cpus or None)
    else:
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)

    config = {
        "env": "FrozenLake-v1",
        # Run with tracing enabled for tfe/tf2?
        "eager_tracing": args.eager_tracing,
        # enable True for tf2
        # "eager_tracing": True, # for production purpose
        # "disable_env_checking": True,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        #"num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "num_gpus": args.num_gpus,
        "framework": args.framework
    }

    stop = {
        "training_iteration": args.stop_iters,
        "timesteps_total": args.stop_timesteps,
        "episode_reward_mean": args.stop_reward,
    }

    print("Training policy until desired reward/timesteps/iterations. ...")
    results = tune.run(
        args.run,
        config=config,
        stop=stop,
        verbose=2,
        checkpoint_freq=1,
        checkpoint_at_end=True,
    )

    print("Training completed. Restoring new Trainer for action inference.")
    # Get the last checkpoint from the above training run.
    checkpoint = results.get_last_checkpoint()
    # Create new Trainer and restore its state from the last checkpoint.
    trainer = get_trainer_class(args.run)(config=config)
    trainer.restore(checkpoint)

    # Create the env to do inference in.
    env = gym.make("FrozenLake-v1")
    obs = env.reset()

    num_episodes = 0
    episode_reward = 0.0

    while num_episodes < args.num_episodes_during_inference:
        # Compute an action (`a`).
        a = trainer.compute_single_action(
            observation=obs,
            explore=args.explore_during_inference,
            policy_id="default_policy",  # <- default value
        )
        # Send the computed action `a` to the env.
        obs, reward, done, _ = env.step(a)
        episode_reward += reward
        # Is the episode `done`? -> Reset.
        if done:
            print(f"Episode done: Total reward = {episode_reward}")
            obs = env.reset()
            num_episodes += 1
            episode_reward = 0.0

    if args.server_address == "auto":
        # dont shutdown on server mode
        ray.shutdown()


    # Currently, on M1,  program stop at "EOF Error: Ran out of input"
    # https://github.com/ray-project/ray/issues/2685

