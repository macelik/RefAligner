import os
import importlib
import json
import traceback
from configs import Configs

class Task:
    
    functionModuleMap = {"runCommand" : "tools.tools"}
    
    def __init__(self, taskType, outputFile, taskArgs, **kwargs):
        self.taskType = taskType
        self.outputFile = outputFile
        self.taskArgs = taskArgs
        
        for attr in kwargs:
            vars(self)[attr] = kwargs.get(attr)    
        self.attributes =  list(vars(self).keys())
        
        self.isFinished = False
        self.future = None
        self.json = self.toJson()   
    
    def submitTask(self):
        submitTasks([self])
    
    def awaitTask(self):
        awaitTasks([self])
        
    def submitAndAwaitTask(self):
        self.submitTask()
        self.awaitTask()
        
    def run(self):
        try:
            if not os.path.exists(self.outputFile):
                print("Running a task, output file: {}".format(self.outputFile))
                mod = importlib.import_module(Task.functionModuleMap[self.taskType])
                func = getattr(mod, self.taskType)
                func(**self.taskArgs)
                print("Completed a task, output file: {}".format(self.outputFile))
            else:
                print("File already exists: {}".format(self.outputFile))
        except Exception as exc:
            print("Task for {} threw an exception:\n{}".format(self.outputFile, exc))
            print(traceback.format_exc())
            raise
        finally:
            self.isFinished = True
        
    def checkFinished(self):
        if not self.isFinished:
            return False
        if self.future is not None:
            self.future.result()
        return True
        
    def toJson(self):
        mapper = {attr : getattr(self, attr) for attr in self.attributes}
        return json.dumps(mapper)
    
    def __eq__(self, other):
        if isinstance(other, Task):
            return self.outputFile == other.outputFile
        return NotImplemented

    def __hash__(self):
        return hash(self.outputFile)