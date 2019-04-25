'''
Utility for rendering sequence of hip files (aka Deadline Render)

For each new render shot row in table:
    - looks into the project.json database and HDD (render dir, render hips) to get parameters (shotItemParams),
    - populate parameters to UI and save them in render.json database

Stop on setup Folder button (openFolder())

'''

import hou
import json
import glob
import os
from EVE.dna import dna
from PySide2 import QtCore, QtUiTools, QtWidgets
reload(dna)

shotItemParams = ['E', 'S', 'hip', 'exr', 'range', 'done', 'start', 'end', 'R', 'actions']
nonEditable = [0, 1, 4, 5] # Table cells: read and select only
# shotItemTemplate = {"E": "", "S": "", "hip": "", "exr": "", "range": "", "done": "", "start": "", "end": ""}

class AlignDelegate(QtWidgets.QItemDelegate):
    '''
    Central alignment of UI table of shots
    '''
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter # Center align
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

class CreateShotItems(QtWidgets.QWidget):
    def __init__(self):
        # SETUP UI WINDOW
        super(CreateShotItems, self).__init__()
        ui_file = "{}/batchRender_AddShots.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.ui.btn_add.clicked.connect(self.addShots)
        self.ui.btn_add.clicked.connect(self.close)

    def addShots(self):
        sequenceNumber = self.ui.lin_sequence.text()
        shotNumbers = self.ui.lin_shots.text()
        BR.addShots(sequenceNumber, shotNumbers)


