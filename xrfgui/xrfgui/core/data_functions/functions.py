from . import align_class as ac
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as mpimg

def test():
    print("from data_functions/functions.py")
    
def normalize(array1, array2):
    """
    Pixel by pixel division
    """
    mask = np.ma.zeros(array2.shape, dtype=bool)
    if 0 in array2:
        maskpoints = np.where(array2 == 0)
        for point in zip(maskpoints[0], maskpoints[1]):
            mask[point[0], point[1]] = 1
    tmparr = np.ma.array(array2, mask=mask)
    array1, tmparr = handle_imgsize(array1, tmparr)
    return array1/tmparr

def unnormalize(array1, array2):
    return array1*array2

def align(ref_array, align_array):
    """
    Aligns array1 by array2 using convolution.
    Returns aligned image and x,y shift.
    Parameters
    ----------
    ref_array: 2D numpy array
        Reference image for alignment
    
    align_array: 2D numpy array
        Image to align.
    """
    if np.array_equal(ref_array, align_array):
        return align_array, 0.0, 0.0
    if ref_array.shape != align_array.shape:
        ref_array, align_array = handle_imgsize(ref_array, align_array)
    aligned_array, x_shift, y_shift = ac.subpixel_align(ref_array, align_array, 0, 0, 1)
    return aligned_array, x_shift, y_shift

def unalign(aligned_array, x_shift, y_shift ):
    """
    Shifts array in opposite direction of x_shift, y_shift.
    Parameters
    ----------
    aligned_array: 2D numpy array
    
    x_shift: float
        Amount to shift aligned_array by along the x axis
        
    y_shift: float
        Amount to shift aligned_array by along the y axis
    """
    unaligned_array = ac.pixel_shift_2d(aligned_array, (-1)*x_shift, (-1)*y_shift)
    return np.real(unaligned_array) 

def plot_img_obj(main, imgObj):
    """
    Plot Img object
    
    Parameters
    ----------
    imgObj: Img object
    """
    if imgObj.state > 0:
        data = imgObj.data_2
    else:
        data = imgObj.data
    update(main, data=data)
    
def temp_plot(data):
    fig, ax = plt.subplots(1,1)
    ax.imshow(data)
    plt.show()
    
def update(main, data=None):
    imgNum = main.horizontalSlider.sliderPosition()
    if len(main.imgObjList) == 0:
        data = np.zeros((50, 50))
    else:# data is None:
        imgObj = main.imgObjList[imgNum]
        data = imgObj.data_2
    main.image.set_data(data)
    main.image.set_extent((0, data.shape[1], data.shape[0], 0))
    main.image.set_clim(vmin=np.amin(data), vmax=np.amax(data))
    main.cb.set_clim(vmin=np.amin(data), vmax=np.amax(data))
    main.cb.draw_all()
    main.plot_canvas.fig.canvas.draw()
    
def image_inverse(imgObj, flag=None):
    if imgObj.state == 1 or imgObj.state == 2:
        imgObj.data_2 = np.copy(imgObj.data)
        imgObj.state = 0
    elif imgObj.state == 3:
        if flag == 'align':
            imgObj.data_2 = np.copy(normalize(imgObj.data, imgObj.norm_array))
            #unalign(imgObj.data_2, imgObj.x_shift, imgObj.y_shift)
            imgObj.state = 2
        else:
            tmparr = ac.pixel_shift_2d(imgObj.data, imgObj.x_shift, imgObj.y_shift)
            imgObj.data_2 = np.copy(np.real(tmparr))
            imgObj.state = 1
    else:
        if flag == 'align':
            # This normalization is different that before unalignment
            imgObj.data_2 = np.copy(normalize(imgObj.data, imgObj.norm_array))
            imgObj.state = 2
        else:
            tmparr = ac.pixel_shift_2d(imgObj.data, imgObj.x_shift, imgObj.y_shift)
            imgObj.data_2 = np.copy(np.real(tmparr))
            imgObj.state = 1
            
def handle_imgsize(array1, array2):
    area1 = array1.shape[0]*array1.shape[1]
    area2 = array2.shape[0]*array2.shape[1]
    if area1 > area2:
        return array1, mpimg.imresize(array2, array1.shape)
    elif area2 > area1:
        return mpimg.imresize(array1, array2.shape), array2
    else:
        return array1, array2
    
def group_handle_imgsize(dataList):
    area = 0
    count = 0
    resizeIndex = 0
    for data in dataList:
        tmparea = data.shape[0]*data.shape[1]
        if tmparea > area:
            area = tmparea
            index = count
        count += 1
    for index in xrange(len(dataList)):
        array1 = dataList[index]
        array2 = dataList[resizeIndex]
        dataList[index], dataList[resizeIndex] = handle_imgsize(array1, array2)
        
def norm_imgObj(main, imgObj):
    imgObj.norm_array = np.copy(main.normData)
    imgObj.data_2, imgObj.norm_array = handle_imgsize(imgObj.data_2, imgObj.norm_array)
    imgObj.data_2 = np.copy(normalize(imgObj.data_2, imgObj.norm_array))
    
def align_imgObj(main, imgObj):
    alignData = np.copy(main.alignData)
    imgObj.data_2, alignData = handle_imgsize(imgObj.data_2, alignData)
    aligned_array, x_shift, y_shift = align(alignData, imgObj.data_2)
    imgObj.data_2 = np.copy(np.real(aligned_array))
    imgObj.x_shift = x_shift
    imgObj.y_shift = y_shift