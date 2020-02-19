#!/usr/local/bin/python3
import json, os, sys, argparse, subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', required=True)
    parser.add_argument('-q', '--queueprefix', default='')
    parser.add_argument('-x', '--execute', default=False, action='store_true')
    args = parser.parse_args()
    sqsUrls = getQueueUrls(args.profile, args.queueprefix)
    deleteQueues(sqsUrls, args.profile, args.execute)


def deleteQueues(sqsUrls, profile, executeCommand):
    queueCounter = 0
    for url in sqsUrls:
        cmd = 'aws-vault exec ' + profile + ' -- aws sqs delete-queue --queue-url ' + url
        print(cmd)
        if executeCommand == True:
            queueCounter += 1
            os.system(cmd)

    if executeCommand == False:
        print('Execution skipped (Dryrun)')
    else:
        print('Total API calls executed: ' +  str(queueCounter))

def getQueueUrls(profile, queueNamePrefix=''):
    cmd = 'aws-vault exec ' + profile + ' -- aws sqs list-queues'
    if queueNamePrefix != '':
        cmd += ' --queue-name-prefix ' + queueNamePrefix
    
    try:
        print('Running: \n' + cmd)
        completedProcess = subprocess.run(cmd, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as error:
        print('Loading of queues failed with msg: ', error.stderr)
        sys.exit(1)
    
    try:
        queues = json.loads(completedProcess.stdout)
    except json.JSONDecodeError as error:
        print('Could not decode json: ', error.msg)
        sys.exit(1)

    return queues['QueueUrls']


if __name__ == "__main__":
    main()
