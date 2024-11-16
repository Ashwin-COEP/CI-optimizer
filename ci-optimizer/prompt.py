import re
import yaml

def create_prow_job(script_name, cpu_time, cron_schedule):
    prow_job = {
        "apiVersion": "prow.k8s.io/v1",
        "kind": "ProwJob",
        "metadata": {
            "name": f"{script_name.replace('.sh', '')}-job",
            "labels": {
                "preset-job": "true"
            }
        },
        "spec": {
            "agent": "kubernetes",
            "cluster": "default",
            "namespace": "test-pods",
            "job": "periodic",
            "cron": cron_schedule,
            "pod_spec": {
                "containers": [
                    {
                        "name": script_name,
                        "image": "busybox",  # Replace with an appropriate image
                        "command": ["/bin/sh"],
                        "args": ["-c", f"./{script_name}"],
                        "resources": {
                            "limits": {
                                "cpu": cpu_time,
                                "memory": "512Mi"
                            },
                            "requests": {
                                "cpu": cpu_time,
                                "memory": "256Mi"
                            }
                        }
                    }
                ]
            }
        }
    }
    return yaml.dump(prow_job, sort_keys=False)

# Example Usage
# script_name = "unit-tests.sh"
# cpu_time = "4000ms"
# cron_schedule = "0 * * * *"  # Replace with the appropriate crontab schedule
# prow_job_yaml = create_prow_job(script_name, cpu_time, cron_schedule)
# print(prow_job_yaml)

def convert_to_crontab(frequency_text):
    # Define mappings from natural language to crontab format
    frequency_mapping = {
        "once an hour": "0 * * * *",
        "every hour": "0 * * * *",
        "every 2 hours": "0 */2 * * *",
        "every day": "0 0 * * *",
        "once a day": "0 0 * * *",
        "once a week": "0 0 * * 0",
    }

    # Lowercase the text and search for matching phrase
    frequency_text = frequency_text.lower()
    for key, crontab_format in frequency_mapping.items():
        if key in frequency_text:
            return crontab_format

    # Return None if no match found
    return "Unknown frequency"

def extract_details(prompt):
    # Regular expression to extract script name (e.g., unit-test.sh, backup.sh)
    script_pattern = r"(?:script\s+.*?\s+)?([a-zA-Z0-9\-_\.]+\.sh)"

    # Updated regular expression to capture CPU capacity with flexible structure
    cpu_pattern = r"(?:using\s+)?(\d+(?:\.\d+)?\s*(GHz|MHz|ms|cores?))(?:\s*CPU)?"
    
    # Regular expression to capture frequency in natural language
    frequency_pattern = r"(every\s+\d+\s+(?:minute|hour|day|week)s?|once\s+an\s+hour|twice\s+a\s+day|every\s+hour|every\s+day)"
    
    # Search for the script name
    script_match = re.search(script_pattern, prompt, re.IGNORECASE)
    script_name = script_match.group(1) if script_match else "Unknown Script"
    
    # Search for CPU capacity
    cpu_match = re.search(cpu_pattern, prompt, re.IGNORECASE)
    cpu_capacity = cpu_match.group(1) if cpu_match else "Unknown CPU capacity"
    
    # Search for frequency of the run
    frequency_match = re.search(frequency_pattern, prompt, re.IGNORECASE)
    frequency_text = frequency_match.group(0) if frequency_match else "Unknown frequency"
    
    # Convert natural language frequency to crontab format
    crontab_frequency = convert_to_crontab(frequency_text) if frequency_text != "Unknown frequency" else frequency_text

    # Return extracted details
    return script_name, cpu_capacity, crontab_frequency
