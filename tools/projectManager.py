'''
Create and manage assets and shots in project
'''

# TODO: Add sequence property window: edit linked shots
# TODO: split list of asset to categories: char, env, prop, fx
# TODO: When delete sequence ask to delete all sequence shots ??
# (del sequence 020 (which has shot 010), create seq 020, try to create shot 010- error- exists)
# TODO: Hide FX Type combo box when not dealing with FX assets

import hou
import json
import os

from PySide2 import QtCore, QtUiTools, QtWidgets
import dna
reload(dna)

# Get environment data
rootProject = os.environ['ROOT']
genesFileAssets = dna.genesFileAssets.format(rootProject)
genesFileShots = dna.genesFileShots.format(rootProject)
genesFileSequences = dna.genesFileSequences.format(rootProject)
genesAssets = dna.loadGenes(genesFileAssets)
genesSequences = dna.loadGenes(genesFileSequences)
genesShots = dna.loadGenes(genesFileShots)

def linkAsset(ui_shot, catch=None):
    '''
    Add asset names to a list of shot assets in UI (don1t populate to database)
    :param catch:
    :return:
    '''

    sequenceNumber = ui_shot.com_shotSequence.currentText()
    shotNumber = ui_shot.lin_shotName.text()

    if sequenceNumber == '':
        print '>> Select shot to link assets!'
        return

    if not catch:
        # Launch Link Window
        LA = LinkAssets(ui_shot)
        LA.show()
    else:
        # Add assets to the asset list of shot
        listAssets = catch

        # Get existing assets and make new asset list
        shotData = dna.getShotData(sequenceNumber, shotNumber, genesShots)
        if shotData:
            listShotAssetsNEW = list(shotData['assets'])  # list() to break connection to shotGenes
        else:
            listShotAssetsNEW = []

        for asset in listAssets:
            # Check if asset already in list
            if not any(i['code'] == asset for i in listShotAssetsNEW):
                listShotAssetsNEW.append({"code": "{}".format(asset)})
        # Add new list to UI

        ui_shot.lis_assets.clear()
        for asset in listShotAssetsNEW:
            ui_shot.lis_assets.addItem(asset['code'])
            print '>> Assets linked: {} >> E{}_S{}'.format(asset['code'], sequenceNumber, shotNumber)

def unlinkAsset(ui_shot):
    '''
    Remove selected asset from shot properties panel (don`t populate to database)
    :return:
    '''
    selectedAssets = ui_shot.lis_assets.selectedItems()

    for asset in selectedAssets:
        ui_shot.lis_assets.takeItem(ui_shot.lis_assets.row(asset))

def getShotDataUI(ui_shot):
    '''
    Get shot data values from shot UI
    :param ui_shot:
    :return:
    '''

    # Get shot data values from UI
    sequenceNumber = ui_shot.com_shotSequence.currentText()
    shotNumber = ui_shot.lin_shotName.text()
    frameEnd = ui_shot.lin_frameEnd.text()
    description = ui_shot.lin_description.text()
    assets = createListShotAssets(ui_shot)

    shotDataUI = {'sequenceNumber': sequenceNumber,
                 'shotNumber': shotNumber,
                 'frameEnd': frameEnd,
                 'description': description,
                 'assets': assets}

    return shotDataUI

def getAssetDataUI(ui_asset):
    '''
    Get ASSET data values from shot UI
    :param ui_shot:
    :return:
    '''

    # Get ASSET data values from UI
    assetName = ui_asset.lin_assetName.text()
    assetType = ui_asset.com_assetType.currentText()
    hda_name = ui_asset.lin_assetHDA.text()
    description = ui_asset.lin_description.text()

    sassetDataUI = {'assetName': assetName,
                    'assetType': assetType,
                    'hda_name': hda_name,
                    'description': description}

    return sassetDataUI

