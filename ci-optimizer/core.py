# core.py

from prompt import extract_details, create_prow_job

# Example prompt to test the function
prompt_text = "I want to run unit-tests.sh twice a day using 4000ms CPU"
script_name, cpu_time, frequency = extract_details(prompt_text)

print(f"Script Name: {script_name}")
print(f"CPU Capacity: {cpu_time}")
print(f"Frequency (crontab format): {frequency}")
prow_job_yaml = create_prow_job(script_name, cpu_time, frequency)

# Save YAML to a file
with open("prowjob.yaml", "w") as file:
    file.write(prow_job_yaml)
