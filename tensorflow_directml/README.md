# Recently Study on this 

Try run Ray on WSL2/GPU_directml  (Ubuntu 20)

Try Cluster run
* start ray head via [bash script](start_ray.sh), with dashboard remote access
* try connect to above ray cluster (head) , using notebook in VSCode [See](notebook/hello.ipynb)

TODO: next

* Try ray up/exec to [connect cluster, exec inside cluster](https://docs.ray.io/en/releases-1.2.0/cluster/commands.html#launching-a-cluster-ray-up)
* try ray submit to exec script in cluster.

# Setup Tensorflow 1.15 on GPU/Directml mode and Python 3.7
This is for special project setting purpurse.

No conda, pure python interpreter. Make it more flexible to 
deploy to enviroments inside firewall .

[See requirements.in](requirements.in) and `compile.sh` 

maybe for GPU ?
[install for GPU/Directml](https://files.pythonhosted.org/packages/7a/10/eaf42847d42c8c2eef2686b3eecd2e1f16d98b748723b932baf60b771496/tensorflow_directml-1.15.5-cp37-cp37m-manylinux2010_x86_64.whl)
[from here ](https://pypi.org/project/tensorflow-directml/#files)


# reinstall Python 3.7 due to below error


```
(pid=16730) /home/ziyu4huang/tf1dml/lib/python3.7/site-packages/pandas/compat/__init__.py:124: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.
(pid=16730)   warnings.warn(msg)
```

If you compile Python from source, you must have the lzma-dev package installed, or it will not be built into python.
```

For ubuntu: sudo apt-get install liblzma-dev

For centos: yum install -y xz-devel

Then configure && make && make install
``
