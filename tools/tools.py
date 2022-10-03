import subprocess
import os
import random
import shutil
import csv
from configs import Configs
from task.task import Task

def runCommand(**kwargs):
    command = kwargs["command"]
    print("Running usearch tool, command: {}".format(command))
    runner = subprocess.run(command, shell = True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:    
        runner.check_returncode()
    except:
        print("Command encountered error: {}".format(command))
        print("Exit code: {}".format(runner.returncode))
        print("Output: {}".format(runner.stdout))
        raise


def runUsearch(fastaPath, reference, outputPath, threads = 8):
    clustal = os.path.join(os.path.dirname(outputPath), "clustal_{}".format(os.path.basename(outputPath)))
    print(clustal)
    args = [Configs.usearchPath,"-usearch_global", fastaPath, "-db", reference, "-fulldp", "-id", "0"]
    args.extend(["-userfields", "query+qrow+trow","-show_termgaps", "-userout", clustal, "-threads", str(threads)])
    print(args)
    taskArgs = {"command" : subprocess.list2cmdline(args)}
    return Task(taskType = "runCommand", outputFile = outputPath, taskArgs = taskArgs)

def findIndels(target):
    return [str(pos) for pos, char in enumerate(target) if char == '-']

def rmIndelRef(seq,pos):
    return ''.join([ c for i, c in enumerate(seq) if str(i) not in pos])

def buildMSA(outputPath):
    clustal = os.path.join(os.path.dirname(outputPath), "clustal_{}".format(os.path.basename(outputPath)))
    
    with open(clustal, newline='') as tsvin, open(outputPath+'.fasta', 'w') as f:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            pos=findIndels(row[2])
            seq=rmIndelRef(row[1],pos)
            pos=list(map(lambda x: str(int(x) + 1), pos))
            header='>' + row[0] + ': ' + '/'.join(pos)
            f.write(header + '\n')
            f.write(seq + '\n')


def removeClustal(output):
    fname='clustal_' + output
    if os.path.exists(fname):
        os.remove(fname)
    else:
      print("The file does not exist")