def updatShotData(shotData, shotDataUI):
    '''
    Update shot data with values from UI
    :return:
    '''
    shotData['code'] = 'SHOT_{}'.format(shotDataUI['shotNumber'])
    shotData['sg_sequence'] = {"name": "{}".format(shotDataUI['sequenceNumber'])}
    shotData['sg_cut_out'] = shotDataUI['frameEnd']
    shotData['description'] = shotDataUI['description']
    shotData['assets'] = shotDataUI['assets']

    return shotData

def updatAssetData(assetData, assetDataUI):
    '''
    Update shot data with values from UI
    :return:
    '''

    assetData['code'] = assetDataUI['assetName']
    assetData['sg_asset_type'] = assetDataUI['assetType']
    assetData['hda_name'] = assetDataUI['hda_name']
    assetData['description'] = assetDataUI['description']

    return assetData

def createListShotAssets(ui_shot):
    '''
    Create list of shot assets dictionaries
    for 'assets' key in shot genes dictionary
    :return:
    '''
    assets = []
    for index in xrange(ui_shot.lis_assets.count()):
        assetName = ui_shot.lis_assets.item(index).text()
        assets.append({"code": "{}".format(assetName)})

    return assets

class LinkAssets(QtWidgets.QWidget):
    '''
    Add assets codes to shot UI
    '''
    def __init__(self, ui_shot):
        # SETUP UI WINDOW
        super(LinkAssets, self).__init__()
        ui_main = "{}/projectManager_linkAssets.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_main, parentWidget=self)
        self.ui_shot = ui_shot

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(320, 120)  # resize window
        self.setWindowTitle('Link Assets')  # Title Main window
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Fill asset list
        listAssets = []
        for asset in genesAssets:
            listAssets.append(asset['code'])
        self.ui.lis_assets.addItems(listAssets)

        # Functionality
        self.ui.btn_add.clicked.connect(self.link)
        self.ui.btn_add.clicked.connect(self.close)

    def link(self):
        listAssets = []
        for asset in self.ui.lis_assets.selectedItems():
            listAssets.append(asset.text())
        linkAsset(self.ui_shot, listAssets)

class CreateShot(QtWidgets.QWidget):
    '''
    Add shot entity to the database
    '''
    def __init__(self, sequenceNumber):
        # SETUP UI WINDOW
        super(CreateShot, self).__init__()
        ui_main = "{}/projectManager_addShot.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_main, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(320, 120)  # resize window
        self.setWindowTitle('Add Shot')  # Title Main window
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        ui_shot = "{}/projectManager_shot.ui".format(dna.folderUI)
        self.ui_shot = QtUiTools.QUiLoader().load(ui_shot, parentWidget=self)
        self.ui.shotLayout.addWidget(self.ui_shot)

        # Add list of existing SEQ to UI
        listSequences = []
        for seq in genesSequences:
            listSequences.append(seq['code'])
        self.ui_shot.com_shotSequence.addItems(listSequences)
        # Get sequence selected in UI and set as current in Create Shot
        if sequenceNumber:
            index = self.ui_shot.com_shotSequence.findText(sequenceNumber, QtCore.Qt.MatchFixedString)
            self.ui_shot.com_shotSequence.setCurrentIndex(index)

        # Functionality
        self.ui.btn_add.clicked.connect(self.addShot)
        self.ui.btn_add.clicked.connect(self.close)
        self.ui_shot.btn_addShotAsset.clicked.connect(lambda: linkAsset(self.ui_shot))
        self.ui_shot.btn_delShotAsset.clicked.connect(lambda: unlinkAsset(self.ui_shot))

    def addShot(self):
        '''
        Create shot entity in datatbase
        :return:
        '''

        # Get shot data from UI
        shotDataUI = getShotDataUI(self.ui_shot)
        sequenceNumber = shotDataUI['sequenceNumber']
        shotNumber = shotDataUI['shotNumber']


        # Skip creation if its exists in DB
        if dna.checkExistsingEntity(genesFileShots, shotNumber, sequenceNumber):
            print '>> Unable to create E{0}-S{1}: Shot exists!'.format(sequenceNumber, shotNumber)
            return

        # Create empty shot data dictionary
        shotData = dna.shotTemplate
        # Update shot data with UI values
        shotData = updatShotData(shotData, shotDataUI)

        # Update SHOT genes
        genesShots.append(shotData)
        json.dump(genesShots, open(genesFileShots, 'w'), indent=4)

        # Update SEQUENCE genes
        for seqData in genesSequences:
            if seqData['code'] == sequenceNumber:
                listShots = seqData['shots']
                listShots.append({"code": "SHOT_{}".format(shotNumber)})
                seqData['shots'] = listShots
        json.dump(genesSequences, open(genesFileSequences, 'w'), indent=4)

        # Send data to PM
        PM.addShot(catch=sequenceNumber)
        print 'Shot E{}-S{} created!'.format(sequenceNumber, shotNumber)

