### Load project

import csv
import glob
import os

class LoadProject:
    def getProjects(self):
        txtfiles = []
        for file in glob.glob("*.csv"):
            txtfiles.append(file)

        return txtfiles


    def loadProject(self, projectName):
        with open(projectName, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='\'')
            for row in spamreader:
                print(', '.join(row))

    def newProject(self, projectName):
        path = os.getcwd()
        path = path + "\\" + projectName
        print ("The current working directory is %s" % path)
        print(os.path.isdir(path))