#!/usr/bin/env python

__author__ = "Justin Miller"

import sys
import logging
import datetime


if(sys.version_info[0] < 3):
    raise RuntimeError('This program requires Python 3+')

logger = logging.getLogger(__file__)

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