class CreateSequences(QtWidgets.QWidget):
    '''
    Add sequences entities to the database
    '''
    def __init__(self):
        # SETUP UI WINDOW
        super(CreateSequences, self).__init__()
        ui_main = "{}/projectManager_addSequences.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_main, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(320, 60)  # resize window
        self.setWindowTitle('Create Sequences')  # Title Main window
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.ui.btn_add.clicked.connect(self.addSequences)
        self.ui.btn_add.clicked.connect(self.close)

    def addSequences(self):
        '''
        Add sequence entity to the database and update UI
        :return:
        '''

        listSeq = self.ui.lin_seqs.text()
        for sequenceName in listSeq.split(' '):

            if dna.checkExistsingEntity(genesFileSequences, sequenceName):
                print '>> Unable to create sequence {}: Sequence exists!'.format(sequenceName)
                continue

            sequenceData = dict(dna.sequenceTemplate)
            sequenceData['code'] = sequenceName
            genesSequences.append(sequenceData)

        json.dump(genesSequences, open(genesFileSequences, 'w'), indent=4)
        PM.addSequences(catch='')

class CreateAssset(QtWidgets.QWidget):
    '''
    Add asset entity to the database
    '''
    def __init__(self):
        # SETUP UI WINDOW
        super(CreateAssset, self).__init__()
        ui_main = "{}/projectManager_addAsset.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_main, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(320, 120)  # resize window
        self.setWindowTitle('Create Asset')  # Title Main window
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        ui_asset = "{}/projectManager_asset.ui".format(dna.folderUI)
        self.ui_asset = QtUiTools.QUiLoader().load(ui_asset, parentWidget=self)
        self.ui.assetLayout.addWidget(self.ui_asset)
        self.ui_asset.com_assetType.addItems(dna.assetTypes)
        self.ui_asset.com_fxType.addItems(dna.fxTypes)


        self.ui.btn_add.clicked.connect(self.addAsset)
        self.ui.btn_add.clicked.connect(self.close)

    def addAsset(self):
        '''
        Create asset entity in datatbase
        :return:
        '''

        # Get asset data from UI
        assetDataUI = getAssetDataUI(self.ui_asset)
        assetName = assetDataUI['assetName']

        # Skip creation if asset exists in DB
        if dna.checkExistsingEntity(genesFileAssets, assetName):
            print '>> Unable to create asset {}: Asset exists!'.format(assetName)
            return

        assetData = dna.assetTemplate
        assetData = updatAssetData(assetData, assetDataUI)
        genesAssets.append(assetData)

        json.dump(genesAssets, open(genesFileAssets, 'w'), indent=4)

        # Send data to PM
        PM.addAsset(catch='')

