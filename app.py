import argparse
import requests
import json
import time
import os
import logging

# Disable the warnings about certificates
requests.packages.urllib3.disable_warnings()

# NOTES
# last query time
# get jobs

def get_request(url, user, password, parameters={}):
    try:
        r = requests.get(url, params=parameters, allow_redirects=False, verify=False, timeout=30, auth=(user, password))
        return r
    except requests.exceptions.RequestException as e:
        logging.error(e)

def get_jobs(ip, user, password):
    url = f'https://{ip}/jobs.json'
    results = json.loads(get_request(url, user, password).text)
    return results

def get_job_results(ip, user, password, job_id):
    url = f'https://{ip}/jobs/{job_id}.json'
    results = json.loads(get_request(url, user, password).text)
    return results

def action_default(args):
    logging.error('UNKNOWN ACTION')

def action_all_jobs(args):
    jobs = get_jobs(args.target, args.username, args.password)
    output_filename = f'{args.dataDir}/jobs.json'
    if not os.path.exists(output_filename) or args.clobber:
        with open(output_filename, 'w') as jf:
            logging.info(f'Writing to {output_filename}')
            logging.debug(json.dumps(jobs, indent=1))
            jf.write(json.dumps(jobs, indent=1))
    else:
        logging.info('jobs.json already exists. Skipping.')

def action_all_job_results(args):
    jobs = get_jobs(args.target, args.username, args.password)
    for job in jobs:
        logging.info(f"Fetching info for job #{job['id']}")
        logging.debug(f'JOB: {job}')
        output_filename = f"{args.dataDir}/jobs/{job['id']}.json"
        os.makedirs(f'{args.dataDir}/jobs/', exist_ok=True)
        if not os.path.exists(output_filename) or args.clobber:
            with open(output_filename, 'w') as jf:
                logging.info(f'Writing to {output_filename}')
                results = get_job_results(args.target, args.username, args.password, job['id'])
                logging.debug(json.dumps(results, indent=1))
                jf.write(json.dumps(results, indent=1))
        else:
            logging.info(f"Job #{job['id']} already exists. Skipping.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username')
    parser.add_argument('-p', '--password', dest='password')
    parser.add_argument('-t', '--target', dest='target', help='Enter the URL or IP address.')
    parser.add_argument('-a', '--action', dest='actionName', default='default', help='Select which action to run.')
    parser.add_argument('-d', '--data-dir', dest='dataDir', default='data', help='Set the output directory for data download.')
    parser.add_argument('-l', '--log-level', dest='logLevel', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level')
    parser.add_argument('-c', '--clobber', action='store_true', default=False, help='Overwrite existing files.')
    args = parser.parse_args()

    if args.logLevel:
        logging.basicConfig(level=getattr(logging, args.logLevel))

    os.makedirs(args.dataDir, exist_ok=True)

    locals().get(f'action_{args.actionName}', action_default)(args)
