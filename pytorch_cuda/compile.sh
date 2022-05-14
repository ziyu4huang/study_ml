
pip install --upgrade pip==22.0.4 pip-tools
hash -r 

#--allow-unsafe \

pip-compile \
    --generate-hashes \
    requirements.in \
    --output-file=requirements.txt \
    --pip-args "-f https://download.pytorch.org/whl/lts/1.8/torch_lts.html --no-cache-dir" 