class ProjectManager(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectManager, self).__init__()
        ui_main = "{}/projectManager_main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_main, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(960, 500)  # resize window
        self.setWindowTitle('{} Project Manager'.format(os.environ['ROOT'].split('/')[-1]))  # Title Main window
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        # Disable create buttons
        self.butAssetsStat(False)
        self.butShotsStat(False)

        # !!!!!!!!!!!!
        # Hide LIBRARY
        self.ui.box_lib.hide()
        self.ui.box_libProperties.hide()

        # Asset UI
        ui_asset = "{}/projectManager_asset.ui".format(dna.folderUI)
        self.ui_asset = QtUiTools.QUiLoader().load(ui_asset, parentWidget=self)
        self.ui.assetLayout.addWidget(self.ui_asset)
        self.ui_asset.com_assetType.addItems(dna.assetTypes)
        self.ui_asset.com_fxType.addItems(dna.fxTypes)
        self.ui_asset.hide()

        # Shot UI
        ui_shot = "{}/projectManager_shot.ui".format(dna.folderUI)
        self.ui_shot = QtUiTools.QUiLoader().load(ui_shot, parentWidget=self)
        # Lock SEQ and SHOT
        self.ui_shot.com_shotSequence.setEnabled(False)
        self.ui_shot.lin_shotName.setEnabled(False)
        self.ui.shotLayout.addWidget(self.ui_shot)
        self.ui_shot.hide()

        # Fill UI with assets and shots from database
        self.poulateAssets()
        self.poulateSequences()

        # Functionality
        self.ui.lis_seq.itemClicked.connect(self.poulateShots)
        self.ui.lis_seq.itemSelectionChanged.connect(self.changeSelectionSeq)
        self.ui.lis_shots.itemClicked.connect(self.displayShotProperties)
        self.ui.lis_shots.itemSelectionChanged.connect(self.changeSelectionShot)
        self.ui.lis_assets.itemClicked.connect(self.displayAssetProperties)
        self.ui.lis_assets.itemSelectionChanged.connect(self.changeSelectionAsset)

        self.ui.btn_saveShot.clicked.connect(self.saveShotEdits)
        self.ui.btn_saveAsset.clicked.connect(self.saveAssettEdits)
        self.ui.btn_assetHipCreate.clicked.connect(self.createAssetHip)
        self.ui.btn_assetHipOpen.clicked.connect(self.openAssetHip)
        self.ui.btn_shotHipANMCreate.clicked.connect(lambda: self.createShotHip(dna.fileTypes['animationScene']))
        self.ui.btn_shotHipRNDCreate.clicked.connect(lambda: self.createShotHip(dna.fileTypes['renderScene']))
        self.ui.btn_assetAdd.clicked.connect(self.addAsset)
        self.ui.btn_assetDel.clicked.connect(self.delAssets)
        self.ui.btn_seqAdd.clicked.connect(self.addSequences)
        self.ui.btn_seqDel.clicked.connect(self.delSequences)
        self.ui.btn_shotsAdd.clicked.connect(self.addShot)
        self.ui.btn_shotsDel.clicked.connect(self.delShots)

        self.ui_shot.btn_addShotAsset.clicked.connect(lambda: linkAsset(self.ui_shot))
        self.ui_shot.btn_delShotAsset.clicked.connect(lambda: unlinkAsset(self.ui_shot))

    # UI FUNCTIONALITY

    def butAssetsStat(self, value):
        self.ui.btn_assetHipCreate.setEnabled(value)
        self.ui.btn_assetHipOpen.setEnabled(value)

    def butShotsStat(self, value):
        self.ui.btn_shotHipRNDCreate.setEnabled(value)
        self.ui.btn_shotHipANMCreate.setEnabled(value)
        self.ui.btn_shotHipRNDOpen.setEnabled(value)
        self.ui.btn_shotHipANMOpen.setEnabled(value)

    def changeSelectionSeq(self):
        '''Clear list of shots if no sequence selected'''
        if self.ui.lis_seq.selectedItems() == []:
            self.ui.lis_shots.clear()

    def changeSelectionShot(self):
        '''Clear shot properties if no shot selected'''
        if self.ui.lis_shots.selectedItems() == []:
            self.ui_shot.hide()
            self.butShotsStat(False)

    def changeSelectionAsset(self):
        '''Clear asset properties if no asset selected'''
        if self.ui.lis_shots.selectedItems() == []:
            self.ui_asset.hide()
            self.butAssetsStat(False)

    def poulateAssets(self):
        '''Add Asset data to UI'''
        self.ui.lis_assets.clear()
        for asset in genesAssets:
            self.ui.lis_assets.addItem(asset['code'])

    def poulateSequences(self):
        '''Add Sequence data to UI'''
        self.ui.lis_seq.clear()
        for sequence in sorted(genesSequences):
            self.ui.lis_seq.addItem(sequence['code'])

    def poulateShots(self, sequence):
        '''
        Add Shots data to UI
        :param sequence:
            - PySide object, if function called from click
            - String, if function called from another function (poulateShots)
        :return:
        '''

        if type(sequence) is unicode:
            sequenceCode = sequence
        else:
            sequenceCode = sequence.text()

        # Clear list
        self.ui.lis_shots.clear()

        # Get list of shots for current sequence
        for sequence in genesSequences:
            if sequence['code'] == sequenceCode:
                shots = sequence['shots']

        for shot in sorted(shots):
            self.ui.lis_shots.addItem(shot['code'])

    def displayShotProperties(self, shot):
        '''
        Display shot properties (from database) in UI
        :param shot: PySide object or string
        :return:
        '''

        # Show SHOT UI and enable buttons
        self.ui_shot.show()
        self.butShotsStat(True)

        if type(shot) is unicode:
            shotNumber = shot
        else:
            shotCode = shot.text()
            shotNumber = shotCode[-3:]

        sequenceNumber = self.ui.lis_seq.selectedItems()[0].text()
        shotData = dna.getShotData(sequenceNumber, shotNumber, genesShots)

        # Get list of sequences
        listSequences = []
        for seq in genesSequences:
            listSequences.append(seq['code'])

        # Get list of assets
        listAssets = []
        for asset in genesAssets:
            listAssets.append(asset['code'])

        # Fill UI with Shot data
        # Clear UI
        self.ui_shot.com_shotSequence.clear()
        self.ui_shot.lis_assets.clear()
        # Add data
        self.ui_shot.lin_shotName.setText(shotNumber)
        self.ui_shot.com_shotSequence.addItems(listSequences)
        index = self.ui_shot.com_shotSequence.findText(sequenceNumber, QtCore.Qt.MatchFixedString)
        self.ui_shot.com_shotSequence.setCurrentIndex(index)
        self.ui_shot.lin_frameEnd.setText(str(shotData['sg_cut_out']))
        self.ui_shot.lin_description.setText(shotData['description'])
        for asset in shotData['assets']:
            self.ui_shot.lis_assets.addItem(asset['code'])

    def displayAssetProperties(self, asset):
        '''
        Display selected asset properties in UI
        :param asset:
        :return:
        '''


        self.ui_asset.show()
        self.butAssetsStat(True)

        assetName = asset.text()
        dataAsset = dna.getAssetDataByName(genesAssets, assetName)

        # Fill UI with asset data from database
        self.ui_asset.lin_assetName.setText(assetName)
        index = self.ui_asset.com_assetType.findText(dataAsset['sg_asset_type'], QtCore.Qt.MatchFixedString)
        self.ui_asset.com_assetType.setCurrentIndex(index)
        self.ui_asset.lin_assetHDA.setText(dataAsset['hda_name'])
        self.ui_asset.lin_description.setText(dataAsset['description'])

    # TOOL FUNCTIONALITY

    def addAsset(self, catch=None):
        '''Add asset to database'''
        if catch == None:
            CA = CreateAssset()
            CA.show()
        else: # After closing Add Asset window
            # Reload genes
            print 'A'
            global genesAssets
            genesAssets = dna.loadGenes(genesFileAssets)
            # Repopulate Asset
            self.poulateAssets()

    def delAssets(self):
        selectedAssets = self.ui.lis_assets.selectedItems()

        assetNames = []
        for asset in selectedAssets:
            assetNames.append(asset.text())

        dna.deleteEntity(genesFileAssets, assetNames)

        global genesAssets
        genesAssets = dna.loadGenes(genesFileAssets)
        # Repopulate Asset
        self.poulateAssets()

    def addSequences(self, catch=None):
        if catch == None:
            CS = CreateSequences()
            CS.show()
        else: # After closing Add Asset window
            # Reload genes
            global genesSequences
            genesSequences = dna.loadGenes(genesFileSequences)
            # Repopulate Asset
            self.poulateSequences()

    def delSequences(self):
        selectedSequences = self.ui.lis_seq.selectedItems()

        sequenceNames = []
        for seq in selectedSequences:
            sequenceNames.append(seq.text())

        dna.deleteEntity(genesFileSequences, sequenceNames)

        global genesSequences
        genesSequences = dna.loadGenes(genesFileSequences)
        # Repopulate Asset
        self.poulateSequences()

    def addShot(self, catch=None):
        '''Add shot to database'''

        if catch == None:
            # Get first selected SEQ
            selectedSeq = self.ui.lis_seq.selectedItems()
            sequenceNumber = None
            if selectedSeq:
                sequenceNumber = selectedSeq[0].text()

            CS = CreateShot(sequenceNumber)
            CS.show()
        else:
            # After closing Add Shots window
            sequenceNumber = catch
            # Reload genes
            global genesShots
            genesShots = dna.loadGenes(genesFileShots)
            # Repopulate Shots
            self.poulateShots(sequenceNumber)

    def delShots(self):
        selectedShots = self.ui.lis_shots.selectedItems()
        selectedSequences = self.ui.lis_seq.selectedItems()
        sequenceNumber = selectedSequences[0].text()

        shotNames = []
        for shot in selectedShots:
            shotNames.append(shot.text())

        # Delete shot from shots
        dna.deleteEntity(genesFileShots, shotNames, sequenceNumber)
        # Delete shot from assets
        for seqData in genesSequences:
            if seqData['code'] == sequenceNumber:
                listShots = seqData['shots']
                listShotsClean = []
                for shot in listShots:
                    if not shot['code'] in shotNames:
                        listShotsClean.append(shot)
                seqData['shots'] = listShotsClean

        json.dump(genesSequences, open(genesFileSequences, 'w'), indent=4)

        # Reload genes
        global genesShots
        genesShots = dna.loadGenes(genesFileShots)
        global genesAssets
        genesAssets = dna.loadGenes(genesFileAssets)

        # Repopulate Shots
        self.poulateShots(sequenceNumber)

    def linkAsset_rem(self, catch=None):
        '''
        Add asset names to a list of shot assets in UI (don1t populate to database)
        :param catch:
        :return:
        '''

        sequenceNumber = self.ui_shot.com_shotSequence.currentText()
        shotNumber = self.ui_shot.lin_shotName.text()

        if sequenceNumber == '':
            print '>> Select shot to link assets!'
            return

        if not catch:
            # Launch Link Window
            LA = LinkAssets()
            LA.show()
        else:
            # Add assets to the asset list of shot
            listAssets = catch

            # Get existing assets and make new asset list
            shotData = dna.getShotData(sequenceNumber, shotNumber, genesShots)
            listShotAssetsNEW = list(shotData['assets']) # list() to break connection to shotGenes
            for asset in listAssets:
                # Check if asset already in list
                if not any(i['code'] == asset for i in listShotAssetsNEW):
                    listShotAssetsNEW.append({"code": "{}".format(asset)})
            # Add new list to UI

            self.ui_shot.lis_assets.clear()
            for asset in listShotAssetsNEW:
                self.ui_shot.lis_assets.addItem(asset['code'])
                print '>> Assets linked: {} >> E{}_S{}'.format(asset['code'], sequenceNumber, shotNumber)

            # self.displayShotProperties(shotNumber)
            # print '>> Assets linked: {} >> E{}_S{}'.format(listAssets, sequenceNumber, shotNumber)

    def unlinkAsset_rem(self):
        '''
        Remove selected asset from shot properties panel (don`t populate to database)
        :return:
        '''
        selectedAssets = self.ui_shot.lis_assets.selectedItems()

        for asset in selectedAssets:
            self.ui_shot.lis_assets.takeItem(self.ui_shot.lis_assets.row(asset))

    def saveShotEdits(self):
        '''
        Get shot data from UI and populate it to a database
        '''

        # Get shot data values from UI
        shotDataUI = getShotDataUI(self.ui_shot)
        sequenceNumber = shotDataUI['sequenceNumber']
        shotNumber = shotDataUI['shotNumber']

        # Find current shot in DB and update its values
        genesShotsNEW = []
        for shotData in genesShots:
            if shotData['code'] == 'SHOT_{}'.format(shotNumber):
                if shotData['sg_sequence']['name'] == sequenceNumber:
                    # Update data values
                    shotData = updatShotData(shotData, shotDataUI)
                    genesShotsNEW.append(shotData)
                else:
                    genesShotsNEW.append(shotData)
            else:
                genesShotsNEW.append(shotData)

        # Save updated shots in DB
        json.dump(genesShotsNEW, open(genesFileShots, 'w'), indent=4)

        print '>> Shot E{}-S{} updated!'.format(sequenceNumber, shotNumber)

    def saveAssettEdits(self):
        '''
        Get asset data from UI and populate it to database
        :return:
        '''
        # Get ASSET data values from UI
        assetDataUI = getAssetDataUI(self.ui_asset)

        # Find current ASSET in DB and update its values
        genesAssetsNEW = []
        for assetData in genesAssets:
            if assetData['code'] == assetDataUI['assetName']:
                    # Update data values
                    assetData = updatAssetData(assetData, assetDataUI)
                    genesAssetsNEW.append(assetData)
            else:
                genesAssetsNEW.append(assetData)

        # Save updated shots in DB
        json.dump(genesAssetsNEW, open(genesFileAssets, 'w'), indent=4)

        print '>> Asset {} updated!'.format(assetDataUI['assetName'])

    def createAssetHip(self):
        '''
        Create Houdini scenes for asset entities of database.

        TBD when create hip:
            - Character: ask if its GEO, RIG or FUR scene
            - FX: ask if its asset (char, env, prop) or shot (E### S###) FX

        :return:
        '''
        assets = self.ui.lis_assets.selectedItems()

        for asset in assets:
            assetName = asset.text()

            print '>> Creating {} asset scene...'.format(assetName)

            # Get asset data
            assetData = dna.getAssetDataByName(genesAssets, assetName)
            assetType = assetData['sg_asset_type']
            fileType = dna.fileTypes[assetType]

            # Create HIP file with content
            if dna.createHip(fileType, assetName=assetName):

                # CHARACTER
                if fileType == dna.fileTypes['character']:
                    pass

                # ENVIRONMENT
                elif fileType == dna.fileTypes['environment']:
                    # Create ENV asset HDA
                    dna.exportHDA(assetType, assetName, assetName)

                # FX
                elif fileType == dna.fileTypes['FX']:
                    # Create ENV asset HDA
                    dna.exportHDA(assetType, assetName, assetName)

                print '>> Asset scene created!'

    def openAssetHip(self):
        '''
        Open latest version of asset hip file

        :return:
        '''
        assets = self.ui.lis_assets.selectedItems()

        assetName = assets[0].text()
        # Get asset data
        assetData = dna.getAssetDataByName(genesAssets, assetName)
        # Build path to a 001 version of HIP file
        fileType = dna.fileTypes[assetData['sg_asset_type']]
        pathScene = dna.buildFilePath('001', fileType, assetName=assetName)
        # Get latest file version
        pathScene = dna.buildPathLatestVersion(pathScene)
        # Open file
        hou.hipFile.load(pathScene)

    def createShotHip(self, fileType):

        # Get E S from SHOT properties window
        sequenceNumber = self.ui_shot.com_shotSequence.currentText()
        shotNumber = self.ui_shot.lin_shotName.text()
        print '>> Creating {0} E{1}_S{2} shot scene...'.format(fileType, sequenceNumber, shotNumber)

        # If shot exists in database run scene creation
        if not dna.checkGenes(sequenceNumber, shotNumber, genesShots):
            return

        if dna.createHip(fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber):
            dna.buildShotContent(fileType, sequenceNumber, shotNumber, genesShots, genesAssets)
            print '>> Shot scene created!'


# Create Tool instance
PM = ProjectManager()

def run():
    # Run the Tool
    PM.show()