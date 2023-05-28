#!/usr/bin/env python3

# Module for fetching information about an audio compact disc and
# returning it in a format friendly to CDDB.

# If called from the command line, will print out disc info in a
# format identical to Robert Woodcock's 'cd-discid' program.

# Written 17 Nov 1999 by Ben Gertzfield <che@debian.org>
# This work is released under the GNU GPL, version 2 or later.

# Release version 1.4
# CVS ID: $Id: DiscID.py,v 1.10 2003/08/31 23:19:45 che_fox Exp $

""" Adapted to Python3

(c)2023  Henrique Moreira
"""

# pylint: disable=missing-function-docstring

import sys
import cdrom


def main():
    dev_name = None
    device = None
    if len(sys.argv) >= 2:
        dev_name = sys.argv[1]
    if dev_name:
        device = open(dev_name)
    else:
        device = open()
    disc_info = disc_id(device)
    print('%08lx' % disc_info[0])

    for i in disc_info[1:]:
        print('%d' % i)
    return 0


def cddb_sum(n):
    ret = 0
    
    while n > 0:
        ret = ret + (n % 10)
        n = n / 10

    return ret

def open(device=None, flags=None):
    # Allow this function to be called with no arguments,
    # specifying that we should call cdrom.open() with
    # no arguments.
    if device is None:
        return cdrom.open()
    elif flags is None:
        return cdrom.open(device)
    else:
        return cdrom.open(device, flags)

def disc_id(device):
    (first, last) = cdrom.toc_header(device)

    track_frames = []
    checksum = 0

    for i in range(first, last + 1):
        (a_min, sec, frame) = cdrom.toc_entry(device, i)
        checksum = checksum + cddb_sum(a_min * 60 + sec)
        track_frames.append(a_min * 60 * 75 + sec * 75 + frame)

    (a_min, sec, frame) = cdrom.leadout(device)
    track_frames.append(a_min * 60 * 75 + sec*75 + frame)

    total_time = (track_frames[-1] / 75) - (track_frames[0] / 75)
	       
    discid = ((checksum % 0xff) << 24 | total_time << 8 | last)

    lst = [discid, last] + track_frames[:-1] + [track_frames[-1] / 75]
    return lst

if __name__ == '__main__':
    main()
