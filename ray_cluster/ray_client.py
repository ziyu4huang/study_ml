import ray 
import os
ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
# execute ../start_ray.sh  first before run this python code
# [See Tutorial](https://docs.ray.io/en/latest/cluster/ray-client.html#ray-client)

if False:
    # this only work when client run same machine as HEAD cluster 
    # aka for develop ease of use only
    ray.init(address="auto")
else:
    print("ipv4 on same cluster", ipv4)
    ray_conn = f"ray://{ipv4}:10001"
    print("connect to ray", ray_conn)
    ray.init(ray_conn)


# Normal Ray code follows
@ray.remote
def do_work(x):
    return x ** x

rs = do_work.remote(2)
print("remote do_work() return, refs",  rs)
print("remote do_work() return, value",  ray.get(rs))

