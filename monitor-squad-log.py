import os
import sys

closed_log_files = []

def GetNewBackupLogs(log_dir):
    global closed_log_files
    for filename in sorted(os.listdir(log_dir)):
        if filename.startswith('Squad-backup-'):
            if filename not in closed_log_files:
                closed_log_files.append(filename)
                yield filename

def main():
    if len(sys.argv) != 2:
        print 'ERROR: Wrong number of command-line arguments.'
        print 'USAGE: python monitor-squad-log.py <log-dir>'
        return
    log_dir = sys.argv[1]
    if not os.path.isdir(log_dir):
        print 'ERROR:', log_dir, 'is not a directory.'
        return
    print 'monitoring', log_dir
    for filename in GetNewBackupLogs(log_dir):
        print 'Back-processing:', filename
    current_log = os.path.join(log_dir, 'Squad.log')
    if os.path.isfile(current_log):
        print 'Processing:', current_log

if __name__ == "__main__":
    main()
