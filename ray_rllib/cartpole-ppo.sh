
# https://github.com/ray-project/ray/blob/27917f570de3296ecf6c81fbe0cc318efd448b1b/rllib/tuned_examples/ppo/cartpole-ppo.yaml

ip="192.168.72.106"
#fixed

if [[ "$OSTYPE" == "darwin"* ]]; then
  # this setting valid only for Mac M1
  # Macos need explicit assign IP , otherwise remote cannot directly access
  ip=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}')
fi

ray_url="ray://${ip}:10001"
echo "connect to cluster-> ${ray_url}"

rllib train -f tuned_example/cartpole-ppo.yaml \
    --ray-address $ray_url
