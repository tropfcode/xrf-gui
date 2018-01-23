import numpy as np

class Img():
    """
    This class manages an x-ray fluorescence image's state altered by image operations.
    If data is to be normalized, aligned, or any combination thereof a copy of the data is made
    with those changes made to the copy keeping the original data unchanged.
    """
    def __init__(self, data, ref_check = False, norm_check = False, align_check = False,
                title = "N/A", filePath = "N/A", x_shift = 0, y_shift=0):
        """
        Parameters
        ----------
        
        data: 2D numpy array
            Required parameter that is never augmented.
            
        ref_check: Boolean
            If True, then data of object instantiaed from this 
            class is used as reference for alignment.
            
        norm_check: Boolean
            If True, data has been normalized
            
        align_check: Boolean
            If True, data has been aligned
            
        title: String
            Title of data/image.
            
        file_path: String
            Full file path from which data was acquired
            
        x_shift: float
            Pixel amount data has been shifted along x-axis
            
        y_shift: float
            Pixel amount data has been shifted along y-axis
            
        Other Attributes
        ----------------
        
        state: int
            Can take values 0 to 4. 
            0 means no change to data has been made. 
            1 means image aligned only.
            2 means image normalized only. 
            3 means image normalized and then aligned. 
            4 means image aligned and then normalized.
        """
        
        self.data = data
        self.data_2 = np.copy(data)
        self.norm_array = np.empty(shape=(0,0))
        self.ref_check = ref_check
        self.norm_check = norm_check
        self.align_check = align_check
        self.title = title
        self.filePath = filePath
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.state = 0
        self.align_global = False
        self.norm_global = False