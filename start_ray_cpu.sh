# pip-sync requirements.txt \
#   --pip-args --force-exclude-deps grpcio # not works
#pip-sync requirements.txt 

#ray start --head --port=6379
# [doc](https://docs.ray.io/en/latest/cluster/index.html)

# --address 0.0.0.0 # not used after 1.12.0 , now redis is not ncessary

ray start --head --port 6379 \
     --num-cpus 8 --num-gpus 0 \
     --include-dashboard true --dashboard-host 0.0.0.0 --dashboard-port 8265 \
     --block
##     --autoscaling-config  tune-default.yaml \
	
     ##--dashboard-host '0.0.0.0' --dashboard-port 8265 \
     ##--gcs-server-port 8075 --object-manager-port 8076 --node-manager-port 8077 
     ## --min-worker-port 10002 --max-worker-port 19999  
     ### --autoscaling-config=~/ray_bootstrap_config.yaml