class BatchRender(QtWidgets.QWidget):
    def __init__(self):
        # SETUP UI WINDOW
        super(BatchRender, self).__init__()
        ui_file = "{}/batchRender_Main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # SETUP SHOTS TABLE
        self.ui.tab_shots.verticalHeader().hide()  # Hide row numbers
        self.ui.tab_shots.setItemDelegate(AlignDelegate()) # Set text alignment for cells
        self.ui.tab_shots.setColumnCount(10) # Columns count
        self.ui.tab_shots.setHorizontalHeaderLabels(shotItemParams)
        # Set columns width
        self.ui.tab_shots.setColumnWidth(0, 40)
        self.ui.tab_shots.setColumnWidth(1, 40)
        self.ui.tab_shots.setColumnWidth(2, 40)
        self.ui.tab_shots.setColumnWidth(3, 40)
        self.ui.tab_shots.setColumnWidth(4, 60)
        self.ui.tab_shots.setColumnWidth(5, 60)
        self.ui.tab_shots.setColumnWidth(6, 40)
        self.ui.tab_shots.setColumnWidth(7, 40)
        self.ui.tab_shots.setColumnWidth(8, 30)
        self.ui.tab_shots.setColumnWidth(9, 210)
        self.ui.tab_shots.horizontalHeader().setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

        # Load shots from database
        self.addShots()

        self.ui.btn_addShots.clicked.connect(self.createShotItems)
        self.ui.btn_render.clicked.connect(self.render)
        self.ui.btn_reload.clicked.connect(self.addShots)
        self.ui.btn_delShots.clicked.connect(self.deleteShots)

    def openFolder(self):
        print 'OLA!'
        #print self.ui.tab_shots.cellWidget(0, 9).parent()

    def render(self):
        print '>> Rendering...'

        # get shot items from UI
        shotItems = self.readShotTable()

        for shotItem in shotItems:

            # Skip completely rendered shots (START value set to '' in populateShotItem)
            if not shotItem['start'] == '':
                renderScenePath = dna.buildFilePath(shotItem['hip'],
                                                    dna.fileTypes['renderScene'],
                                                    sequenceNumber=shotItem['E'],
                                                    shotNumber=shotItem['S'])

                hou.hipFile.load(renderScenePath)
                rop = hou.node('/out/{}'.format(dna.mantra))
                rop.render(frame_range=(int(shotItem['start']), int(shotItem['end'])))
            else:
                print '>> Shot E{0}_S{1} already rendered in {2} version!'.format(shotItem['E'],shotItem['S'], shotItem['exr'])

        print '>> Rendering done!'

    def createShotItems(self):
        AS = CreateShotItems()
        AS.show()

    def checkExistingShot(self, sequenceNumber, shotNumber):
        '''
        Check if shot item exists in render database
        :param sequenceNumber:
        :param shotNumbers:
        :return:
        '''

        # print 'E{} S{}'.format(sequenceNumber, shotNumber)

        shotItems = json.load(open(dna.genesFile_render))

        for shotItem in shotItems:
            if shotItem[shotItemParams[0]] == sequenceNumber and shotItem[shotItemParams[1]] == shotNumber:
                return True

    def populateShotItem(self, shotItem):
        '''
        Build shot items from database and populate UI

        :param shotItem: render shot data dictionary
        :return:
        '''

        sequenceNumber, shotNumber = shotItem[shotItemParams[0]], shotItem[shotItemParams[1]]

        # Get shot frame range from database
        shotData = dna.getShotData(sequenceNumber, shotNumber)

        shotItem['range'] = '{0:03d} - {1:03d}'.format(dna.frameStart, shotData['sg_cut_out'])

        # Get latest render hip and latest render folder
        # Assume that in latest hip the render path set to the latest render folder
        # (TBD switch to published version)
        renderScenePath = dna.buildFilePath('001',
                                            dna.fileTypes['renderScene'],
                                            sequenceNumber=sequenceNumber,
                                            shotNumber=shotNumber)

        latestHIP = dna.buildPathLatestVersion(renderScenePath)
        pathMapHIP = dna.analyzeFliePath(latestHIP)

        renderSequencePath = dna.buildFilePath('001',
                                           dna.fileTypes['renderSequence'],
                                           sequenceNumber=sequenceNumber,
                                           shotNumber=shotNumber)

        shotItem['hip'] = pathMapHIP['fileVersion']

        pathMapEXR = dna.analyzeFliePath(renderSequencePath)
        fileLocation = pathMapEXR['fileLocation']
        # Check if folder exists, create if not
        if not os.path.exists(fileLocation):
            os.makedirs(fileLocation)
        latestEXR = dna.extractLatestVersionFolder(fileLocation)

        shotItem['exr'] = latestEXR

        renderFilePath = dna.buildFilePath(latestEXR,
                                           dna.fileTypes['renderSequence'],
                                           sequenceNumber=sequenceNumber,
                                           shotNumber=shotNumber)

        pathMapEXR = dna.analyzeFliePath(renderFilePath)
        latestFolderPath = pathMapEXR['fileLocation']
        listExisted = glob.glob('{0}*.exr'.format(latestFolderPath))

        # Clean list from partially rendered files 'E010_S060_012.1.exr.mantra_checkpoint'
        listCorruptedFiles = glob.glob('{0}*.exr.mantra_checkpoint'.format(latestFolderPath))
        listCorrupted = []
        for file in listCorruptedFiles:
            file = file.replace('\\','/').replace('.mantra_checkpoint', '')
            listCorrupted.append(file.split('/')[-1])

        doneStart, doneEnd = self.extractFrames(listExisted, listCorrupted)

        if doneStart != 0:
            shotItem['done'] = '{0:03d} - {1:03d}'.format(doneStart, doneEnd)

        # Check if sequence is not rendered completely
        # Otherwise set START to a blank value. This will be skipped when render
        if not doneEnd == shotData['sg_cut_out']:
            shotItem['start'] = str(doneEnd + 1)
        else:
            shotItem['start'] = ''

        shotItem['end'] = str(shotData['sg_cut_out'])

        self.addShotRow(shotItem)

        return shotItem

    def addShots(self, sequenceNumber=None, shotNumbers=None):

        # Load existing shots from database
        shotItems = json.load(open(dna.genesFile_render))
        # print shotItems # [{u'hip': u'000', u'S': u'010', u'E': u'010'}, {u'hip': u'001', u'S': u'020', u'E': u'010'}]

        # INIT LAUNCH: LOAD (RELOAD) EXISTING SHOTS
        if sequenceNumber == None:

            # Clear table
            self.ui.tab_shots.setRowCount(0)

            for n, shotItem in enumerate(shotItems):
                self.populateShotItem(shotItem)
                # Paint cells
                # self.ui.tab_shots.item(n, 0).setBackground(QtGui.QColor(75, 75, 75))
                # self.ui.tab_shots.item(n, 1).setBackground(QtGui.QColor(75, 75, 75))

        # LAUNCH FROM CreateShotItems CLASS
        else:
            # Add new shots to database
            shotNumbers = shotNumbers.split(' ')

            for shotNumber in shotNumbers:
                # Check if shot exists in database
                if dna.getShotData(sequenceNumber, shotNumber):
                    # Check if shot item exists in database
                    if not self.checkExistingShot(sequenceNumber, shotNumber):
                        shotItem = {}
                        shotItem[shotItemParams[0]] = sequenceNumber
                        shotItem[shotItemParams[1]] = shotNumber

                        shotItem = self.populateShotItem(shotItem)
                        shotItems.append(shotItem)

                    else:
                        print '>> Shot E{0}-S{1} already exists!'.format(sequenceNumber, shotNumber)

            json.dump(shotItems, open(dna.genesFile_render, 'w'), indent=4)

    def addShotRow(self, shotItem):
        '''
        Add Render Shot ROW to the shots table
        '''

        # print 'shotItem = {}'.format(shotItem)

        table = self.ui.tab_shots
        rows = table.rowCount()  # Get quantity of rows
        table.setRowCount(rows + 1)  # Add one row to existing rows

        for n, param in enumerate(shotItemParams):

            # Create shot CELL
            cell = QtWidgets.QTableWidgetItem()
            btn = QtWidgets.QPushButton()
            btn.setText('Open Folder')
            btn.clicked.connect(self.openFolder)

            # Fill shot CELL with data database
            if shotItemParams[n] in shotItem:
                cell.setText(shotItem[shotItemParams[n]])

            # Add cell to the table row
            table.setItem(rows, n, cell)

            # Disable CELL editing, enable selecting
            if n in nonEditable:
                cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            # Add Open Folder button
            if n == 9:
                table.setCellWidget(rows, n, btn)


        #print 'C', table.rowCount()
        # Add button NOTES to cell
        #for i in range(table.rowCount()):
            #print i
        #btn = QtWidgets.QPushButton()
        #table.setCellWidget(0, 9, btn)

        # Add check box to RENDER to cell
        #chb = QtWidgets.QCheckBox()
        #table.setCellWidget(n, 8, chb)
        # Add comboBox to cell
        # itemTemp = QtWidgets.QComboBox()
        # itemTemp.addItems(['A', 'B'])
        # table.setCellWidget(n, 8, itemTemp)

    def deleteShots(self):
        '''
        REMOVE selected shots from the SHOTs TABLE
        '''

        # Delete shot from UI
        tab = self.ui.tab_shots
        rows = [tab.row(item) for item in tab.selectedItems()]
        [tab.removeRow(row) for row in sorted(rows, reverse=True)]

        # TBD: Delete shot from render.json database

    def readShotTable(self):
        '''
        Read shots data from UI
        :return: list of dictionaries: shotItems
        '''

        shotItems = []  # Shot data for each shot (name shot/scene SRC, name shot/scene NEW)

        # Read shots by ROW
        for i in range(self.ui.tab_shots.rowCount()):

            shotItem = {}
            for n, param in enumerate(shotItemParams):
                shotItem[param] = self.ui.tab_shots.item(i, n).text()
            shotItems.append(shotItem)

        return shotItems


    # MISC
    def extractFrames(self, listExisted, listCorrupted):
        '''
        Get from and last frames from sequence of EXR
        :param listExisted: list of EXR in render shot folder
        :param listCorrupted: list of corrupted EXR
        :return:
        '''

        listFrames = []
        for exr in listExisted:
            exr = exr.replace('\\','/')
            if not exr.split('/')[-1] in listCorrupted:
                # print '{} not in {}'.format(exr.split('/')[-1], listCorrupted)
                frame = exr.split('/')[-1].split('.')[-2]
                listFrames.append(int(frame))

        if listFrames:
            return min(listFrames), max(listFrames)
        else:
            return 0, 0

# Create CS objectfileTypes
BR = BatchRender()

def run():
    # Run the Create Scene Tool
    BR.show()