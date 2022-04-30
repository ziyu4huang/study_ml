# run https://github.com/ray-project/ray/blob/cfc192ebc464ceac77904e7b67cdbe9910876a74/rllib/tuned_examples/a3c/pong-a3c.yaml
# this works on M1/GPU 

ip="192.168.72.106"
#fixed

if [[ "$OSTYPE" == "darwin"* ]]; then
  # this setting valid only for Mac M1
  # Macos need explicit assign IP , otherwise remote cannot directly access
  ip=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}')
fi

ray_url="ray://${ip}:10001"
echo "connect to cluster-> ${ray_url}"

rllib train -f tuned_example/cartpole-dqn.yaml \
    --ray-address $ray_url
