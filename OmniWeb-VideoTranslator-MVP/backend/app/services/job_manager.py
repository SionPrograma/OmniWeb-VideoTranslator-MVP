import uuid
from typing import Dict, Any, List
from datetime import datetime

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    def create_job(self) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "status": "pending",
            "stage": "initialization",
            "percent": 0.0,
            "message": "Job created",
            "progress_history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "result_url": None,
            "error": None
        }
        return job_id

    def update_job(self, job_id: str, stage: str, percent: float, message: str, result_url: str = None, error: str = None):
        if job_id not in self.jobs:
            return
        
        job = self.jobs[job_id]
        job["updated_at"] = datetime.now().isoformat()
        job["stage"] = stage
        job["percent"] = percent
        job["message"] = message
        
        # Log to history
        job["progress_history"].append({
            "stage": stage,
            "percent": percent,
            "message": message,
            "timestamp": job["updated_at"]
        })
            
        if result_url:
            job["result_url"] = result_url
            
        if error:
            job["error"] = error
            job["status"] = "failed"
            # Note: We keep the 'percent' at its last value for debugging
        elif percent == 100 and stage == "complete":
            job["status"] = "completed"
        else:
            job["status"] = "processing"

    def get_job(self, job_id: str) -> Dict[str, Any]:
        job = self.jobs.get(job_id)
        if not job:
            return None
        return {
            "job_id": job_id,
            "status": job["status"],
            "stage": job["stage"],
            "percent": job["percent"],
            "message": job["message"],
            "result_url": job["result_url"],
            "error": job["error"]
        }

job_manager = JobManager()
