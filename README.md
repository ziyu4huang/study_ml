# Install Ray and Tensorflow 2.8 (GPU) in Macbook M1

<!-- TOC -->
<!-- vscode-markdown-toc -->
* 1. [Reference:](#Reference:)
* 2. [STEP_1 homebrew](#STEP_1homebrew)
* 3. [STEP_2 xcode](#STEP_2xcode)
* 4. [STEP_3 instal conda M1(ARM)](#STEP_3instalcondaM1ARM)
* 5. [STEP_4 CREATE conda enviroment, INSTALL tensorflow from Apple Channel](#STEP_4CREATEcondaenviromentINSTALLtensorflowfromAppleChannel)
* 6. [STEP_6 generate via pip-compile](#STEP_6generateviapip-compile)
* 7. [STEP 7 install requirements.txt generate from last step](#STEP7installrequirements.txtgeneratefromlaststep)
* 8. [STEP 8 step special for grpcio hack](#STEP8stepspecialforgrpciohack)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
<!-- TOC -->



##  1. <a name='Reference:'></a>Reference: 
* [tensorflow 2.8 M1 macos](https://betterdatascience.com/install-tensorflow-2-7-on-macbook-pro-m1-pro/)
* [OLD: install tensorflow 2.7 macos](https://betterdatascience.com/install-tensorflow-2-7-on-macbook-pro-m1-pro/)

And try [TensorFlow probility](https://www.tensorflow.org/probability?hl=en), if possible

TensorFlow Probability (TFP) is a Python library built on TensorFlow that makes 
it easy to combine probabilistic models and deep learning on 
modern hardware (TPU, GPU). 

##  2. <a name='STEP_1homebrew'></a>STEP_1 homebrew

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

install necessary brew
```
brew install node
brew install npm
brew install libjpeg
```


##  3. <a name='STEP_2xcode'></a>STEP_2 xcode

> xcode-select --install

##  4. <a name='STEP_3instalcondaM1ARM'></a>STEP_3 instal conda M1(ARM) 

[Ray install Official](https://docs.ray.io/en/latest/ray-overview/installation.html#m1-mac-apple-silicon-support)

```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
# Cleanup.
rm https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
```

##  5. <a name='STEP_4CREATEcondaenviromentINSTALLtensorflowfromAppleChannel'></a>STEP_4 CREATE conda enviroment, INSTALL tensorflow from Apple Channel 

注：tensorflow-deps 的版本是基于 TensorFlow 的，因此可以根据自己的需求指定版本安装：

```shell
conda create --name tf28 python=3.9.5
conda activate tf28
conda install -c apple tensorflow-deps==2.8.0 -y
conda install matplotlib jupyterlab -y

```

Here is image how TensorFlow Macos install
![tf macos](https://betterdatascience.com/content/images/size/w1000/2021/12/6-min.png)

Let's Skip install pip here , using pip-tools 
```shell
# just for refernce
pip install tensorflow-macos (compbine to pip-compile)
pip install tensorflow-metal (compbine to pip-compile)
```


##  6. <a name='STEP_6generateviapip-compile'></a>STEP_6 generate via pip-compile
Install pip-tools first
> pip isntall pip-tools

Install Ray as you normally would. using requirement.txt 
> [pip-compile --> compile.sh ](compile.sh)
```bash 
pip-compile \
    --allow-unsafe \
    --generate-hashes \
    requirements.in \
    --output-file=requirements.txt

```

> [Check file for pip-compile : requirements.in](requirements.in)
```in
tensorflow-macos
tensorflow-metal
tensorboard
ray[default,data,rllib,tune,serve]
### see real requrements.in for detail
```
jupter notebooks seems necessary for VS Code's jupter works 
install on `conda` seems not works.

##  7. <a name='STEP7installrequirements.txtgeneratefromlaststep'></a>STEP 7 install requirements.txt generate from last step

Install generated via `pip-sync`
> pip-sync requirements.txt

##  8. <a name='STEP8stepspecialforgrpciohack'></a>STEP 8 step special for grpcio hack
> pip uninstall grpcio; conda install grpcio  --force-reinstall

If there is any problem , just purge pip via 
> pip chache purge

# Test 

Verify tool version and Tensorflow

```shell
(tf28) ziyu4huang@Ziyu-MBA-M1 study_ml % python
Python 3.9.5 | packaged by conda-forge | (default, Jun 19 2021, 00:24:55) 
[Clang 11.1.0 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow as tf
>>> print(tf.__version__)
2.8.0
>>> tf.config.list_physical_devices()
[PhysicalDevice(name='/physical_device:CPU:0', device_type='CPU'), PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]

```

Tensorflow, takes a little longer (about 10 mins)

```
> python try_tensorflow.py

(tf28) ziyu4huang@Ziyu-MBA-M1 study_ml % python try_tensorflow.py 
Metal device set to: Apple M1

systemMemory: 8.00 GB
maxCacheSize: 2.67 GB

2022-04-24 18:09:37.678779: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:305] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2022-04-24 18:09:37.679902: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:271] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2022-04-24 18:09:38.166989: W tensorflow/core/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz

Epoch 1/10
2022-04-24 18:09:38.350431: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:113] Plugin optimizer for device_type GPU is enabled.
1872/1875 [============================>.] - ETA: 0s - loss: 0.4934 - accuracy: 0.82452022-04-24 18:09:53.286105: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:113] Plugin optimizer for device_type GPU is enabled.


```


------

# CONFIG git 

```ini
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
[remote "origin"]
	url = git@github.com:ziyu4huang/study_ml.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
	remote = origin
	merge = refs/heads/main
[credential]
	helper = store
[user]
	name = ziyu4huang
	email = ziyu4huang@gmail.com
```