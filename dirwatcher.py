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

# Global
exit_flag = False

# Logger
logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.DEBUG,
    # filename='logfile.log',
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT.
    Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main()
    will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    logger.warn('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def look_for_txt(filename, text, last_line):
    """Searches thru a file to see if it contains given text"""
    with open(filename, 'r') as rf:
        index = 0
        for index, line in enumerate(rf):
            if index >= last_line:
                if text in line:
                    logger.info(f'{text} found in {filename} '
                                f'at line {index + 1}')
        return index + 1


def watch_directory(directory, text, extension, interval):
    """"Watches a directory for given file/text combination"""
    logger.info(f'Watching directory: {directory} for files ending in '
                f'{extension} with text: {text}')
    watching_files = {}
    while not exit_flag:
        for filename in os.listdir(directory):
            if filename.endswith(extension) and filename not in watching_files:
                logger.info(f'{filename} is now being watched')
                watching_files[filename] = 0
        for filename in list(watching_files):
            if filename not in os.listdir(directory):
                watching_files.pop(filename)
                logger.info(f'{filename} has been removed from directory')
        for filename in watching_files:
            full_path = os.path.join(directory, filename)
            watching_files[filename] = look_for_txt(
                full_path, text, watching_files[filename])
        time.sleep(interval)


def create_parser():
    """Creates parser for taking in command line args"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext',
                        type=str,
                        default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval',
                        type=float,
                        default=1.0,
                        help='Number of seconda between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        f'{"-"*40}\n'
        f'Process ID: {os.getpid()}\n'
        f'Running {__file__}\n'
        f'Started: {app_start_time}\n'
        f'{"-"*40}\n'
    )
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while not exit_flag:
        try:
            # call my directory watching function..
            watch_directory(args.path, args.magic, args.ext, args.interval)
        except FileNotFoundError:
            logger.warning("Directory does not exist")
        except Exception:
            logger.exception('Unhandeled exception')
        finally:
            logger.warning('Attempting to stabilize program')
        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(3.0)
    uptime = datetime.datetime.now() - app_start_time
    logger.info(
        '\n'
        f'{"-"*40}\n'
        f'Stopped: {__file__}\n'
        f'Uptime was: {uptime}\n'
        f'{"-"*40}\n'
    )
    logging.shutdown()


if __name__ == "__main__":
    main()
