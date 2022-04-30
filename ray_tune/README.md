

# Colab example of Ray Tune,  Tensoflow only


[Here is original colab](https://colab.research.google.com/github/ray-project/tutorial/blob/master/tune_exercises/exercise_1_basics.ipynb#scrollTo=CbYE0EwkuH_D)


I wrap it to a local python file 

[Local python tf_basic.py](tf_basic.py)

```
# how to run it 
```


# Tune Result 

Still not works correctly under WSL (no metter CPU or GPU )

it works on Macos / M1  setting 

##  ex1  -- on CPU mode  -- ray_tune_example_tf_ex1.py

>  python ray_tune_example_tf_ex1.py


```
(run pid=30549) == Status ==
(run pid=30549) Current time: 2022-04-30 13:25:14 (running for 00:03:27.51)
(run pid=30549) Memory usage on this node: 3.4/7.7 GiB
(run pid=30549) Using AsyncHyperBand: num_stopped=0
(run pid=30549) Bracket: Iter 320.000: None | Iter 80.000: None | Iter 20.000: None
(run pid=30549) Resources requested: 0/8 CPUs, 0/0 GPUs, 0.0/3.78 GiB heap, 0.0/1.89 GiB objects
(run pid=30549) Current best trial: 6e2a3_00005 with mean_accuracy=0.9902333617210388 and parameters={'threads': 2, 'lr': 0.0923391580993009, 'momentum': 0.7478894946481159, 'hidden': 377}
(run pid=30549) Result logdir: /home/ziyu4huang/ray_results/exp
(run pid=30549) Number of trials: 10/10 (10 TERMINATED)
(run pid=30549) +-------------------------+------------+---------------------+----------+-----------+------------+----------+--------+------------------+
(run pid=30549) | Trial name              | status     | loc                 |   hidden |        lr |   momentum |      acc |   iter |   total time (s) |
(run pid=30549) |-------------------------+------------+---------------------+----------+-----------+------------+----------+--------+------------------|
(run pid=30549) | train_mnist_6e2a3_00000 | TERMINATED | 172.23.26.224:30674 |      314 | 0.0659666 |   0.58544  | 0.9814   |     12 |          20.1392 |
(run pid=30549) | train_mnist_6e2a3_00001 | TERMINATED | 172.23.26.224:31463 |      510 | 0.0782941 |   0.126104 | 0.9764   |     12 |          23.6243 |
(run pid=30549) | train_mnist_6e2a3_00002 | TERMINATED | 172.23.26.224:32114 |      470 | 0.0358024 |   0.293729 | 0.96565  |     12 |          21.7094 |
(run pid=30549) | train_mnist_6e2a3_00003 | TERMINATED | 172.23.26.224:32738 |      325 | 0.0231097 |   0.198122 | 0.95035  |     12 |          18.6412 |
(run pid=30549) | train_mnist_6e2a3_00004 | TERMINATED | 172.23.26.224:861   |       77 | 0.0228321 |   0.650863 | 0.954617 |     12 |          10.7663 |
(run pid=30549) | train_mnist_6e2a3_00005 | TERMINATED | 172.23.26.224:1350  |      377 | 0.0923392 |   0.747889 | 0.990233 |     12 |          19.8368 |
(run pid=30549) | train_mnist_6e2a3_00006 | TERMINATED | 172.23.26.224:1967  |      241 | 0.0265833 |   0.186454 | 0.953717 |     12 |          16.5154 |
(run pid=30549) | train_mnist_6e2a3_00007 | TERMINATED | 172.23.26.224:2554  |      412 | 0.0403198 |   0.451757 | 0.971983 |     12 |          21.3272 |
(run pid=30549) | train_mnist_6e2a3_00008 | TERMINATED | 172.23.26.224:3191  |      256 | 0.0780921 |   0.629148 | 0.983383 |     12 |          16.5484 |
(run pid=30549) | train_mnist_6e2a3_00009 | TERMINATED | 172.23.26.224:3773  |      136 | 0.0995687 |   0.512248 | 0.977467 |     12 |          13.6323 |
(run pid=30549) +-------------------------+------------+---------------------+----------+-----------+------------+----------+--------+------------------+
(run pid=30549)
(run pid=30549)
Best hyperparameters found were:  {'threads': 2, 'lr': 0.0923391580993009, 'momentum': 0.7478894946481159, 'hidden': 377}
(run pid=30549) 2022-04-30 13:25:14,438 INFO tune.py:702 -- Total run time: 207.72 seconds (207.50 seconds for the tuning loop).
```

##  ex2  -- on CPU mode  -- ray_tune_example_tf_ex2.py