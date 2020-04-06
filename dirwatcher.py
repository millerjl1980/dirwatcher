#!/usr/bin/env python

__author__ = "Justin Miller and demo from 3/25"

import sys
import logging
import datetime
import time
import argparse
import os


if(sys.version_info[0] < 3):
    raise RuntimeError('This program requires Python 3+')

logger = logging.getLogger(__file__)

def find_magic(filename, starting_line, magic_word):
    pass

def watch_directory(args):
    watching_files: {}
    logger.info('Watching directory: {}, File Extention: {}, Polling Interval: {}, Magic Text: {}'.format(
        args.path, args.ext, args.interval, args.magic
    ))
    #Keys are actual filenames and values are last line in file read
 
    #Look at directory and get a list of files from it
    #Put files into watching_files dictionary if not already in
    #Log new files that are added to dictionary
    #Loop thru dictionary and compare to list of files in directory
    #If file is misssing from directory, remove from dictionary
    #For all remaining files in dictionary, open each file at last line that was read from and look for "magic" text
    #Log any new magic words located
    #Update last postition of where you were in files

    while True:
        try:
            logger.info('Inside Watch Loop')
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
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '------------------------------------------------------\n'
        '     Running {0}\n'
        '     Started on {1}\n'
        '------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()
    watch_directory(args) 
    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '------------------------------------------------------\n'
        '     Stopped {0}\n'
        '     Uptime was {1}\n'
        '------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )




if __name__ == "__main__":
    main()