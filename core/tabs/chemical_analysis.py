from ..data_functions import functions as func
from ..gui_functions import slider
from ..gui_functions import checkbox
import numpy as np

def registration(main):
    # To do: Add warning messages for increasing size of data for alignment etc....
    if len(main.imgObjList) == 0:
        main.msg("tabs.chemical_analysis.registration Error: Need to plot image")
        return
    if main.alignData == None or main.normData == None:
        main.msg("tabs.chemical_analysis.registration Error: Need to provide align and norm data")
        return
    
    shiftList = []
    normData = np.copy(main.normData)
    alignData = np.copy(main.alignData)
    
    for imgObj in main.imgObjList: 
        func.norm_imgObj(main, imgObj)
        func.align_imgObj(main, imgObj)
        shiftList.append((imgObj.title, imgObj.x_shift, imgObj.y_shift))
        imgObj.state = 3
        
    regFile = open(main.wd+'/registration.txt', 'w')
    for index in range(len(main.imgObjList)):
        regFile.write('{} {} {}\n'.format('Title', 'x shift', 'y shift'))
        shift = shiftList[index]
        regFile.write('{} {} {}\n'.format(shift[0], shift[1], shift[2]))
    regFile.close()
    slider.slider_change(main)
    
