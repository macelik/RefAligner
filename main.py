#!/usr/bin/python3
import time
import argparse
import sys,os
from configs import buildConfigs, Configs
from tools import tools

def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return an open file handle

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise parser.error("%s is an invalid positive int value" % value)
    return ivalue


def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--sequences", type=lambda x: is_valid_file(parser, x),
                        help="Path to input unaligned sequences", required=True, default=None)

    parser.add_argument("-r", "--reference", type=lambda x: is_valid_file(parser, x),
                        help="Path to input unaligned sequences", required=True, default=None)

    parser.add_argument("-o", "--output", type=str,
                        help="Output alignment path", required=True)

    parser.add_argument("-t", "--numprocs", type=check_positive,
                        help="Number of processors to use (default: # 8)",
                        required=False, default=8)

    parser.add_argument("-f", "--id", type=float,
                        help="minimum sequence identity of a hit", required=False, default=0.7)
    
    return parser.parse_args()

parser = argparse.ArgumentParser(description="Multiple Sequence Aligner")
args = parseArgs()
sequences=args.sequences
reference=args.reference
outfile=args.output
threads=args.numprocs

def main():   
    
    startTime = time.time()
    buildConfigs(args)
    tools.runUsearch(sequences,reference,outfile,threads).run()
    tools.buildMSA(outfile)
    tools.removeClustal(outfile)
    endTime = time.time()
    print("KhanAligner finished in {} seconds..".format(endTime-startTime))

if __name__ == '__main__':
    main()
