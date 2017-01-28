#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Compilebutton

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QWidget, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QCheckBox, QMessageBox
from PyQt5.QtGui import QIcon
import os
import json
import subprocess

def readRecipe(name):
	fillblanks = ["license", "github", "commandrun", "name"]
	jsondecoded = {}
	
	if name != "":
		f = open(os.path.join("recipes",name,'recipe.json'), "r")
		jsondecoded = json.loads(f.read())
		f.close()
	
	jsondecoded["id"] = name
	
	for key in fillblanks:
		if key not in jsondecoded:
			jsondecoded[key] = ""
	return jsondecoded
	

class EditWindow(QWidget):
	recipe = None
	textid = None
	modid = ""
	textid = None
	textname = None
	textgithub = None
	textcommand = None
	textlicense = None
	
	onsave = pyqtSignal()
	
	def __init__(self, modid):
		self.modid = modid

		self.recipe = readRecipe(self.modid)
		super().__init__()
		self.initUI()
		
	def save(self):
		
		if not self.textid.text().isalnum():
			q = QMessageBox()
			q.setText("The id needs to be alphanumeric")
			q.exec()
			return
		
		if self.modid == "":
			os.mkdir(os.path.join("recipes",self.textid.text()))
			
		self.recipe["id"] = ""
		self.recipe["name"] = self.textname.text()
		self.recipe["github"] = self.textgithub.text()
		self.recipe["commandrun"] = self.textcommand.text()
		self.recipe["license"] = self.textlicense.text()
		
		self.recipe = dict((k, v) for k, v in self.recipe.items() if v != '')
		
		f = open(os.path.join("recipes",self.textid.text(),'recipe.json'), "w")
		f.write(json.dumps(self.recipe, sort_keys=False, indent=4, separators=(',', ': ')))
		f.close()
		self.close()
		self.onsave.emit()
		
	def initUI(self):
		self.setGeometry(300, 300, 300, 220)
		grid = QGridLayout()
		mainWidget = QWidget()
		self.setLayout(grid)
		
		l1 = QLabel("ID (alphanumeric folder name you want. Used on the command line)")
		grid.addWidget(l1)
		
		self.textid = QLineEdit(self.recipe["id"])
		grid.addWidget(self.textid)
		
		if self.modid != '':
			self.textid.setEnabled(False)
		
		l5 = QLabel("Name")
		grid.addWidget(l5)
		
		self.textname = QLineEdit(self.recipe["name"])
		grid.addWidget(self.textname)
		
		l2 = QLabel("Github adress")
		grid.addWidget(l2)
		
		self.textgithub = QLineEdit(self.recipe["github"])
		grid.addWidget(self.textgithub)
		
		l3 = QLabel("Command to run to build")
		grid.addWidget(l3)
		
		self.textcommand = QLineEdit(self.recipe["commandrun"])
		grid.addWidget(self.textcommand)
		
		l4 = QLabel("License of the mod")
		grid.addWidget(l4)
		
		self.textlicense = QLineEdit(self.recipe["license"])
		grid.addWidget(self.textlicense)
		
		#QLabel("Name")
		
		okButton = QPushButton("&Save")
		okButton.clicked.connect(self.save)
		grid.addWidget(okButton)
		

class BuildatronGui(QMainWindow):
	modlist = None
	jsonmodlist = []
	editwindow = None
	newAction = None
	editAction = None
	
	def __init__(self):
		super().__init__()
		self.initUI()
	
	def openedit(self):	
		self.editwindow = EditWindow(self.jsonmodlist[self.modlist.currentRow()]["id"])
		self.editwindow.onsave.connect(self.refreshmods)
		self.editwindow.show()
	
	def opennew(self):	
		self.editwindow = EditWindow('')
		self.editwindow.onsave.connect(self.refreshmods)
		self.editwindow.show()
	
	def opencompile(self):
		subprocess.Popen(["cmd", "/c", "start", "builder", self.jsonmodlist[self.modlist.currentRow()]["id"]])
	
	def initUI(self):
		self.setGeometry(300, 300, 300, 220)
		self.setWindowTitle("mcBuildaTron")
		
		grid = QGridLayout()
		mainWidget = QWidget()
		mainWidget.setLayout(grid)
		self.setCentralWidget(mainWidget)
		
		self.modlist = QListWidget()
		
		grid.addWidget(self.modlist)
		
		self.newAction = QAction(QIcon('libraries/tango/document-new.svg'), '&New', self)        
		self.newAction.setShortcut('Ctrl+N')
		self.newAction.setStatusTip('New recipe')
		self.newAction.triggered.connect(self.opennew)
		
		self.editAction = QAction(QIcon('libraries/tango/document-properties.svg'), '&Edit', self)        
		self.editAction.setShortcut('Ctrl+E')
		self.editAction.setStatusTip('Edit recipe')
		self.editAction.triggered.connect(self.openedit)
		
		self.compileAction = QAction(QIcon('libraries/tango/media-record.svg'), '&Compile', self)        
		self.compileAction.setShortcut('Ctrl+E')
		self.compileAction.setStatusTip('Download and compile')
		self.compileAction.triggered.connect(self.opencompile)
		
		self.toolbar = self.addToolBar('Cheese')
		self.toolbar.addAction(self.newAction)
		self.toolbar.addAction(self.editAction)
		self.toolbar.addAction(self.compileAction)
		
		self.refreshmods()
		self.modlist.setCurrentRow(0)
		self.show()
	
	def refreshmods(self):
		self.jsonmodlist = []
		self.modlist.clear()
		directories = [f for f in os.listdir("recipes") if not os.path.isfile(os.path.join("recipes", f))]
		for dirname in directories:
			f = open(os.path.join("recipes",dirname,'recipe.json'), "r")
			recipe = readRecipe(dirname)
			self.jsonmodlist.append(recipe)
			f.close()
			if recipe["name"] != '':
				self.modlist.addItem(recipe["name"] + ' (' + recipe["id"] + ')')
			else:
				self.modlist.addItem(recipe["id"])
		print(directories)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	bgui = BuildatronGui()
	sys.exit(app.exec_())