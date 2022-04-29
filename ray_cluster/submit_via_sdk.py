from ray.job_submission import JobSubmissionClient
import os

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]

# If using a remote cluster, replace 127.0.0.1 with the head node's IP address.
#client = JobSubmissionClient("http://127.0.0.1:8265")
client = JobSubmissionClient(f"http://{ipv4}:8265")


job_id = client.submit_job(
    # Entrypoint shell command to execute
    entrypoint="python ray_job_submit.py",
    # Runtime environment for the job, specifying a working directory and pip package
    runtime_env={
        "working_dir": "./",
        "pip": ["requests==2.26.0"]
    }
)


# here is where example comes from:
# https://docs.ray.io/en/latest/cluster/job-submission.html#jobs-overview

from ray.job_submission import JobStatus
import time

def wait_until_finish(job_id):
    start = time.time()
    timeout = 5
    while time.time() - start <= timeout:
        status = client.get_job_status(job_id)
        print(f"status: {status}")
        if status in {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED}:
            break
        time.sleep(1)


wait_until_finish(job_id)
logs = client.get_job_logs(job_id)

print("result of logs", logs)
