from PySide.QtGui import *
from PySide.QtCore import *
from pprint import pprint
from multiprocessing.pool import ThreadPool
import sys, database, os, defines, threading

class MetaFilesMainDialog(QDialog):

  def __init__(self):
    super(MetaFilesMainDialog, self).__init__()
    self.setMinimumSize(500, 500)
    self.setWindowTitle("MetaFiles")

    # Init dialog
    self.createFilesListLayout()
    self.createControls()

    # Init database
    databasePath = os.getcwd() + '/' + defines.database_name
    if not QFile.exists(databasePath):
        database.createDatabase()

    self.populateListView()

    # Layout
    mainLayout = QVBoxLayout()
    mainLayout.addWidget(self.horizontalGroupBox)
    mainLayout.addWidget(self.controlsGroupBox)
    self.setLayout(mainLayout)

  def populateListView(self):
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(database.getListOfFiles)
    files = async_result.get()
    file_names = map(lambda x: x.name, files)


    for index in xrange(self.list.count()):
        self.list.takeItem(index)
    self.list.addItems(file_names)


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
    layout.addWidget(exitButton)
    layout.addWidget(removeFileButton)

    self.controlsGroupBox.setLayout(layout)

  def onAddFileCliked(self):
      print "on add file clicked"
      file_name, extensions = QFileDialog.getOpenFileName(self, 'Open file', QDir.homePath())
      file_info = QFileInfo(file_name)

      dialog_text = "Are you sure you want to add " + file_info.fileName() + "?"

      reply = QMessageBox.question(self, None, dialog_text, QMessageBox.Yes | QMessageBox.No)
      if reply == QMessageBox.Yes:
         database.createFile(file_info.fileName(), file_info.path())
         self.populateListView()

  def onRemovedSelected(self):
      print self.list.selectedItems()

   
def main():  
    app 		= QApplication(sys.argv)
    window = MetaFilesMainDialog()
    window.show()


    return app.exec_()

if __name__ == '__main__':
  main()