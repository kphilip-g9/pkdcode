import docker
import json
import os
import tempfile
from multiprocessing import Process, Queue

client = docker.from_env()

def run_container_worker(payload: dict, queue: Queue, memory_limit_mb: int):
    container = None
    
    with tempfile.TemporaryDirectory() as tmpdir:
        payload_path = os.path.join(tmpdir, "payload.json")
        
        with open(payload_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)

        try:
            container = client.containers.run(
                image="python-judge-sandbox",
                command=["python", "runner.py", "/app/data/payload.json"],
                volumes={tmpdir: {'bind': '/app/data', 'mode': 'ro'}},
                network_disabled=True,
                mem_limit=f"{memory_limit_mb}m",
                nano_cpus=1000000000,
                detach=True
            )

            result = container.wait()
            exit_code = result.get("StatusCode", 0)

            if exit_code == 137:
                queue.put({"status": "MLE", "message": "Memory Limit Exceeded"})
                return

            logs = container.logs(stdout=True, stderr=False).decode('utf-8').strip()
            
            if not logs:
                queue.put({"status": "RTE", "message": "Runtime Error: Isolation wrapper closed empty."})
            else:
                queue.put(json.loads(logs))

        except Exception as e:
            queue.put({"status": "SE", "message": f"System Error Exception context: {str(e)}"})
            
        finally:
            if container:
                try:
                    container.remove(force=True)
                except:
                    pass

def execute_in_sandbox(payload: dict, time_limit_seconds: float = 2.0, memory_limit_mb: int = 64) -> dict:
    queue = Queue()
    
    worker_process = Process(target=run_container_worker, args=(payload, queue, memory_limit_mb))
    worker_process.start()

    worker_process.join(timeout=time_limit_seconds)

    if worker_process.is_alive():
        worker_process.terminate()
        worker_process.join()
        return {"status": "TLE", "message": "Time Limit Exceeded"}

    if not queue.empty():
        return queue.get()
        
    return {"status": "SE", "message": "System Error: Background execution engine timed out structural trackers."}

if __name__ == "__main__":
    cf_payload = {
        "style": "codeforces",
        "code": "import time\nwhile True: pass",
        "test_cases": [{"input": "1 2\n", "expected": "3\n"}]
    }
    
    lc_payload = {
        "style": "leetcode",
        "method_name": "twoSum",
        "code": "class Solution:\n    def twoSum(self, nums: list, target: int) -> list:\n        return [0, 1]",
        "test_cases": [{"args": ([2, 7, 11, 15], 9), "expected": [0, 1]}]
    }

    print("--- [VERIFICATION STAGE 1] Running Codeforces Infinite Loop Simulator ---")
    print("Verdict:", execute_in_sandbox(cf_payload, time_limit_seconds=1.5))
    
    print("\n--- [VERIFICATION STAGE 2] Running LeetCode Optimal Match Simulator ---")
    print("Verdict:", execute_in_sandbox(lc_payload, time_limit_seconds=2.0))
