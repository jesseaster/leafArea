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


    def loadProject(self, csvfilename):
        with open(csvfilename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='\'')
            for row in spamreader:
                print(', '.join(row))

    def saveData(self, csvfilename, variables):
        with open(csvfilename, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",",
                            quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([variables[0],
                                variables[1],
                                variables[2],
                                variables[3],
                                variables[4],
                                variables[5],
                                variables[6],
                                variables[7],
                                variables[8],
                                variables[9]])

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
                                 'Notes',
                                 'Image',
                                 'Calibrated Image'
                                 ])

if __name__ == '__main__':
    lp = LoadProject()
    #image = cp.capturePic()

    txtfiles = lp.getProjects()
    if len(txtfiles) > 0:
        csvfilename = txtfiles[0]
        variables = ["1","2","3","Yes","07-05-2020","18.51","7","8","Project1\\07-05-2020.18.51Cat1Leaf2.png", "Project1\\07-05-2020.18.51Calibrated.png"]
        lp.loadProject(csvfilename)
        lp.saveData(csvfilename, variables)
        lp.loadProject(csvfilename)
