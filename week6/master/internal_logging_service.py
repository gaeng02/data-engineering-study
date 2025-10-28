from datetime import datetime
import json
import os

class InternalLoggingService :
    
    LOG_FILE = "internal.log"
    
    @staticmethod
    def log_api_call(
        endpoint: str,
        caller_info: dict,
        caller_name: str = None
    ):

        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "endpoint": endpoint,
                "caller_info": caller_info,
                "caller_name": caller_name
            }
            
            with open(InternalLoggingService.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                
        except Exception as e:
            print(f"Internal logging failed: {e}")
    
    @staticmethod
    def get_internal_logs (limit: int = 100) :
        logs_data = []
        
        try:
            if not os.path.exists(InternalLoggingService.LOG_FILE):
                return logs_data
            
            with open(InternalLoggingService.LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            lines.reverse()
            lines = lines[:limit]
            
            for line in lines:
                line = line.strip()
                if line:
                    try:
                        log_entry = json.loads(line)
                        logs_data.append(log_entry)
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"Failed to read internal logs: {e}")
        
        return logs_data
