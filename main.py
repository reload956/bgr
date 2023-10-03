from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
QFileDialog, QListWidget, QLineEdit, QLabel, QMessageBox, QProgressBar)
from PyQt5.QtGui import QPixmap
from PIL import Image
from rembg import new_session, remove
import sys
import os
from pathlib import Path

def error_window(text):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.exec_()


def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(resource_path('main.ui'), self)
        self.exeButton = self.findChild(QPushButton,'Execute')
        self.exeButton.clicked.connect(self.remBG)

        self.inputButton = self.findChild(QPushButton,'SelectInput')
        self.inputButton.clicked.connect(self.openFileDialog)
        

        self.outputButton = self.findChild(QPushButton,'SelectOutput')
        self.outputButton.clicked.connect(self.openDirectoryDialog)

        self.inputPath = self.findChild(QLineEdit, 'InputPath')
        self.outputPath = self.findChild(QLineEdit,'OutputPath')

        self.fileList = self.findChild(QListWidget,'FileList')

        self.fileList.itemSelectionChanged.connect(self.showImage)

        self.inputImage = self.findChild(QLabel, 'InputImage')
        self.outputImage = self.findChild(QLabel, 'OutputImage')
        
        self.progress = self.findChild(QProgressBar,'progressBar')


        self.show()


    def remBG(self):
        if len(self.inputPath.text()) == 0:
            error_window("не выбраны изображения")
            return
        if len(self.outputPath.text()) == 0:
            error_window("не указана директория для сохранения") 
            return
        listSize = self.fileList.count()
        step = 100/listSize
        for index in range(listSize):
            input = Image.open(f'{self.inputPath.text()}/{self.fileList.item(index).text()}')
            output = remove(input)
            output.save(f'{self.outputPath.text()}/{self.fileList.item(index).text().replace("jpg","png")}')
            self.progress.setValue(int(step * (index+1)))
        
        self.showImage()
            

    def openFileDialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.inputPath.setText(str(filenames[0]).rsplit('/',1)[0])
                self.fileList.clear()
                self.fileList.addItems([str(filename).rsplit('/',1)[1] for filename in filenames])

    
    def openDirectoryDialog(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file:
            self.outputPath.setText(file)

    
    def showImage(self):
         if self.fileList.currentItem() is not None:
            self.inputImage.setPixmap(QPixmap(f'{self.inputPath.text()}/{self.fileList.currentItem().text()}'))
            self.inputImage.setScaledContents(True)

            editImage = Path(f'{self.outputPath.text()}/{self.fileList.currentItem().text().replace("jpg","png")}')
            if editImage.is_file:
                self.outputImage.setPixmap(QPixmap(str(editImage)))
                self.outputImage.setScaledContents(True)

def main():
    app = QApplication([])
    application = MainWindow()
    sys.exit(app.exec())

if __name__=="__main__":
    main()