pip3 install --upgrade pip==22.0.4 pip-tools
hash -r 
#pip install "torch==1.8.2+cpu" "torchvision==0.9.2+cpu" "torchaudio==0.8.2"
#pip install "torch==1.8.2+cu111" "torchvision==0.9.2+cu111" "torchaudio==0.8.2"
pip3 install "torch" "torchvision" "torchaudio" --extra-index-url https://download.pytorch.org/whl/cu113

pip3 install ray[default,rllib,tune,serve]==1.12.0 gym[atari] gym[accept-rom-license] atari_py "matplotlib>=3.2.2" "numpy>=1.18.5" "opencv-python>=4.1.2" Pillow "PyYAML>=5.3.1" "scipy>=1.4.1" "tqdm>=4.41.0" "tensorboard>=2.4.1" "seaborn>=0.11.0" pandas "pycocotools>=2.0" thop humanize 
