'''
Utility for rendering sequence of hip files (aka Deadline Render)

For each new render shot row in table:
    - looks into the project.json database and HDD (render dir, render hips) to get parameters (shotItemParams),
    - populate parameters to UI and save them in render.json database

'''

import hou
import json
import glob
from EVE.dna import dna
from PySide2 import QtCore, QtUiTools, QtWidgets
reload(dna)

shotItemParams = ['E', 'S', 'hip', 'exr', 'range', 'done', 'start', 'end', 'R', 'notes']
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
        self.ui.tab_shots.setColumnWidth(8, 20)
        self.ui.tab_shots.setColumnWidth(9, 120)
        self.ui.tab_shots.horizontalHeader().setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

        # Load shots from database
        self.addShots()

        self.ui.btn_addShots.clicked.connect(self.createShotItems)
        self.ui.btn_render.clicked.connect(self.render)
        self.ui.btn_reload.clicked.connect(self.addShots)
        self.ui.btn_delShots.clicked.connect(self.deleteShots)

    def render(self):
        print '>> Rendering...'

        # get shot items from UI
        shotItems = self.readShotTable()

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

        renderSequencePath = dna.buildFilePath('001',
                                           dna.fileTypes['renderSequence'],
                                           sequenceNumber=sequenceNumber,
                                           shotNumber=shotNumber)

        pathMapEXR = dna.analyzeFliePath(renderSequencePath)
        latestEXR = dna.extractLatestVersionFolder(pathMapEXR['fileLocation'])
        latestHIP = dna.buildPathLatestVersion(renderScenePath)
        pathMapHIP = dna.analyzeFliePath(latestHIP)

        shotItem['exr'] = latestEXR
        shotItem['hip'] = pathMapHIP['fileVersion']

        renderFilePath = dna.buildFilePath(latestEXR,
                                           dna.fileTypes['renderSequence'],
                                           sequenceNumber=sequenceNumber,
                                           shotNumber=shotNumber)

        pathMapEXR = dna.analyzeFliePath(renderFilePath)
        latestFolderPath = pathMapEXR['fileLocation']
        listExisted = glob.glob('{0}*.exr'.format(latestFolderPath))
        doneStart, doneEnd = self.extractFrames(listExisted)
        if doneStart != 0:
            shotItem['done'] = '{0:03d} - {1:03d}'.format(doneStart, doneEnd)

        # Check if sequence is not rendered completely
        if not doneEnd == shotData['sg_cut_out']:
            shotItem['start'] = str(doneEnd + 1)
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

            # Fill shot CELL with data database
            if shotItemParams[n] in shotItem:
                cell.setText(shotItem[shotItemParams[n]])

            # Add cell to the table row
            table.setItem(rows, n, cell)

            # Disable CELL editing, enable selecting
            if n in nonEditable:
                cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

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
        return shotItems

    # DATABASE
    def getShotRange(self):
        return range

    # MISC
    def extractFrames(self, listEXR):
        '''
        Get 1 and last frames from sequence of EXR
        :param listEXR:
        :return:
        '''
        listFrames = []
        for exr in listEXR:
            exr = exr.replace('\\','/')
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