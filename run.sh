#!/bin/bash

source venv/bin/activate

URL="${1}"
USERNAME="${2}"
PASSWORD="${3}"

python3 app.py --action "default" --log-level "DEBUG" --target "${URL}" --username "${USERNAME}" --password "${PASSWORD}"
python3 app.py --action "all_jobs" --log-level "DEBUG" --target "${URL}" --username "${USERNAME}" --password "${PASSWORD}"
python3 app.py --action "all_job_results" --log-level "DEBUG" --target "${URL}" --username "${USERNAME}" --password "${PASSWORD}"

deactivate
