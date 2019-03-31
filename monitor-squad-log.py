import os
import re
import sys
import time

# A list of log filenames that have already been fully processed.
closed_log_files = []

# The maximum timestamp encountered so far.
max_timestamp = None

def ProcessLogLine(line):
    global max_timestamp
    m = re.match(r'\[(.*?)\:(\d+)\]\[(.*?)\](.*)', line)
    if not m:
        # Bail if the log line does not match the expected pattern.
        return
    timestamp = m.group(1)
    try:
        time.strptime(timestamp, '%Y.%m.%d-%H.%M.%S')
    except:
        # Bail if the timestamp isn't valid.
        return
    milliseconds = m.group(2)
    timestamp = timestamp + ':' + milliseconds
    unknown_number = m.group(3)
    log_message = m.group(4)
    if timestamp > max_timestamp:
        max_timestamp = timestamp
        print timestamp, log_message

def ProcessLogFile(filename):
    with open(filename) as f:
        for line in f:
            ProcessLogLine(line)

def GetNewBackupLogs(log_dir):
    global closed_log_files
    for filename in sorted(os.listdir(log_dir)):
        if filename.startswith('Squad-backup-'):
            if filename not in closed_log_files:
                closed_log_files.append(filename)
                yield filename

def Monitor(log_dir):
    print 'Monitoring', log_dir
    for filename in GetNewBackupLogs(log_dir):
        print 'Back-processing:', filename
        ProcessLogFile(os.path.join(log_dir, filename))
    current_log = os.path.join(log_dir, 'Squad.log')
    if os.path.isfile(current_log):
        print 'Processing', current_log
        ProcessLogFile(current_log)
    print 'Done'

def main():
    if len(sys.argv) != 2:
        print 'ERROR: Wrong number of command-line arguments.'
        print 'USAGE: python monitor-squad-log.py <log-dir>'
        return
    log_dir = sys.argv[1]
    if not os.path.isdir(log_dir):
        print 'ERROR:', log_dir, 'is not a directory.'
        return
    while True:
        Monitor(log_dir)
        time.sleep(60)

if __name__ == "__main__":
    main()
