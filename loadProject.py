### Load project

import csv
import glob
import os
import time

class LoadProject:
    def getProjects(self):
        txtfiles = []
        for file in glob.glob("*.csv"):
            txtfiles.append(file)
        return txtfiles


    def loadProject(self, csvfilename):
        with open(csvfilename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='\'')
            for row in spamreader:
                print(', '.join(row))
        path = os.getcwd()
        path = path + "\\" + projectName
        return path

    def newProject(self, projectName):
        csvfilename = projectName + '.csv'
        path = os.getcwd()
        path = path + "\\" + projectName

        # If path does not exist, create it
        if not os.path.isdir(path):
            os.mkdir(path)

        with open(csvfilename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",",
                            quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Caterpillar ID',
                                 'Leaf ID',
                                 'Caterpillar Instar',
                                 'Caterpillar Alive',
                                 'Date',
                                 'Time',
                                 'Leaf Area',
                                 'Notes'
                                 ,'Image'])
        txtfiles = []
        for file in glob.glob("*.csv"):
            txtfiles.append(file)


if __name__ == '__main__':
    lp = LoadProject()
    #image = cp.capturePic()

    txtfiles = lp.getProjects()
    if len(txtfiles) > 0:
        file = txtfiles[0]
        lp.loadProject(file)
