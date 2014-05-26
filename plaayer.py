#!/usr/bin/env python

import sys
  
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

class MainWindow(QtGui.QMainWindow):
	
	def dodpliki(self):
		pliki = QtGui.QFileDialog.getOpenFileNames(self, "Wybierz pliki",
				QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation))
  
		if not pliki:
			return
  
		index = len(self.zrodla)
		
		for string in pliki:
			self.zrodla.append(Phonon.MediaSource(string))
		
		print str(len(self.zrodla))
		
		wiersze = self.tabela.rowCount()
		ile_zrodla = len(self.zrodla)
		while (ile_zrodla > wiersze):
			self.tabela.insertRow(wiersze)
			fileNameItem = QtGui.QTableWidgetItem((self.zrodla[wiersze]).fileName())
			self.tabela.setItem(wiersze,0,fileNameItem)
			wiersze = wiersze + 1
			
		self.tabela.resizeColumnsToContents()
			
	def zmianastat(self, aktywnosc, oldState):
		if aktywnosc == Phonon.PlayingState:
			self.odtwarzaj.setEnabled(False)
			self.pauzuj.setEnabled(True)
			self.stopuj.setEnabled(True)

		elif aktywnosc == Phonon.StoppedState:
			self.stopuj.setEnabled(False)
			self.odtwarzaj.setEnabled(True)
			self.pauzuj.setEnabled(False)
			self.zegar.display("00:00")
  
		elif aktywnosc == Phonon.PausedState:
			self.pauzuj.setEnabled(False)
			self.stopuj.setEnabled(True)
			self.odtwarzaj.setEnabled(True)
  
	def czas(self, time):
		stoper = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
		self.zegar.display(stoper.toString('mm:ss'))
  
	def klik(self, row, column):
		bylodt = (self.media.state() == Phonon.PlayingState)
  
		self.media.stop()
		self.media.clearQueue()
  
		self.media.setCurrentSource(self.zrodla[row])
  
		if bylodt:
			self.media.play()
		else:
			self.media.stop()
  
	def zmianazrodla(self, source):
		self.zegar.display('00:00')
  
	def metaStateChanged(self, aktywnosc, oldState):
		if aktywnosc != Phonon.StoppedState and aktywnosc != Phonon.PausedState:
			return
  
	def koniec(self):
		index = self.zrodla.index(self.media.currentSource()) + 1
		if len(self.zrodla) > index:
			self.media.enqueue(self.zrodla[index])
			
	def funkcje(self):
		self.odtwarzaj = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "odtwarzaj",self, enabled=False,triggered=self.media.play)
		self.pauzuj = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPause),"pauza", self,  enabled=False,triggered=self.media.pause)
		self.stopuj = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaStop), "stop",self, enabled=False,triggered=self.media.stop)
		self.wybpliku = QtGui.QAction("dodaj plik", self, triggered=self.dodpliki)
		self.wyjscie = QtGui.QAction("Wyjscie", self, triggered=self.close)
  
	def menu(self):
		plik = self.menuBar().addMenu("plik")
		plik.addAction(self.wybpliku)
		plik.addAction(self.wyjscie)
			
	def interfejs(self):
		przyciski = QtGui.QToolBar()
  
		przyciski.addAction(self.odtwarzaj)
		przyciski.addAction(self.pauzuj)
		przyciski.addAction(self.stopuj)
		
		self.suwak = Phonon.SeekSlider(self)
		self.suwak.setMediaObject(self.media)
  
		self.glosnosc = Phonon.VolumeSlider(self)
		self.glosnosc.setAudioOutput(self.wyjsciedzw)
  
		self.zegar = QtGui.QLCDNumber()
  
		naglowek = ("Tytul", "")
  
		self.tabela = QtGui.QTableWidget(0, 1)
		self.tabela.setHorizontalHeaderLabels(naglowek)
		self.tabela.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tabela.cellPressed.connect(self.klik)
  
		suwaklayout = QtGui.QHBoxLayout()
		suwaklayout.addWidget(self.suwak)
		suwaklayout.addWidget(self.zegar)
  
		styl = QtGui.QVBoxLayout()
		styl.addWidget(przyciski)
		styl.addWidget(self.glosnosc)

		styl.addLayout(suwaklayout)
		styl.addWidget(self.tabela)
  
		widget = QtGui.QWidget()
		widget.setLayout(styl)
  
		self.setCentralWidget(widget)
		self.setWindowTitle("EGG Player")
		
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__()
  
		self.wyjsciedzw = Phonon.AudioOutput(Phonon.MusicCategory, self)
		self.media = Phonon.MediaObject(self)
  
		self.media.setTickInterval(1000)
  
		self.media.tick.connect(self.czas)
		self.media.stateChanged.connect(self.zmianastat)
		self.media.currentSourceChanged.connect(self.zmianazrodla)
		self.media.aboutToFinish.connect(self.koniec)
  
		Phonon.createPath(self.media, self.wyjsciedzw)
  
		self.funkcje()
		self.menu()
		self.interfejs()
		self.zegar.display("00:00") 
  
		self.zrodla = []
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	okno = MainWindow()
	okno.show()

	sys.exit(app.exec_())

