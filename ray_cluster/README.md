
# example of running start_ray.sh 

```shell

(tf1dml) ziyu4huang@ziyuxt3700:~/proj/study_ml$ source start_ray.sh
Usage stats collection will be enabled by default in the next release. See https://github.com/ray-project/ray/issues/20857 for more details.
Local node IP: 172.23.26.224
2022-04-30 05:33:34,689 INFO services.py:1462 -- View the Ray dashboard at http://172.23.26.224:8265

--------------------
Ray runtime started.
--------------------

Next steps
  To connect to this Ray runtime from another node, run
    ray start --address='172.23.26.224:6379'

  Alternatively, use the following Python code:
    import ray
    ray.init(address='auto')

  To connect to this Ray runtime from outside of the cluster, for example to
  connect to a remote cluster from your laptop directly, use the following
  Python code:
    import ray
    ray.init(address='ray://<head_node_ip_address>:10001')

  If connection fails, check your firewall settings and network configuration.

  To terminate the Ray runtime, run
    ray stop

--block
  This command will now block until terminated by a signal.
  Running subprocesses are monitored and a message will be printed if any of them terminate unexpectedly.


```

# then try to run ray_client here.

[See Tutorial](https://docs.ray.io/en/latest/cluster/ray-client.html#ray-client)

> python ray_client.py

# Versioning Requirements

Versioning requirements
Generally, the client Ray version must match the server Ray version. 
An error will be raised if an incompatible version is used.

Similarly, the minor Python (e.g., 3.6 vs 3.7) must match between the client and server. 
An error will be raised if this is not the case.

#Ray client logs
Ray client logs can be found at /tmp/ray/session_latest/logs on the head node.



# Ray Job Submission Architecture

The following diagram shows the underlying structure and steps for each submitted job.
![Image ARchi](https://raw.githubusercontent.com/ray-project/images/master/docs/job/job_submission_arch_v2.png)


