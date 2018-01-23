from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import sys
from pyxrf.api import (make_hdf)
import os
from matplotlib import interactive
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .core import data_functions as data_func
from .core import gui_functions as gui_func
from .core import xrfGui_v4, tabs, roi
#%matplotlib qt

class ExampleApp(QtGui.QMainWindow, xrfGui_v4.Ui_MainWindow):
    """
    This class connects buttons from the inherited Ui_MainWindow GUI to functions
    which will visualize, register, and analyze x-ray fluorescence data.
    It is intended that the functionality of buttons and the GUI itself be
    seperate for maximum flexibility and code adaptation.
    """
    
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
    
        # Primary Variables
        self.wd = os.getcwd()
        self.h5_file = ""
        self.json = ""
        self.imgObjList = []
        self.horizontalSlider.setMaximum(0)
        self.horizontalSlider.setMinimum(0)
        self.alignData = None
        self.normData = None
        self.data_list = []
        self.xanes_list = []
        self.error_num = 0
        
        # Set tri-state false for all checkboxes
        self.checkBox.setTristate(on=False)
        self.checkBox_2.setTristate(False)
        #self.checkBox_3.setTristate(False)
        #self.checkBox_4.setTristate(False)
        self.checkBox_5.setTristate(False)
        self.checkBox_6.setTristate(False)
        
        # Setup Dock Widgets as Tabs (can't be done in qt designer)
        #self.tabifyDockWidget(self.dockWidget_4, self.dockWidget)        
        
        # Create blank Images and display as placeholders
        self.plot_canvas = data_func.MplCanvas.MplCanvas(width=9,height=7)
        blank = np.zeros((100, 100))
        tmp = np.zeros((100, 100))
        self.blank_img = data_func.Img.Img(blank)
        
        self.image = self.plot_canvas.axes.imshow(tmp, cmap='jet')
        self.navi_toolbar = NavigationToolbar(self.plot_canvas, self)

        # Create Roi tool and place in gui
        self.roiLayout = QtGui.QHBoxLayout()
        self.roiList = roi.RoiPopUp.RoiList(self.plot_canvas.axes)
        self.roiLayout.addWidget(self.roiList)
        
        self.canvaslayout = QtGui.QVBoxLayout()
        self.canvaslayout.insertWidget(0, self.navi_toolbar)
        self.canvaslayout.insertWidget(1, self.plot_canvas)
        self.roiLayout.insertLayout(1, self.canvaslayout)
        #self.roiLayout.insertWidget(1, self.plot_canvas)
        
        #self.verticalLayout_4.insertWidget(0, self.navi_toolbar)
        self.verticalLayout_4.insertLayout(0, self.roiLayout)

        divider = make_axes_locatable(self.plot_canvas.axes)
        cax = divider.append_axes('right', size='5%', pad=0.05) # Set colorbar to right of image
        self.cb = self.plot_canvas.fig.colorbar(self.image, cax = cax)
        
        # Begin with no images displayed
        self.lineEdit_9.setText(str(0)+"/"+str(0))
        
        """
        # Data acquisition tab
        self.pushButton.clicked.connect(lambda: func.choose_wd(self))
        self.pushButton_2.clicked.connect(lambda: func.create_h5(self))    
        self.pushButton_3.clicked.connect(lambda: func.create_h5_from_file(self))
        self.pushButton_4.clicked.connect(lambda: func.choose_json(scfffffffffffffffffk,ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhelf))
        self.pushButton_5.clicked.connect(lambda: func.fit_h5(self))
        """
        
        # Data operation tab
        self.pushButton_6.clicked.connect(lambda: tabs.data_operation.choose_data(self, self.lineEdit_6))
        self.pushButton_9.clicked.connect(lambda: tabs.data_operation.plot_chosen_data(self,str(self.lineEdit_6.text())))
        self.pushButton_7.clicked.connect(lambda: tabs.data_operation.choose_img_dir(self))
        self.pushButton_11.clicked.connect(lambda: tabs.data_operation.plot_dir(self))
        self.pushButton_13.clicked.connect(lambda: tabs.data_operation.choose_data(self, self.lineEdit_12))
        self.pushButton_14.clicked.connect(lambda: tabs.data_operation.set_ref(self))
        self.pushButton_8.clicked.connect(lambda: tabs.data_operation.choose_data(self, self.lineEdit_7))
        self.pushButton_23.clicked.connect(lambda: tabs.data_operation.set_norm(self))
        self.pushButton_24.clicked.connect(lambda: tabs.data_operation.choose_data(self, self.lineEdit_10))
        self.pushButton_26.clicked.connect(lambda: tabs.data_operation.temp_plot(self))
        
        # Chemical analysis tab
        self.pushButton_19.clicked.connect(lambda: tabs.chemical_analysis.registration(self))
        #self.pushButton_20.clicked.connect(lambda: func.generate_roi_data(self))
        #self.pushButton_15.clicked.connect(lambda: func.get_data(self))
        #self.pushButton_25.clicked.connect(lambda: func.plot_all_data(self))
        
        # Gui checkboxes and buttons
        self.horizontalSlider.valueChanged.connect(lambda: gui_func.slider.slider_change(self))
        self.checkBox_5.clicked.connect(lambda: gui_func.checkbox.align_global(self))
        self.checkBox_6.clicked.connect(lambda: gui_func.checkbox.norm_global(self))
        self.pushButton_21.clicked.connect(lambda: gui_func.delete.delete(self))
        self.pushButton_22.clicked.connect(lambda: gui_func.delete.delete_all(self))
        #self.pushButton_17.clicked.connect(lambda: func.remove_data(self))
        
        
        # Checkboxes for Image Application/Augmentation
        self.checkBox.clicked.connect(lambda: gui_func.checkbox.align_check(self))
        self.checkBox_2.clicked.connect(lambda: gui_func.checkbox.norm_check(self))
        
        # Roi 
        #self.pushButton_10.clicked.connect(lambda: func.compute_roiList_intensity(self))
        
        
    def msg(self, msgStr):
        """
        Displays message in 'message and error box'.

        Parameters
        ----------
        msgStr: String
            Message to be displayed.
        """
        self.textEdit.append("->"+msgStr)
        
def main():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.setGeometry(50, 50, 1250, 1000)
    form.show()
    app.exec_()
    
if __name__ == '__main__':
    main()