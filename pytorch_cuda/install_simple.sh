pip install --upgrade pip==22.0.4 pip-tools
hash -r 

pip install ray[default,rllib,tune,serve]==1.12.0 gym[atari] gym[accept-rom-license] atari_py "matplotlib>=3.2.2" "numpy>=1.18.5" "opencv-python>=4.1.2" Pillow "PyYAML>=5.3.1" "scipy>=1.4.1" "tqdm>=4.41.0" "tensorboard>=2.4.1" "seaborn>=0.11.0" pandas "pycocotools>=2.0" thop humanize 
