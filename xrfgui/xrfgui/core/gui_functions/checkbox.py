from PyQt4 import QtCore, QtGui
from ..data_functions import functions as func
import numpy as np

def align_check(main):
    """
    Manages align image check box in 'Image Augmentation' box. Aligns or
    unaligns image based on how box is checked.
    For checkBox
    """
    if len(main.imgObjList) is 0:
        main.msg("gui_functions.checkbox.align_check Error: Need to plot image in order to align it")
        main.checkBox.setCheckState(0)
        return
    if main.alignData is None:
        main.msg("gui_functions.checkbox.align_check Error: Need to choose data to align with")
        main.checkBox.setCheckState(0)
        return
    imgObj = main.imgObjList[main.horizontalSlider.value()]
    if main.checkBox.isChecked():
        if main.checkBox_2.isChecked():
            imgObj.state = 3
        else:
            imgObj.state = 1
        alignData = np.copy(main.alignData)
        imgObj.data_2, alignData = func.handle_imgsize(imgObj.data_2, alignData)
        aligned_array, x_shift, y_shift = func.align(alignData, imgObj.data_2)
        imgObj.data_2 = np.copy(np.real(aligned_array))
        imgObj.x_shift = x_shift
        imgObj.y_shift = y_shift
    else:
        func.image_inverse(imgObj, flag='align')
    func.update(main)
    
def norm_check(main):
    """
    Manages normalize image check box in 'Image Augmentation' box. 
    Normalizes or unnormalizes image based on how box is checked.
    For checkBox_2
    """
    if len(main.imgObjList) == 0:
        main.msg("gui_functions.checkbox.norm_check Error: Need to plot image in order to normalize it")
        main.checkBox_2.setCheckState(0)
        return
    if main.normData is None:
        main.msg("gui_functions.checkbox.norm_check Error: Need to choose data to normalize with")
        main.checkBox_2.setCheckState(0)
        return
    imgObj = main.imgObjList[main.horizontalSlider.value()]
    if main.checkBox_2.isChecked():
        if main.checkBox.isChecked():
            imgObj.state = 4
        else:
            imgObj.state = 2
        imgObj.norm_array = np.copy(main.normData)
        imgObj.data_2, imgObj.norm_array = func.handle_imgsize(imgObj.data_2, imgObj.norm_array)
        imgObj.data_2 = np.copy(func.normalize(imgObj.data_2, imgObj.norm_array))
    else:
        func.image_inverse(imgObj, flag='norm')
    func.update(main)
    
    
def boxes(main, imgObj):
    # setCheckState 0 is not checked, 2 is checked
    if imgObj.state == 3 or imgObj.state == 4:
        main.checkBox.setCheckState(2)
        main.checkBox_2.setCheckState(2)
    elif imgObj.state == 0:
        main.checkBox.setCheckState(0)
        main.checkBox_2.setCheckState(0)
    elif imgObj.state == 1:
        main.checkBox.setCheckState(2)
        main.checkBox_2.setCheckState(0)
    else:
        main.checkBox.setCheckState(0)
        main.checkBox_2.setCheckState(2)
        
    if imgObj.align_global == True:
        main.checkBox_5.setCheckState(2)
    else:
        main.checkBox_5.setCheckState(0)
    
    if imgObj.norm_global == True:
        main.checkBox_5.setCheckState(2)
    else:
        main.checkBox_5.setCheckState(0)
        
        
def align_global(main):
    """
    Function for checkbox_5
    """
    if len(main.imgObjList) == 0:
        main.msg("gui_functions.checkbox.align_global Error: Need to plot image")
        main.checkBox_5.setCheckState(0)
        return
    
    imgObj = main.imgObjList[main.horizontalSlider.value()]
    if main.checkBox_5.isChecked():
        imgObj.align_global = True
        main.alignData = np.copy(imgObj.data_2)
        main.checkBox_5.setCheckState(2)
        main.msg(imgObj.title+" set as reference image for alignment")
    else:
        main.checkBox_5.setCheckState(0)
        imgObj.align_global = False
        
def norm_global(main):
    """
    Function for checkbox_6
    """
    if len(main.imgObjList) == 0:
        main.msg("gui_functions.checkbox.norm_global Error: Need to plot image")
        main.checkBox_6.setCheckState(0)
        return
    
    imgObj = main.imgObjList[main.horizontalSlider.value()]
    if main.checkBox_6.isChecked():
        imgObj.norm_global = True
        main.normData = np.copy(imgObj.data_2)
        main.checkBox_6.setCheckState(2)
        main.msg(imgObj.title+" set as reference image for normalization")
    else:
        main.checkBox_6.setCheckState(0)
        imgObj.norm_global = False