#!/usr/local/bin/python3
import json
import os
import argparse

def main(inputFile, profile, executeCommand):
    with open(inputFile, 'r') as file:
        sqsQueues = json.load(file)

    queueCounter = 0
    for url in sqsQueues['QueueUrls']:
        cmd = 'aws-vault exec ' + profile + ' -- aws sqs delete-queue --queue-url ' + url
        print(cmd)
        if executeCommand == True:
            queueCounter += 1
            os.system(cmd)

    if executeCommand == False:
        print('Execution skipped (Dryrun)')
    else:
        print('Total API calls executed: ' +  str(queueCounter))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', required=True)
    parser.add_argument('-p', '--profile', required=True)
    parser.add_argument('-x', '--execute', default=False, action='store_true')
    args = parser.parse_args()
    main(args.inputfile, args.profile, args.execute)
