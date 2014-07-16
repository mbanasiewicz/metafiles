# -*- coding: utf-8 -*-
from PySide.QtGui import *
from PySide.QtCore import *
from pprint import pprint
from multiprocessing.pool import ThreadPool
from stemming import stemmer
from database import *
import sys, os, defines, threading, file_parser


class MetaFilesMainDialog(QDialog):

  def __init__(self):
    super(MetaFilesMainDialog, self).__init__()
    self.setMinimumSize(500, 500)
    self.setWindowTitle("MetaFiles")

    # Init dialog
    self.createSearchBox()
    self.createFilesListLayout()
    self.createControls()

    # Init database
    self.databaseHandler = DatabaseHandler()
    databasePath = os.getcwd() + '/' + defines.database_name
    if not QFile.exists(databasePath):
        self.databaseHandler.createDatabase()

    self.populateListView()

    # Init file parser
    self.fileParser = file_parser.FileParser()

    # Layout
    mainLayout = QVBoxLayout()
    mainLayout.addWidget(self.searchBox)
    mainLayout.addWidget(self.horizontalGroupBox)
    mainLayout.addWidget(self.controlsGroupBox)
    self.setLayout(mainLayout)

  def createSearchBox(self):
    self.searchBox = QGroupBox("Search field")
    layout = QHBoxLayout()
    self.lineEdit = QLineEdit()
    layout.addWidget(self.lineEdit)
    button = QPushButton("Search")
    button.clicked.connect(self.onSearchClicked)
    layout.addWidget(button)
    self.searchBox.setLayout(layout)

  def populateListView(self):
    files = self.databaseHandler.getListOfFiles()
    # Remove previous items if any
    for index in xrange(self.list.count()):
        self.list.takeItem(index)
    for file in files:
        new_item = QListWidgetItem(file.name, self.list)
        new_item.setData(Qt.UserRole, file)


  def createFilesListLayout(self):
    # List
    self.list = QListWidget()

    self.horizontalGroupBox = QGroupBox("Files list")
    layout = QHBoxLayout()
    layout.addWidget(self.list)
    self.horizontalGroupBox.setLayout(layout)

  def createControls(self):
    self.controlsGroupBox = QGroupBox("Controls")
    layout = QHBoxLayout()
    addFileButton = QPushButton("Add file")
    addFileButton.clicked.connect(self.onAddFileCliked)

    removeFileButton = QPushButton("Remove selected file")
    removeFileButton.clicked.connect(self.onRemovedSelected)

    exitButton = QPushButton("Exit")
    exitButton.clicked.connect(self.close)

    layout.addWidget(addFileButton)
    layout.addWidget(removeFileButton)
    layout.addWidget(exitButton)

    self.controlsGroupBox.setLayout(layout)

  def onAddFileCliked(self):
      print "on add file clicked"
      file_name, extensions = QFileDialog.getOpenFileName(self, 'Open file', QDir.homePath())
      file_info = QFileInfo(file_name)


      if self.fileParser.isFileSupported(file_info):
          dialog_text = "Are you sure you want to add " + file_info.fileName() + "?"
          reply = QMessageBox.question(self, None, dialog_text, QMessageBox.Yes | QMessageBox.No)
          if reply == QMessageBox.Yes:
              self.fileParser.getFileTags(file_info)
              self.databaseHandler.createFile(file_info.fileName(), file_info.path())
              self.populateListView()
      else:
          dialog_text = "Selected file has unsupported extension"
          reply = QMessageBox.information(self, None, dialog_text, QMessageBox.Close)


  def onRemovedSelected(self):
      selected_items = self.list.selectedItems()
      if len(selected_items):
          list_item = selected_items[0]
          file_object = list_item.data(Qt.UserRole)
          self.databaseHandler.deleteFile(file_object)
          self.list.takeItem(self.list.indexFromItem(list_item))

  def onSearchClicked(self):
      print(self.lineEdit.text())


   
def main():  
    app 		= QApplication(sys.argv)
    window = MetaFilesMainDialog()
    window.show()
    return app.exec_()

if __name__ == '__main__':
    main()
