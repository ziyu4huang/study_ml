# pip-sync requirements.txt \
#   --pip-args --force-exclude-deps grpcio # not works
#pip-sync requirements.txt 

#ray start --head --port=6379
# [doc](https://docs.ray.io/en/latest/cluster/index.html)

# --address 0.0.0.0 # not used after 1.12.0 , now redis is not ncessary
# after 1.12.0, use --ip-node-address to bind all ip in M1

# no need this, it should automatic : --num-cpus 6 --num-gpus 1 \
# --node-ip-address 0.0.0.0 
# --dashboard-host 0.0.0.0 

if [[ "$OSTYPE" == "darwin"* ]]; then
  # this setting valid only for Mac M1
  # Macos need explicit assign IP , otherwise remote cannot directly access
  ip=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}')
  gpus=1
  cpus=10
fi

if [[ "$OSTYPE" == "linux"* ]]; then
  ip=$(ip addr show eth0 |grep inet | grep -Fv inet6  | awk '{print $2}' | cut -d '/' -f 1)
  # this is for WSL runs in AMD ryzen 3700X
  cpus=8
  # current WSL GPU only support DirectML
  gpus=1
fi

echo "--num-cpus $cpus --num-gpus $gpus "

ray start --head --port 6379 \
     --node-ip-address $ip \
     --num-cpus $cpus --num-gpus $gpus \
     --include-dashboard true \
     --dashboard-host $ip \
     --dashboard-port 8265 \
     --block
     ### --autoscaling-config=~/ray_bootstrap_config.yaml

