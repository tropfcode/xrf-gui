from PyQt4 import QtCore, QtGui
from ..data_functions import functions as func
from . import checkbox

def slider_change(main):
    """
    Controls slider to change displayed image from main.imObjList.
    """
    imgNum = main.horizontalSlider.sliderPosition()
    if len(main.imgObjList) == 0:
        return
    imgObj = main.imgObjList[imgNum]
    main.lineEdit_9.setText(str(imgNum+1)+"/"+str(main.horizontalSlider.maximum()+1))
    func.update(main)
    checkbox.boxes(main, imgObj)
    #textLabels(obj, img)
    
def slider_update(main):
    if len(main.imgObjList) == 0:
        slidersize = 0
    else:
        slidersize = len(main.imgObjList)-1
    main.horizontalSlider.setMaximum(slidersize)
    imgNum = main.horizontalSlider.sliderPosition()
    main.lineEdit_9.setText(str(imgNum+1)+"/"+str(slidersize+1))