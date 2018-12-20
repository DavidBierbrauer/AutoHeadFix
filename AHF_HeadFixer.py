#! /usr/bin/python3
#-*-coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import os
import inspect

class AHF_HeadFixer(metaclass = ABCMeta):
    """
    Base class for all head fix classs. Other head fixers subclass from this, or from one of its subclasses
    boolean for settability of headFixing levels, default is False. Can be used for incremental learning
    """
    hasLevels = False
    
    ##################################################################################
    # Static methods for base class for getting class names and importing classes
    @staticmethod
    def get_class(fileName):
        """
        Imports a module from a fileName (stripped of the .py) and returns the class

        Assumes the class is named the same as the module. 
        """
        module = __import__(fileName)
        return getattr(module, fileName)


    @staticmethod
    def get_HeadFixer_from_user ():
        """
        Static method that trawls through current folder looking for HeadFixer class python files
        
        Allows user to choose from the list of files found. Files are recognized by names starting
        with 'AHF_HeadFixer_' and ending with '.py'
        Raises: FileNotFoundError if no stimulator class files found
        """
        iFile=0
        files = ''
        #print (os.listdir(os.curdir))
        for f in os.listdir(os.curdir):
            if f.startswith ('AHF_HeadFixer_') and f.endswith ('.py'):
                f= f.rstrip  ('.py')
                #print ('file = ' + str (f))
                try:
                    moduleObj=__import__ (f)
                    #print ('module=' + str (moduleObj))
                    classObj = getattr(moduleObj, moduleObj.__name__)
                    #print ('class obj = ' + str (classObj))
                    isAbstractClass =inspect.isabstract (classObj)
                    if isAbstractClass == False:
                        if iFile > 0:
                            files += ';'
                        files += f
                        iFile += 1
                except Exception as e: # exception will be thrown if imported module imports non-existant modules, for instance
                    print (e)
                    continue     
        if iFile == 0:
            print ('Could not find any AHF_HeadFixer_ files in the current or enclosing directory')
            raise FileNotFoundError
        else:
            if iFile == 1:
                headfixFile =  files.split('.')[0]
                print ('Head Fixer file found: ' + headfixFile)
                headfixFile =  files.split('.')[0]
            else:
                inputStr = '\nEnter a number from 0 to ' + str (iFile -1) + ' to Choose a HeadFixer class:\n'
                ii=0
                for file in files.split(';'):
                    inputStr += str (ii) + ': ' + file + '\n'
                    ii +=1
                inputStr += ':'
                headfixNum = -1
                while headfixNum < 0 or headfixNum > (iFile -1):
                    headfixNum =  int(input (inputStr))
                headfixFile =  files.split(';')[headfixNum]
                headfixFile =  headfixFile.split('.')[0]
            return headfixFile

    ##################################################################################
    #abstact methods each headfixer class must implement
    #part 1: three main methods of initing, fixing, and releasing
    @abstractmethod
    def __init__(self, settingsDict):
        """
        hardware initialization of a headFixer, reading data from the task object
        """
        pass

    @abstractmethod
    def setup (self):
        """
        does hardware initialization of a headFixer with (possibly updated) info in self.settingsDict
        """
        pass
        

    @abstractmethod
    def fixMouse(self):
        """
        performs head fixation by energizing a piston, moving a servomotor, etc
        """
        pass
    
    @abstractmethod
    def releaseMouse(self):
        """
        releases mouse from head fixation by relaxing a piston, moving a servomotor, etc
        """
        pass

    ##################################################################################
    #abstact methods each headfixer class must implement
    #part 2: static function for getting ConfigDict from user


    @staticmethod
    @abstractmethod
    def config_user_get ():
        """
        in absence of json configDict, querries user for settings, and returns a dictionary with settings
        """
        pass


    

    ##################################################################################
    #abstract methods each headfixer class must implement
    #part 3: hadware tester function
    @abstractmethod
    def test(self, task):
        """
        Called by hardwaretester, runs a harware test for headFixer, verifying that it works
        gives user a chance to change configuration, and, if changed, saves new configuration info in headFixer dictionary in task
        """
        pass

    ###################################################################################
    # methods a headFixer will implement if it hasLevels
    # we pass the current level of a particular mouse and level up before head fixing
    # we save the returned new value in the mouse object, for next time

    def level_get_start (self):
        return 0
    
    def level_up (self, baseValue):
        return baseValue + 0

    def level_down (self, baseValue):
        return baseVaue - 0

    def level_set_level (self, level):
        pass

    ##################################################################################
    # a simple function to run when run as Main, for all head fixers
    @staticmethod
    def funcForMain ():
        from time import sleep
        from AHF_HeadFixer 
        from AHF_Task import AHF_Task
        task = AHF_Task(None)
        task.edit()
        task.save()
        headFixer=AHF_HeadFixer.get_class (task.headFixerClass) (task.headFixerDict)
        print ('Released Position')
        headFixer.releaseMouse()
        sleep (1)
        print ('Fixed Position')
        headFixer.fixMouse()
        sleep (1)
        print ('Released Position')
        headFixer.releaseMouse()


if __name__ == "__main__":
    AHF_HeadFixer.funcForMain()

