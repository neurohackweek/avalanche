#!/usr/bin/env python3

'''
main.py: command line for avalanche
'''

from avalanche.avalanche import avalanche
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
    description="generate avalanches from fMRI file")
    parser.add_argument("--file", dest='file', help="fMRI 4D file", type=str, default=None)
    parser.add_argument("--thr", dest='thr', help="SD * thr will be the cutting threshold for point process calculation", type=int, default=1)
    parser.add_argument("--structure", dest='structure', help="Size of cluster location kernel", type=int, default=4)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    thr = args.thr
    structure = args.structure

    if args.file != None:
        avalanche(args.file, thr, structure)
    else:
        print('meeek! avalanche did not work, did you provide a file?')

if __name__ == '__main__':
    main()
