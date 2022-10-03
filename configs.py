import os
import time
from shutil import which
from sys import platform
import stat
from os.path import basename
from glob import glob

def retrieve_packaged_binary(p):
    if platform == "linux" or platform == "linux2":
        for executable in glob(os.path.dirname(p) + "/**/*",recursive=True):
            if not os.path.isfile(executable):
                continue
            os.chmod(executable, os.stat(p).st_mode | stat.S_IEXEC)
        return p
    else:
        return None

def find_binary(rel_default_path):
    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_default_path)
    return which(basename(rel_default_path)) or retrieve_packaged_binary(default_path)


class Configs:
    
    #workingDir = None
    sequencesPath = None
    outputPath = None
    refPath = None
    
    usearchPath = find_binary("tools/usearch")
    
    numCores = 8
    idThreshold = 0.7

def buildConfigs(args):
    Configs.outputPath = os.path.abspath(args.output)
    Configs.refPath = os.path.abspath(args.reference)

    
    #if args.directory is not None:
    #    Configs.workingDir = os.path.abspath(args.directory) 
    #else:
    #    Configs.workingDir = os.path.join(os.path.dirname(Configs.outputPath), "workdir")
    #if not os.path.exists(Configs.workingDir):
    #    os.makedirs(Configs.workingDir)
    #    print("created")
    
    Configs.sequencesPath = os.path.abspath(args.sequences) if args.sequences is not None else Configs.sequencesPath
    

    if args.numprocs > 0:
        Configs.numCores = args.numprocs
    else:
        Configs.numCores = 8


    Configs.idThreshold = args.id