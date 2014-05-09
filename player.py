import sys
import os
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import Phonon

app = QtCore.QCoreApplication(sys.argv)
app.setApplicationName("EGG player")
mediaObject = Phonon.MediaObject()
audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
volume = 0
Phonon.createPath(mediaObject, audioOutput)
index = 0
playlist = []
lista=[]
path = "/home/marek/Muzyka"

def playNext():
	global index,player
	if len(playlist) > 0:
		index = (index + 1) % len(playlist)
		player = Phonon.createPlayer(Phonon.MusicCategory, playlist[index])
		player.play()
	

#~ QObject.connect( app, SIGNAL( 'finished()' ), playNext())

for file in os.listdir(path):
	if file.endswith(".mp3"):
		playlist.append(Phonon.MediaSource(path+'/'+str(file)))
		lista.append(file)
		print "Dodano plik: " + str(file)


#~ player = Phonon.createPlayer(Phonon.MusicCategory, playlist[0])

mediaObject.setQueue(playlist)
#~ QObject.connect(mediaObject, SIGNAL(aboutToFinish()), SLOT(enqueueNextSource()));
mediaObject.play()


while True:
	s=input("Odtwarzam plik: " + str((mediaObject.currentSource()).fileName()) + "\n")
	if s==0:
		print "Odtwarzam plik: " + str((mediaObject.currentSource()).fileName()) + "\n"
	if s==1:
		player.pause()
	elif s==2:
		player.play()
	elif s==3:
		player.stop()
	elif s==4:
		index = (index + 1) % len(playlist)
		player = Phonon.createPlayer(Phonon.MusicCategory, playlist[index])
		player.play()
	elif s==44:
		player.playNext()
	elif s==443:
		mediaObject.enqueue(playlist[1])

	elif s==444:
		mediaObject.seek(999999999999999)
		time.sleep(1)
		#~ while (True):
			#~ print "Odtwarzam plik: " + str((mediaObject.currentSource()).fileName()) + "\n"
	elif s==5:
		index = (index - 1) % len(playlist)
		player = Phonon.createPlayer(Phonon.MusicCategory, playlist[index])
		mediaObject.play()
	elif s==6:
		mediaObject.seek(mediaObject.currentTime() + 40000)
	elif s==7:
		player.seek(player.currentTime() - 4000)
	elif s==8:
		volume = volume - 0.1
		if volume < 0.0:
			volume = 0.0
		audioOutput.setVolume(volume)
		print "Zmienio glosnosc na: " + str(volume)
	elif s==9:
		volume = volume + 0.1
		if volume > 1.0:
			volume = 1.0
		audioOutput.setVolume(volume)
		print "Zmienio glosnosc na: " + str(volume)
	elif s==99:
		audioOutput.setMuted(True)
	elif s==98:
		audioOutput.setMuted(False)
	elif s==433:
		pl = playlist
		current = mediaObject.currentSource()
		print current.fileName()
		if (current == pl[0]):
			print "cant do"
		else:
			print pl[1].fileName()
			while (pl[1] != current):
				pl.removeFirst()
			mediaObject.stop()
			mediaObject.clearQueue()
			mediaObject.setQueue(pl)
			mediaObject.play()

app.exec_()
