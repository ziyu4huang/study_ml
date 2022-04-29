import requests
import json
import time
import os

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]

### THIS DONES NOT WORKS

# Submit job via RESET
resp = requests.post(
    f"http://{ipv4}8265/api/jobs/",
    json={
        "entrypoint": "echo hello",
        "runtime_env": {},
        "job_id": None,
        "metadata": {"job_submission_id": "123"}
    }
)
rst = json.loads(resp.text)
job_id = rst["job_id"]

# Query and poll for Job status

start = time.time()
while time.time() - start <= 10:
    resp = requests.get(
        f"http://{ipv4}:8265/api/jobs/{job_id}"
    )
    rst = json.loads(resp.text)
    status = rst["status"]
    print(f"status: {status}")
    if status in {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED}:
        break
    time.sleep(1)
