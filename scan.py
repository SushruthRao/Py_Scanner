from pyqt import *
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
import os
import sys
import cv2
import pytesseract
from PyQt5.QtWidgets import QPushButton
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

image_global = ""
global_text = ""
class My_Application(QDialog):
    global image_global
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.checkPath)
        

    def checkPath(self):
        image_path = self.ui.lineEdit.text()
        global image_global 
        image_global = image_path[:]
        
        if os.path.isfile(image_path):
            ImageScan()
            showDialog()      
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(image_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)
            
            

            
            
        
            
def showDialog():
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText("\n" + global_text + "\n")
   msgBox.setText(global_text)
   msgBox.setWindowTitle("Success !")
   msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   msgBox.buttonClicked.connect(msgButtonClick)

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok:
      print('OK clicked')
   
def msgButtonClick(i):
   print("Button clicked is:",i.text())      

def ImageScan():
    pytesseract.pytesseract.tesseract_cmd = "C://Program Files//Tesseract-OCR//tesseract.exe"

    # CHANGE THE NAME OF THIS TO THE IMAGE IN YOUR FOLDER
    img = cv2.imread(image_global)
    #Convert image to grey color 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))


    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 10)

    outlines, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)


    im2 = img.copy()

    file = open("output.txt", "w+")
    file.write("")
    file.close()


    for out in outlines:
        x, y, width, height = cv2.boundingRect(out)
        

        rect = cv2.rectangle(im2, (x, y), (x + width, y + height), (0, 255, 0), 2)
        

        cropped = im2[y:y + height, x:x + width]
        

        file = open("output.txt", "a")
        
        
        text = pytesseract.image_to_string(cropped)
        global global_text
        global_text = text[:]

        file.write(text)
        file.write("\n")
        
        file.close
    
    # CHANGE THE PATH OF THE FILE TO MATCH YOUR TESSERACT INSTALL LOCATION !!!



    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_instance = My_Application()
    class_instance.show()
    sys.exit(app.exec_())



        




