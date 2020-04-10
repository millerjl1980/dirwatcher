#!/usr/bin/env python

__author__ = "Justin Miller and demos from 3/25 and 4/10"

import sys
import logging
import datetime
import time
import argparse
import os
import signal

if(sys.version_info[0] < 3):
    raise RuntimeError('This program requires Python 3+')

#Global
exit_flag = False

#Logger
logger = logging.getLogger(__file__)
logging.basicConfig(
        level=logging.DEBUG,
        # filename='logfile.log',
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    logger.warn('Received ' + signal.Signals(sig_num).name)
    if v.startswith('SIG') and not v.startswith('SIG_'))
        logger.warn('Received ' + signames[sig_num])
    exit_flag = True

def build_watching_dict(dir, ext, watching_files):
    #Look at directory and get a list of files from it
    #Put files into watching_files dictionary if not already in
    #Log new files that are added to dictionary
    #Loop thru dictionary and compare to list of files in directory
    #If file is misssing from directory, remove from dictionary
    #Log file removed from directory
    watching_files = watching_files
    ext_match = []

    for filename in os.walk(dir):
        if ext in filename:
            ext_match.append(filename)
    for match in ext_match:
        break
    # for each file in directory with ext:
    #     if file not in directory:
    #         watching_files.append(file)
    #         log that file was added to watch list
    # for each file in watching_files:
    #     if file not in directory:
    #         watching_files.remove(file)
    #         log that file was removed from directory

    return watching_files
    
def look_for_txt(directory, magic_txt):
    #For all remaining files in dictionary, open each file at last line that was read from and look for "magic" text
    #Log any new magic words located
    #Update last postition of where you were in files

    # for each entry in directory:
    #     pattern = r'magic_txt'
    #     last_line = directory[line]
    #     with (each) open as rf:
    #         start with last line +1
    #         word_found = re.complile(pattern)
    #         if word_found:
    #             log out
    #             directory[file]: line Update
    #         else:
    #             directory[file]: line update to last line read
    pass
    


def watch_directory(args):
    watching_files: {}
    logger.info(f'Watching directory: {args.path}, File Extention: '
                f'{args.ext}, Polling Interval: {args.interval}, '
                f'Magic Text: {args.magic}')
    #Keys are actual filenames and values are last line in file read
    while True:
        try:
            logger.info('Inside Watch Loop')
            watching_files = build_watching_dict(args.path, args.ext, watching_files)
            look_for_txt(watching_files, args.magic)
            time.sleep(args.interval)
        except KeyboardInterrupt:
            break

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float,
                        default=1.0, help='Number of seconda between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '------------------------------------------------------\n'
        '     Running {0}\n'
        '     Started on {1}\n'
        '------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    # Hook these two signals from the OS .. 
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my process.\
    while not exit_flag:
        try:
            # call my directory watching function..
            watch_directory(args)
            logger.debug("Watching directory")
        except FileNotFoundError:
            logger.warning("Directory does not exist")
        except Exception:
            logger.exception('Unhandeled exception')
        finally:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.warning('Attempting to stabilize program')
        time.sleep(5.0)

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(args.interval)
    
    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start.
    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '------------------------------------------------------\n'
        '     Stopped {0}\n'
        '     Uptime was {1}\n'
        '------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )
    logging.shutdown()

if __name__ == "__main__":
    main()