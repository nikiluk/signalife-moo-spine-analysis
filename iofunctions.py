#
# functions to process file loading and data manipulation

import datetime
import os
import numpy as np
import pandas as pd


def list_files(path,ext):
    # returns a list of names (with extension, without full path) of all files
    # in folder path ext could be '.txt'
    #

    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if ext in name:
                files.append(name)
    return files

def printDate():
    # returns the string with the current date/time in minute
    # example output '2016-05-23_16-31'

    printDate =  datetime.datetime.now().isoformat().replace(":", "-")[:16].replace("T", "_")
    return printDate

def outputFile(fileName, projectFolder=os.getcwd(), folderSuffix='_output'):
    # creates the output folder with current datetime and returns the path url for the file to be used further
    outputFolder = os.path.join(projectFolder, printDate() + folderSuffix)
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    outputFile = os.path.join(outputFolder, fileName)
    return outputFile




def intensityThresholding(inputProfile, intensityColumn='intensity', intensityThreshold=0):
    #drop rows with intensity les than threshold

    inputProfile = inputProfile[inputProfile[intensityColumn] > intensityThreshold]
    outputProfile = inputProfile.reset_index(drop=True)

    return outputProfile



def genotyping(imageName):
    #depending on imageName returns the genotype string

    #genotype filtering
    list_WT = ['f-f_cre-neg','f-p_cre-neg','p-p_cre-neg','p-p_cre-pos']
    list_CKO = ['f-f_cre-pos']
    list_HTZ = ['f-p_cre-pos']


    if any(ext in str(imageName) for ext in list_CKO):
        return 'CKO'
    if any(ext in str(imageName) for ext in list_WT):
        return 'WT'
    if any(ext in str(imageName) for ext in list_HTZ):
        return 'HTZ'