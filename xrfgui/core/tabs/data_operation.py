# Image operation tab

from PyQt4 import QtCore, QtGui
from ..data_functions import functions as func
from ..data_functions import Img
from ..gui_functions import slider
import scipy.misc as mpimg
import numpy as np
import os
    
errorPath = 'core.tabs.data_operation.'    
    
def test():
    print("From data_operation.py "+str(os.getcwd()))
	
def choose_data(main, lineEdit):
    try:
        dataPath = str(QtGui.QFileDialog.getOpenFileName(main.centralwidget, 'Open File'))
        if dataPath == '':
            main.msg(errorPath+"choose_data: No data chosen")
            return
        lineEdit.setText(dataPath)
        main.msg("Chose data " + dataPath)
    except:
        main.msg("Error "+errorPath+"choose_data: Must choose data of proper format (tiff, jpeg, etc.)")
        
        
def plot_chosen_data(main, dataPath):
    """
    Plots and adds to 'main.imgObjList' most recently chosen data from function 'choose_data'.
    """
    error = "Error "+errorPath+"plot_chosen_data: Must choose data of proper format (tiff, jpeg, etc.)"
    try:
        if dataPath == '':
            main.msg('thinks it has nothing')
            main.msg(error)
            return
        data = mpimg.imread(dataPath)
        imgObj = Img.Img(data, title = os.path.basename(dataPath), filePath = dataPath)
        main.imgObjList.append(imgObj)
        main.horizontalSlider.setMaximum(len(main.imgObjList)-1)
        main.horizontalSlider.setValue(main.horizontalSlider.maximum())
        func.plot_img_obj(main, imgObj)
    except:
        main.msg(error)
        
def choose_img_dir(main):
    wd = str(QtGui.QFileDialog.getExistingDirectory(main.centralwidget, 'Open File'))
    main.lineEdit_8.setText(wd)
    if wd == '':
        main.msg("Did not choose directory of images")
    else:
        main.msg("Chose directory of images "+wd)
    
def plot_dir(main):
    """
    Plots all images in directory from chosen via the 'choose_img_dir()' function.
    """
    try:
        wd = str(main.lineEdit_8.text())
        if wd == '':
            main.msg("Error "+errorPath+"plot_dir: Must choose directory first")
            return
        for fi in os.listdir(wd):
            dataPath = os.path.join(wd, fi)
            main.msg("Plotting "+str(fi))
            img = mpimg.imread(str(dataPath))
            imgObj = Img.Img(img, title=str(fi), filePath=str(dataPath))
            main.imgObjList.append(imgObj)
        func.update(main)
        slider.slider_update(main)
    except:
        main.msg("Error "+errorPath+"plot_dir: Make sure all files are images (tiff, jpeg, etc.)")
        
def set_ref(main):
    try:
        dataPath = str(main.lineEdit_12.text())
        data =  mpimg.imread(dataPath)
        main.alignData = np.asarray(data)
        main.msg("Reference data set to "+dataPath)
    except:
        main.msg("Error "+errorPath+"set_ref: File must be proper format (tiff, jpeg, etc.)")
    
def set_norm(main):
    try:
        dataPath = str(main.lineEdit_7.text())
        data =  mpimg.imread(dataPath)
        main.normData = np.asarray(data)
        main.msg("Normalization data set to "+dataPath)
    except:
        main.msg("Error "+errorPath+"set_norm: File must be proper format (tiff, jpeg, etc.)")
        
def temp_plot(main):
    try:
        dataPath = str(main.lineEdit_10.text())
        main.msg("Plotting "+dataPath)
        data = mpimg.imread(dataPath)
        func.temp_plot(data)
    except:
        main.msg("Error "+errorPath+"temp_plot: File must be proper format (tiff, jpeg, etc.)")