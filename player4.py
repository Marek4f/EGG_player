#!/usr/bin/env python

import sip
  
import sys
  
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__()
  
		self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
		self.mediaObject = Phonon.MediaObject(self)
		self.metaInformationResolver = Phonon.MediaObject(self)
  
		self.mediaObject.setTickInterval(1000)
  
		self.mediaObject.tick.connect(self.tick)
		self.mediaObject.stateChanged.connect(self.stateChanged)
		self.metaInformationResolver.stateChanged.connect(self.metaStateChanged)
		self.mediaObject.currentSourceChanged.connect(self.sourceChanged)
		self.mediaObject.aboutToFinish.connect(self.aboutToFinish)
  
		Phonon.createPath(self.mediaObject, self.audioOutput)
  
		self.setupActions()
		self.setupMenus()
		self.setupUi()
		self.timeLcd.display("00:00") 
  
		self.sources = []
		
	def addFiles(self):
		files = QtGui.QFileDialog.getOpenFileNames(self, "Select Music Files",
				QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation))
  
		if not files:
			return
  
		index = len(self.sources)
		
		print str(len(self.sources))
  
		for string in files:
			self.sources.append(Phonon.MediaSource(string))
  
		if self.sources:
			self.metaInformationResolver.setCurrentSource(self.sources[index])
		
		print str(len(self.sources))
			
		self.musicTable.resizeColumnsToContents()
			
	def stateChanged(self, newState, oldState):
		if newState == Phonon.ErrorState:
			if self.mediaObject.errorType() == Phonon.FatalError:
				QtGui.QMessageBox.warning(self, "Fatal Error",
						self.mediaObject.errorString())
			else:
				QtGui.QMessageBox.warning(self, "Error",
						self.mediaObject.errorString())
  
		elif newState == Phonon.PlayingState:
			self.playAction.setEnabled(False)
			self.pauseAction.setEnabled(True)
			self.stopAction.setEnabled(True)

		elif newState == Phonon.StoppedState:
			self.stopAction.setEnabled(False)
			self.playAction.setEnabled(True)
			self.pauseAction.setEnabled(False)
			self.timeLcd.display("00:00")
  
		elif newState == Phonon.PausedState:
			self.pauseAction.setEnabled(False)
			self.stopAction.setEnabled(True)
			self.playAction.setEnabled(True)
  
	def tick(self, time):
		displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
		self.timeLcd.display(displayTime.toString('mm:ss'))
  
	def tableClicked(self, row, column):
		wasPlaying = (self.mediaObject.state() == Phonon.PlayingState)
  
		self.mediaObject.stop()
		self.mediaObject.clearQueue()
  
		self.mediaObject.setCurrentSource(self.sources[row])
  
		if wasPlaying:
			self.mediaObject.play()
		else:
			self.mediaObject.stop()
  
	def sourceChanged(self, source):
		self.musicTable.selectRow(self.sources.index(source))
		self.timeLcd.display('00:00')
  
	def metaStateChanged(self, newState, oldState):
		if newState == Phonon.ErrorState:
			QtGui.QMessageBox.warning(self, "Error opening files",
					self.metaInformationResolver.errorString())
  
			while self.sources and self.sources.pop() != self.metaInformationResolver.currentSource():
				pass
  
			return
  
		if newState != Phonon.StoppedState and newState != Phonon.PausedState:
			return
  
		if self.metaInformationResolver.currentSource().type() == Phonon.MediaSource.Invalid:
			return
  
		#~ metaData = self.metaInformationResolver.metaData()
  
		#~ fileName = self.metaInformationResolver.currentSource().fileName()
		#~ fileName = self.mediaObject.currentSource().fileName()
		fileName = str((self.sources[-1]).fileName())
  
		fileNameItem = QtGui.QTableWidgetItem(fileName)
		
		currentRow = self.musicTable.rowCount()
		self.musicTable.insertRow(currentRow)
		self.musicTable.setItem(currentRow, 0, fileNameItem)
  
		if not self.musicTable.selectedItems():
			self.musicTable.selectRow(0)
			self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())
  
		index = self.sources.index(self.metaInformationResolver.currentSource()) + 1
  
		if len(self.sources) > index:
			self.metaInformationResolver.setCurrentSource(self.sources[index])
		else:
			self.musicTable.resizeColumnsToContents()
			if self.musicTable.columnWidth(0) > 300:
				self.musicTable.setColumnWidth(0, 300)
  
	def aboutToFinish(self):
		index = self.sources.index(self.mediaObject.currentSource()) + 1
		if len(self.sources) > index:
			self.mediaObject.enqueue(self.sources[index])
			
	def setupActions(self):
		self.playAction = QtGui.QAction(
				self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play",
				self, shortcut="Ctrl+P", enabled=False,
				triggered=self.mediaObject.play)
  
		self.pauseAction = QtGui.QAction(
				self.style().standardIcon(QtGui.QStyle.SP_MediaPause),
				"Pause", self, shortcut="Ctrl+A", enabled=False,
				triggered=self.mediaObject.pause)
  
		self.stopAction = QtGui.QAction(
				self.style().standardIcon(QtGui.QStyle.SP_MediaStop), "Stop",
				self, shortcut="Ctrl+S", enabled=False,
				triggered=self.mediaObject.stop)
  
		self.nextAction = QtGui.QAction(
				self.style().standardIcon(QtGui.QStyle.SP_MediaSkipForward),
				"Next", self, shortcut="Ctrl+N")
  
		self.previousAction = QtGui.QAction(
				self.style().standardIcon(QtGui.QStyle.SP_MediaSkipBackward),
				"Previous", self, shortcut="Ctrl+R")
  
		self.addFilesAction = QtGui.QAction("Add &Files", self,
				shortcut="Ctrl+F", triggered=self.addFiles)
  
		self.exitAction = QtGui.QAction("E&xit", self, shortcut="Ctrl+X",
				triggered=self.close)
  
		#~ self.aboutAction = QtGui.QAction("A&bout", self, shortcut="Ctrl+B",
				#~ triggered=self.about)
  
		#~ self.aboutQtAction = QtGui.QAction("About &Qt", self,
				#~ shortcut="Ctrl+Q", triggered=QtGui.qApp.aboutQt)
			
	def setupMenus(self):
		fileMenu = self.menuBar().addMenu("&File")
		fileMenu.addAction(self.addFilesAction)
		fileMenu.addSeparator()
		fileMenu.addAction(self.exitAction)
  
		#~ aboutMenu = self.menuBar().addMenu("&Help")
		#~ aboutMenu.addAction(self.aboutAction)
		#~ aboutMenu.addAction(self.aboutQtAction)
			
	def setupUi(self):
		bar = QtGui.QToolBar()
  
		bar.addAction(self.playAction)
		bar.addAction(self.pauseAction)
		bar.addAction(self.stopAction)
  
		self.seekSlider = Phonon.SeekSlider(self)
		self.seekSlider.setMediaObject(self.mediaObject)
  
		self.volumeSlider = Phonon.VolumeSlider(self)
		self.volumeSlider.setAudioOutput(self.audioOutput)
		self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum,
				QtGui.QSizePolicy.Maximum)
  
		palette = QtGui.QPalette()
		palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.yellow)
  
		self.timeLcd = QtGui.QLCDNumber()
		self.timeLcd.setPalette(palette)
  
		headers = ("filename", "")
  
		self.musicTable = QtGui.QTableWidget(0, 1)
		self.musicTable.setHorizontalHeaderLabels(headers)
		self.musicTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.musicTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.musicTable.cellPressed.connect(self.tableClicked)
  
		seekerLayout = QtGui.QHBoxLayout()
		seekerLayout.addWidget(self.seekSlider)
		seekerLayout.addWidget(self.timeLcd)
  
		playbackLayout = QtGui.QHBoxLayout()
		playbackLayout.addWidget(bar)
		playbackLayout.addStretch()
		playbackLayout.addWidget(self.volumeSlider)
  
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(self.musicTable)
		mainLayout.addLayout(seekerLayout)
		mainLayout.addLayout(playbackLayout)
  
		widget = QtGui.QWidget()
		widget.setLayout(mainLayout)
  
		self.setCentralWidget(widget)
		self.setWindowTitle("EGG Player")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(True)
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec_())

