import numpy as np
import SimpleITK as sitk
import os
from os import listdir
from os.path import isfile, join
import glob

def createMIP(np_img, slices_num = 15):
    ''' create the mip image from original image, slice_num is the number of 
    slices for maximum intensity projection'''
    img_shape = np_img.shape
    np_mip = np.zeros(img_shape)
    for i in range(img_shape[0]):
        start = max(0, i-slices_num)
        np_mip[i,:,:] = np.amax(np_img[start:i+1],0)
    return np_mip

def main():
    dirs = listdir('input')
    for dir in dirs:
        dir_path = join('input',dir)
        files = glob.glob(join(dir_path, '*.nii.gz'))
        files += glob.glob(join(dir_path,'*.nii'))
        
        if files:
            print (files[0])
            output_dir = join('output',dir)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            sitk_img = sitk.ReadImage(files[0])
            np_img = sitk.GetArrayFromImage(sitk_img)
            np_mip = createMIP(np_img)
            sitk_mip = sitk.GetImageFromArray(np_mip)
            sitk_mip.SetOrigin(sitk_img.GetOrigin())
            sitk_mip.SetSpacing(sitk_img.GetSpacing())
            sitk_mip.SetDirection(sitk_img.GetDirection())
            writer = sitk.ImageFileWriter()
            writer.SetFileName(join(output_dir, 'mip.nii.gz'))
            writer.Execute(sitk_mip)

if __name__ == '__main__':
    main()  




