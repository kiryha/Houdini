'''
Utility for rendering sequence of hip files (aka Deadline Render)
'''

import hou
import json
from EVE.dna import dna
from PySide2 import QtCore, QtUiTools, QtWidgets
reload(dna)

columns = ['E', 'S', 'hip', 'exr', 'range', 'done', 'start', 'end', 'progress']
nonEditable = [4, 5] # Table cells: read and select only
shotItemTemplate = {"E": "", "S": "", "hip": "", "exr": "", "range": "", "done": "", "start": "", "end": ""}

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
        self.ui.tab_shots.setColumnCount(9) # Columns count
        self.ui.tab_shots.setHorizontalHeaderLabels(columns)
        # Set columns width
        self.ui.tab_shots.setColumnWidth(0, 50)
        self.ui.tab_shots.setColumnWidth(1, 50)
        self.ui.tab_shots.setColumnWidth(2, 40)
        self.ui.tab_shots.setColumnWidth(3, 40)
        self.ui.tab_shots.setColumnWidth(4, 60)
        self.ui.tab_shots.setColumnWidth(5, 60)
        self.ui.tab_shots.setColumnWidth(6, 40)
        self.ui.tab_shots.setColumnWidth(7, 40)
        self.ui.tab_shots.setColumnWidth(8, 140)
        self.ui.tab_shots.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)

        # Load shots from database
        self.addShots()

        # REM WORKING
        # Stretch all columns to fit table width
        #self.ui.tab_shots.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Resize column by column index
        # self.ui.tab_shots.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # Set row height
        #self.ui.tab_shots.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)


        # self.ui.btn_addShot.clicked.connect(lambda: self.fillShotsTable(['010', '020', '005', '002', '1-210', '1-180', '181', '210'], self.ui.tab_shots))
        self.ui.btn_addShots.clicked.connect(self.createShotItems)
        self.ui.btn_delShots.clicked.connect(self.deleteShots)

    def render(self):
        print '>> Rendering...'

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
            if shotItem['E'] == sequenceNumber and shotItem['S'] == shotNumber:
                return True

    def populateShotItems(self, shotItems):

        # Build shot items from database and populate UI

        for shotItem in shotItems:
            E = shotItem['E']
            S = shotItem['S']
            hipVersion = ''  # RND scene *.hiplc version
            exrVersion = ''  # EXR version in RND scene RENDER output node
            rangeGenes = ''  # Frame range from shots database
            rangeRendered = ''
            frameStart = ''
            frameEnd = ''

            shotData = [E, S,
                        hipVersion,
                        exrVersion,
                        rangeGenes,
                        rangeRendered,
                        frameStart,
                        frameEnd]

            self.fillShotsTable(shotData)

    def populateShotItem(self, shotItem):

        # Build shot items from database and populate UI

        E = shotItem['E']
        S = shotItem['S']
        hipVersion = ''  # RND scene *.hiplc version
        exrVersion = ''  # EXR version in RND scene RENDER output node
        rangeGenes = ''  # Frame range from shots database
        rangeRendered = ''
        frameStart = ''
        frameEnd = ''

        shotData = [E, S,
                    hipVersion,
                    exrVersion,
                    rangeGenes,
                    rangeRendered,
                    frameStart,
                    frameEnd]

        self.fillShotsTable(shotData)

    def addShots(self, sequenceNumber=None, shotNumbers=None):

        # Load existing shots from database
        shotItems = json.load(open(dna.genesFile_render))
        # print shotItems # [{u'hip': u'000', u'S': u'010', u'E': u'010'}, {u'hip': u'001', u'S': u'020', u'E': u'010'}]

        # INIT LAUNCH
        if sequenceNumber == None:
            self.populateShotItems(shotItems)

        # LAUNCH FROM CreateShotItems CLASS
        else:
            # Add new shots to database
            shotNumbers = shotNumbers.split(' ')

            for shotNumber in shotNumbers:
                # Check if shot item exists in database
                if not self.checkExistingShot(sequenceNumber, shotNumber):

                    # print 'Shot NOT exists'
                    shotItem = shotItemTemplate
                    shotItem['E'] = sequenceNumber
                    shotItem['S'] = shotNumber
                    shotItems.append(shotItem)
                    self.populateShotItem(shotItem)

            json.dump(shotItems, open(dna.genesFile_render, 'w'), indent=4)


    def fillShotsTable(self, shotData):
        '''
        Add Render Shot ROW to the shots table
        '''

        table = self.ui.tab_shots
        rows = table.rowCount()  # Get quantity of rows
        table.setRowCount(rows + 1)  # Add one row to existing rows
        for n, row in enumerate(shotData):

            cell = QtWidgets.QTableWidgetItem()  # Create shot CELL
            cell.setText(shotData[n])  # Fill shot CELL with data from UI
            table.setItem(rows, n, cell)  # Add cell to the table row
            # Disable CELL editing, enable selecting
            if n in nonEditable:
                cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def deleteShots(self):
        '''
        REMOVE selected shots from the SHOTs TABLE
        '''

        tab = self.ui.tab_shots
        rows = [tab.row(item) for item in tab.selectedItems()]
        [tab.removeRow(row) for row in sorted(rows, reverse=True)]

    # DATABASE
    def getShotRange(self):
        return range


# Create CS objectfileTypes
BR = BatchRender()

def run():
    # Run the Create Scene Tool
    BR.show()