from PyQt4 import QtCore, QtGui
from ..data_functions import functions as func
from ..gui_functions import slider
import numpy as np

def delete(main):
    """
    Function for pushButton_21
    """
    if len(main.imgObjList) == 0:
        main.msg("gui_functions.delete.delete Error: Need to plot image")
        return
    
    index = main.horizontalSlider.value()
    del main.imgObjList[index]
    slider.slider_update(main)
    func.update(main)
    
def delete_all(main):
    """
    Function for pushButton_22
    """
    if len(main.imgObjList) == 0:
        main.msg("gui_functions.delete.delete_all Error: Need to plot image")
        return
    
    main.imgObjList = []
    slider.slider_update(main)
    func.update(main)
    