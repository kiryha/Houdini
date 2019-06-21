'''
Utility for rendering sequence of hip files (aka Deadline Render)

For each new render shot row in table:
    - looks into the project.json database and HDD (render dir, render hips) to get parameters (shotItemParams),
    - populate parameters to UI and save them in render.json database

'''

# TODO: Check restrictions in moveShotItems()


import hou
import json
import glob
import os
import subprocess

import dna
reload(dna)

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui

shotItemParams = ['E', 'S', 'hip', 'exr', 'range', 'done', 'start', 'end', 'R', 'actions']
nonEditable = [0, 1, 4, 5] # Table cells: read and select only

rootProject = os.environ['ROOT']
genesFileRender = dna.genesFileRender.format(rootProject)
genesFileShots = dna.genesFileShots.format(rootProject)
genesRender = dna.loadGenes(genesFileRender)
genesShots = dna.loadGenes(genesFileShots)

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
        ui_file = "{}/renderFarm_addShots.ui".format(dna.folderUI)
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
        ui_file = "{}/renderFarm_main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(680, 400)  # resize window
        self.setWindowTitle('Render Farm')  # Title Main window

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
        self.ui.tab_shots.setColumnWidth(9, 290)
        self.ui.tab_shots.horizontalHeader().setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

        # Load shots from database
        self.addShots()
        # Fill statistics
        self.fillStatistics(self.readShotTable())


        self.ui.btn_addShots.clicked.connect(self.createShotItems)
        self.ui.btn_render.clicked.connect(lambda: self.render(self.readShotTable()))
        self.ui.btn_reload.clicked.connect(self.addShots)
        self.ui.btn_delShots.clicked.connect(self.deleteShots)
        self.ui.btn_up.clicked.connect(lambda: self.moveShotItems(-1))
        self.ui.btn_down.clicked.connect(lambda: self.moveShotItems(1))
        self.ui.lin_rt.textChanged.connect(lambda: self.fillStatistics(self.readShotTable(), self.ui.lin_rt.text()))

    def openFolder(self):

        splitter = self.sender().parent()
        index = self.ui.tab_shots.indexAt(splitter.pos())
        sequenceNumber = self.ui.tab_shots.item(index.row(), 0).text()
        shotNumber = self.ui.tab_shots.item(index.row(), 1).text()
        exrVersion = self.ui.tab_shots.item(index.row(), 3).text()

        renderFilePath = dna.buildFilePath(exrVersion,
                                           dna.fileTypes['renderSequence'],
                                           sequenceNumber=sequenceNumber,
                                           shotNumber=shotNumber)

        renderFileFloder = dna.analyzeFliePath(renderFilePath)['fileLocation']
        subprocess.Popen('explorer "{}"'.format(renderFileFloder.replace('/', '\\')))

    def openHip(self):

        splitter = self.sender().parent()
        index = self.ui.tab_shots.indexAt(splitter.pos())
        sequenceNumber = self.ui.tab_shots.item(index.row(), 0).text()
        shotNumber = self.ui.tab_shots.item(index.row(), 1).text()
        hipVersion = self.ui.tab_shots.item(index.row(), 2).text()

        renderScenePath = dna.buildFilePath(hipVersion,
                                            dna.fileTypes['renderScene'],
                                            sequenceNumber=sequenceNumber,
                                            shotNumber=shotNumber)

        hou.hipFile.load(renderScenePath)

    def fillStatistics(self, shotItems, frameRenderTime=None):
        # Fill STATISTICS
        if frameRenderTime== None:
                self.ui.lin_rt.setText('15')
        framesTotal = self.calculateFrames(shotItems)
        self.ui.lin_totalFrames.setText('{}'.format(framesTotal))
        renderTimeTotal = round((float(self.ui.lin_rt.text())*framesTotal/1440), 1)
        self.ui.lin_rtTotal.setText(str(renderTimeTotal))

    def calculateFrames(self, shotItems):
        '''Calculate total frames to render'''
        framesTotal = 0

        for shot in shotItems:
            if shot['start'] != '':
                framesTotal += int(shot['end']) - int(shot['start'])
        return framesTotal + 1

    def needRender(self, shotItems):
        ''' Check if any frame need to be rendered (return true) '''

        for shot in shotItems:
            if shot['start'] != '':
                return True

    def render(self, shotItems):
        '''
        Render list of shots
        :param shotItems: list of shot dictionaries to render
        :return:
        '''

        print '>> Rendering list of shots...'

        if self.needRender(shotItems):
            for n, shotItem in enumerate(shotItems):

                renderScenePath = dna.buildFilePath(shotItem['hip'],
                                                    dna.fileTypes['renderScene'],
                                                    sequenceNumber=shotItem['E'],
                                                    shotNumber=shotItem['S'])

                print '>> Rendering shot [ {0} - {1} ]...'.format(shotItem['E'], shotItem['S'])

                try:
                    hou.hipFile.load(renderScenePath, suppress_save_prompt=True)
                    rop = hou.node('/out/{}'.format(dna.mantra))
                    rop.render(frame_range=(int(shotItem['start']), int(shotItem['end'])))
                    print '>> Shot complete'
                except:
                    print '>> Rendering of shot FAILS! Reload render...'
                    self.addShots()  # Reload shots
                    shotItems = self.readShotTable()  # read table
                    self.render([shotItems[n]])

        print '>> Rendering list of shots done!'
        self.addShots()  # Reload shots

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

        shotItems = json.load(open(genesFileRender))

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
        shotData = dna.getShotData(sequenceNumber, shotNumber, genesShots)
        # Get end frame
        frameEnd = shotData['sg_cut_out']

        if frameEnd:
            frameEnd = int(frameEnd)
        else:
            print '>> Error! Set the end frame in shot properties.'
            return

        shotItem['range'] = '{0:03d} - {1:03d}'.format(dna.frameStart, frameEnd)

        # Get latest render hip and latest render folder
        # Assume that in latest hip the render path set to the latest render folder
        # (TBD switch to published version)
        renderScenePath = dna.buildFilePath('001',
                                            dna.fileTypes['renderScene'],
                                            sequenceNumber=sequenceNumber,
                                            shotNumber=shotNumber)

        latestHIP = dna.buildPathLatestVersionFile(renderScenePath)
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
        else:
            shotItem['done'] = ''

        # Check if sequence is not rendered completely
        # Otherwise set START to a blank value. This will be skipped when render
        if not doneEnd == shotData['sg_cut_out']:
            shotItem['start'] = str(doneEnd + 1)
            shotItem['end'] = str(shotData['sg_cut_out'])
        else:
            shotItem['start'] = ''
            shotItem['end'] = ''



        self.addShotRow(shotItem)

        return shotItem

    def addShots(self, sequenceNumber=None, shotNumbers=None):
        '''
        Add shot from database to UI
        :param sequenceNumber:
        :param shotNumbers:
        :return:
        '''

        # Reload genes shot (if shot updated in Project Manager)
        global genesShots
        genesShots = dna.loadGenes(genesFileShots)
        global genesRender
        genesRender = dna.loadGenes(genesFileRender)

        # print 'addShots [sequenceNumber, shotNumbers] = ', sequenceNumber, shotNumbers

        # Load existing shots from database
        # shotItems [{u'hip': u'000', u'S': u'010', u'E': u'010'}, {u'hip': u'001', u'S': u'020', u'E': u'010'}]
        shotItems = genesRender

        # INIT LAUNCH: LOAD (RELOAD) EXISTING SHOTS
        if sequenceNumber == None:

            # Clear table
            self.ui.tab_shots.setRowCount(0)

            # Shot items list with updated data
            shotItemsUP = []

            for n, shotItem in enumerate(shotItems):
                shotItem = self.populateShotItem(shotItem)
                shotItemsUP.append(shotItem)

                # Paint cells
                if shotItem['range'] == shotItem['done']:
                    self.ui.tab_shots.item(n, 8).setBackground(QtGui.QColor(75, 150, 75))
                elif shotItem['done'] == '':
                    self.ui.tab_shots.item(n, 8).setBackground(QtGui.QColor(150, 75, 75))
                else:
                    self.ui.tab_shots.item(n, 8).setBackground(QtGui.QColor(150, 150, 75))

            json.dump(shotItemsUP, open(genesFileRender, 'w'), indent=4)

        # LAUNCH FROM CreateShotItems CLASS
        else:
            # Add new shots to database
            shotNumbers = shotNumbers.split(' ')

            for shotNumber in shotNumbers:
                # Check if shot exists in database
                if dna.getShotData(sequenceNumber, shotNumber, genesShots):
                    # Check if shot item exists in database
                    if not self.checkExistingShot(sequenceNumber, shotNumber):
                        shotItem = {}
                        shotItem[shotItemParams[0]] = sequenceNumber
                        shotItem[shotItemParams[1]] = shotNumber
                        shotItem = self.populateShotItem(shotItem)
                        shotItems.append(shotItem)

                    else:
                        print '>> Shot E{0}-S{1} already exists!'.format(sequenceNumber, shotNumber)

                else:
                    return

            json.dump(shotItems, open(genesFileRender, 'w'), indent=4)

        # Update stat
        self.fillStatistics(shotItems)

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

            btn1 = QtWidgets.QPushButton()
            btn1.setText('Open Folder')
            btn1.clicked.connect(self.openFolder)

            btn2 = QtWidgets.QPushButton()
            btn2.setText('Open Hip')
            btn2.clicked.connect(self.openHip)

            s = QtWidgets.QSplitter()
            s.addWidget(btn1)
            s.addWidget(btn2)

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
                table.setCellWidget(rows, n, s)
                #table.setCellWidget(rows, n, btn2)


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

    def deleteShotDB(self, sequenceNumber, shotNumber):

        shotItems = json.load(open(genesFileRender))

        for i in range(len(shotItems)):
            if shotItems[i]['E'] == sequenceNumber and shotItems[i]['S'] == shotNumber:
                del shotItems[i]
                break

        json.dump(shotItems, open(genesFileRender, 'w'), indent=4)

    def deleteShots(self):
        '''
        REMOVE selected shots from the SHOTs TABLE
        '''

        # Delete shot from UI
        tab = self.ui.tab_shots
        rows = [tab.row(item) for item in tab.selectedItems()]

        for row in sorted(rows, reverse=True):
            sequenceNumber = tab.item(row, 0).text()
            shotNumber = tab.item(row, 1).text()
            self.deleteShotDB(sequenceNumber, shotNumber)
            tab.removeRow(row)

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

    def moveShotItems(self,  operation):
        '''
        Move shot dictionary up or down in the list of shot items (shotItems)
        Restrictions:
            - Only one row at a time could be moved
            - First row could not be moved UP
            - Last row could not be moved DOWN

        :param operation: integer UP(-1) or DOWN(+1)
        :return:
        '''

        table = self.ui.tab_shots

        # Selected row index (only one row should be selected)
        if len(table.selectedItems()) != 1:
            print '>> Select only ONE cell!'
        else:
            rowIndex = table.selectedItems()[0].row()
            columnIndex = table.selectedItems()[0].column()

            # Restrict first UP and last DOWN
            if rowIndex == 0 and operation == -1:
                print '>> Such move not supported!'
            elif rowIndex == table.rowCount()-1 and operation == 1:
                print '>> Such move not supported!'

            else:
                # Clear selection
                table.item(rowIndex, columnIndex).setSelected(False)

                # MOVE SHOT ITEM IN DATABASE
                indexCurrent = rowIndex
                # Load list of shots
                shotItems = json.load(open(genesFileRender))

                # Generate SRC list of indexes for shotItems list
                indexes = []
                for i in range(len(shotItems)):
                    indexes.append(i)

                indexSwap = indexCurrent + operation
                indexes[indexCurrent], indexes[indexSwap] = indexes[indexSwap], indexes[indexCurrent]

                # Build a new list of shots
                shotItemsNEW = []
                for i, shotItem in zip(indexes, shotItems):
                    shotItemsNEW.append(shotItems[i])

                # Save rearranged list of shots
                json.dump(shotItemsNEW, open(genesFileRender, 'w'), indent=4)


                self.addShots()
                # Select same shot item
                table.item(rowIndex + operation, columnIndex).setSelected(True)

    # MISC
    def extractFrames(self, listExisted, listCorrupted):
        '''
        Get first and last frames from sequence of EXR
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

# Create CS object
BR = BatchRender()

def run():
    # Run the Create Scene Tool
    BR.show()