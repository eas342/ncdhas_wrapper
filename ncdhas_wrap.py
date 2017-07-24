import os
import numpy as np
from astropy.io import ascii
from astropy.io import fits
import glob
from subprocess import check_output
import subprocess
from copy import deepcopy
import yaml
import sys

progData = yaml.load(open('prog_files/prog_dirs.yaml'))
ncdhasApp      = progData['ncdhasCommand']

## Old legacy flags
# flags__MMM_stability   = '+cfg isimcv3 +ow +wi +wd +ws -rx +rc -rss +rsf +cbp +cs +cbs -cd +mf 2'
# flags_all = '+ow +wi +wd +ws -dr -cbp -cs -cbs -cd +mf 2 -ipc -cl -cf -cgm'

class ncFiles():
    def __init__(self,paramFile):
        """ An object to hold the file list and run NCDHAS on
        All .red, .dia, .slp, .cds and .txt files will be removed from the input
        """
        param = yaml.load(open(paramFile))
        
        self.inputFiles = param['inputFiles']
        self.fileDir = os.path.dirname(self.inputFiles)
        self.reduceDir = param['outputDir']
        for oneDir in [self.fileDir,self.reduceDir]:
            if os.path.exists(oneDir) == False:
                raise ValueError("Specified directory "+oneDir+" not found")
        
        fileList = glob.glob(self.inputFiles)
        
        ## ignore processed files
        ignoretypes = ['.red.','.dia.','.slp.','.cds.','.txt']
        useList = deepcopy(fileList)
        for onefile in fileList:
            for ignoretype in ignoretypes:
                if ignoretype in onefile:
                    useList.remove(onefile)
        self.fileList = useList
        
        self.flags = param['flags_all']

    def run_pipe(self):
        """ Runs the pipeline on the file list
        Starts by created a symbolic link to the original data
        """
        dirOutput = []
        for oneFile in self.fileList:
            ## Make a symbolic link to the ramp
            baseName = os.path.basename(oneFile)
            rampFile = self.reduceDir+baseName
            if os.path.exists(rampFile) == False:
                ## Only make a symlink if there isn't one there
                os.symlink(oneFile,rampFile)
            
            head = fits.getheader(rampFile)
            cmd = ncdhasApp + ' '+ rampFile + ' '+self.flags
            dirOutput.append('Command to be executed:')
            dirOutput.append(cmd)
        
            try:
                out = check_output(cmd,shell=True)
                dirOutput.append(out)
            except subprocess.CalledProcessError as e:
                saveout="command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output)
                dirOutput.append(saveout)
            except:
                saveout="Unknown error for command:"+cmd
                dirOutput.append(saveout)
                
        with open(self.reduceDir+'ncdhas_output.txt','w') as outputfile:
            for line in dirOutput:
                outputfile.write(line+'\n')

            


if __name__ == "__main__":
    """ Default command line run.
    Searches the command line for an input parameter file
    """
    if len(sys.argv) > 1:
        paramFile = sys.argv[1]
    else:
        paramFile = 'run_params/test_params.yaml'
    
    nc = ncFiles(paramFile)
    nc.run_pipe()
