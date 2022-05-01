# run https://github.com/ray-project/ray/blob/cfc192ebc464ceac77904e7b67cdbe9910876a74/rllib/tuned_examples/a3c/pong-a3c.yaml
# this works on M1/GPU 

ip="127.0.0.1"

if [[ "$OSTYPE" == "darwin"* ]]; then
  # this setting valid only for Mac M1
  # Macos need explicit assign IP , otherwise remote cannot directly access
  ip=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}')
fi

if [[ "$OSTYPE" == "linux"* ]]; then
  ip=$(ip addr show eth0 |grep inet | grep -Fv inet6  | awk '{print $2}' | cut -d '/' -f 1)
  # this is for WSL runs in AMD ryzen 3700X
  cpus=8
  # current WSL GPU only support DirectML
  gpus=1

fi

ray_url="ray://${ip}:10001"
echo "connect to cluster-> ${ray_url}"

rllib train -f tuned_example/cartpole-dqn.yaml \
    --ray-address $ray_url
