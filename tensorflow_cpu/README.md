# Setup Tensorflow 2.8 on CPU mode and Python 3.7.13

This is for special project setting purpurse.
DON'T use this , it's not for Mac M1.

No conda, pure python interpreter. Make it more flexible to 
deploy to enviroments inside firewall .

[See requirements.in](requirements.in) and `compile.sh` 
[Install for CPU only ](https://files.pythonhosted.org/packages/31/66/d9cd0b850397dbd33f070cc371a183b4903120b1c103419e9bf20568456e/tensorflow-2.8.0-cp37-cp37m-manylinux2010_x86_64.whl)
[from here ](https://pypi.org/project/tensorflow/2.8.0/#files)

## what if I want specifiy local path ?
[Reference](https://stackoverflow.com/questions/9809557/use-a-relative-path-in-requirements-txt-to-install-a-tar-gz-file-with-pip)

```
fabric==1.13.1
./some_fir/some_package.whl
packaging==16.8
```

maybe for GPU ?
[install for GPU](https://files.pythonhosted.org/packages/70/1d/eed1827b2482dcb855d43cb660d0e9ca5e91a14c9e7d4e5b884bc6e58029/tensorflow_gpu-2.8.0-cp37-cp37m-win_amd64.whl)
[from here ](https://pypi.org/project/tensorflow-gpu/2.8.0/#files)
