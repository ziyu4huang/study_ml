# Install Ray and Tensorflow 2.7 (GPU) in Macbook M1

see [requirements.in](./requirements.in)

## Reference: 
[install tensorflow 2.7 macos](https://betterdatascience.com/install-tensorflow-2-7-on-macbook-pro-m1-pro/)

## STEP_#1 homebrew

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


## STEP_#2 xcode

> xcode-select --install

## STEP_#3 instal conda M1(ARM) 

[Ref](https://docs.ray.io/en/latest/ray-overview/installation.html#m1-mac-apple-silicon-support)

```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
rm https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh # Cleanup.
```

## STEP_#4 CREATE conda enviroment, INSTALL tensorflow from Apple Channel 

```shell
conda create --name ray python=3.9; conda activate ray

conda install -c apple tensorflow-deps -y

```

![tf macos](https://betterdatascience.com/content/images/size/w1000/2021/12/6-min.png)

# <SKIP HERE> pip install tensorflow-macos (compbine to pip-compile)
# <SKIP HERE> pip install tensorflow-metal (compbine to pip-compile)


## STEP_#6 generate via pip-compile

Install Ray as you normally would. using requirement.txt 
> ==== compile.sh ================
```bash 
pip-compile \
    --allow-unsafe \
    --generate-hashes \
    requirements.in \
    --output-file=requirements.txt

```
> ===== requirements.in =======
```in
setuptools
keras
tensorflow-macos
tensorflow-metal
tensorboard
ray[default,data,rllib,tune,serve]
pyarrow
dask

jupyter
notebook
jupyterlab

ipywidgets         
jupyter_console    
jupyterlab_widgets 
prompt_toolkit     
widgetsnbextension 
```
jupter notebooks seems necessary for VS Code's jupter works 
install on `conda` seems not works.

## STEP #7 install requirements.txt generate from last step

> pip-sync requirements.txt

## STEP #8 step special for grpcio hack
> pip uninstall grpcio; conda install grpcio  --force-reinstall

# More package required in conda install after use VSCode
 at  4/23, runs ipython on VScode directly has missing package 
 warnning from VScode. 

```
The following NEW packages will be INSTALLED:

  ipywidgets         conda-forge/noarch::ipywidgets-7.7.0-pyhd8ed1ab_0
  jupyter            conda-forge/osx-arm64::jupyter-1.0.0-py39h2804cbe_7
  jupyter_console    conda-forge/noarch::jupyter_console-6.4.3-pyhd8ed1ab_0
  jupyterlab_widgets conda-forge/noarch::jupyterlab_widgets-1.1.0-pyhd8ed1ab_0
  prompt_toolkit     conda-forge/noarch::prompt_toolkit-3.0.29-hd8ed1ab_0
  widgetsnbextension conda-forge/osx-arm64::widgetsnbextension-3.6.0-py39h2804cbe_0
```

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
