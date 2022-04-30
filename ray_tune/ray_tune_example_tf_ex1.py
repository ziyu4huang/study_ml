# https://docs.ray.io/en/latest/tune/examples/tune_mnist_keras.html#tune-mnist-keras

import argparse
import os

from filelock import FileLock
from tensorflow.keras.datasets import mnist

import ray
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.integration.keras import TuneReportCallback


def train_mnist(config):
    # https://github.com/tensorflow/tensorflow/issues/32159
    import tensorflow as tf

    batch_size = 128
    num_classes = 10
    epochs = 12

    with FileLock(os.path.expanduser("~/.data.lock")):
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(config["hidden"], activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.compile(
        loss="sparse_categorical_crossentropy",
        optimizer=tf.keras.optimizers.SGD(lr=config["lr"], momentum=config["momentum"]),
        metrics=["accuracy"],
    )

    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        verbose=0,
        validation_data=(x_test, y_test),
        callbacks=[TuneReportCallback({"mean_accuracy": "accuracy"})],
    )


def tune_mnist(num_training_iterations, gpu=0):
    sched = AsyncHyperBandScheduler(
        time_attr="training_iteration", max_t=400, grace_period=20
    )

    analysis = tune.run(
        train_mnist,
        name="exp",
        scheduler=sched,
        metric="mean_accuracy",
        mode="max",
        stop={"mean_accuracy": 0.99, "training_iteration": num_training_iterations},
        num_samples=10,
        resources_per_trial={"cpu": 4, "gpu": gpu},
        config={
            "threads": 2,
            "lr": tune.uniform(0.001, 0.1),
            "momentum": tune.uniform(0.1, 0.9),
            "hidden": tune.randint(32, 512),
        },
    )
    print("Best hyperparameters found were: ", analysis.best_config)


if __name__ == "__main__":

    import platform_util
    ipv4, gpu, cpu = platform_util.check_platform()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-test", action="store_true", help="Finish quickly for testing"
    ),
    parser.add_argument(
        "--server-port",
        type=str,
        default=10001,
    ),
    parser.add_argument(
        "--gpu",
        type=int,
        default=gpu,
    ),
    parser.add_argument(
        "--server-address",
        type=str,
        default=ipv4,
        required=False,
        help="The address of server to connect to if using " "Ray Client.",
    )
    args, _ = parser.parse_known_args()
    if args.smoke_test:
        ray.init(num_cpus=4)
    elif args.server_address:
        url = f"ray://{args.server_address}:{args.server_port}"
        print("Connect to url: ", url)
        ray.init(url)

    tune_mnist(num_training_iterations=5 if args.smoke_test else 300, gpu=args.gpu)

# not complete we found erros in the end
# ray.tune.error.TuneError: ('Trials did not complete', [train_mnist_8b005_00000, train_mnist_8b005_00001, train_mnist_8b005_00002, tr

