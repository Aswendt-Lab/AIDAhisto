""""
Created on 20.07.2020

@author: Leon Scharwächter
AG Neuroimaging and Neuroengineering of Experimental Stroke
Department of Neurology, University Hospital Cologne

AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology

This function prints and returns the percentage of the affected regions within
a brain slice both regarding the region size and the whole brain slice
due to a given mask. You may resize both images to speed up the calculation using
the optional input argument -r followed by the desired image width.

Example (Execution in termial):
python AIDAhisto_maskSize.py "path_to_brain_slice.tif" "path_to_stroke_mask" -r 2000
"""

import argparse
import pandas
from PIL import Image
from collections import Counter

# imgB = image file of brain slice with all regions
# imgM = image file of stroke mask

def main(path1, path2):
    Image.MAX_IMAGE_PIXELS = None
    B = False # to check, if resizing was necessary
    M = False
    imgB = Image.open(path1)  # path1 = path to brain slice image
    widthB, heightB = imgB.size
    imgM = Image.open(path2)  # path2 = path to stroke mask image
    widthM, heightM = imgM.size
    print('Original Image Sizes:')
    print('Brain Width: ' + str(widthB), 'Brain Height: ' + str(heightB))
    print('Mask Width: ' + str(widthM), 'Mask Height: ' + str(heightM))
    
    if imgB.size != imgM.size:
        print("Dimension of input image and mask do not agree")
    else:
        if args.newSize != 0:
            if widthB > args.newSize:
                print('Resize Brain Image...')
                resizeFactor = args.newSize/widthB
                widthB = round(widthB * resizeFactor)
                heightB = round(heightB * resizeFactor)
                imgB = imgB.resize((widthB,heightB),Image.NEAREST)
                B = True
                print('Done');
            if widthM > args.newSize:
                print('Resize Mask Image...')
                resizeFactor = args.newSize/widthM
                widthM = round(widthM * resizeFactor)
                heightM = round(heightM * resizeFactor)
                imgM = imgM.resize((widthM,heightM),Image.NEAREST)
                M = True
                print('Done')
            if B or M == True:
                print('New Image Sizes:')
                if B == True:
                    print('Brain Width: ' + str(widthB), 'Brain Height: ' + str(heightB))
                if M == True:
                    print('Mask Width: ' + str(widthM), 'Mask Height: ' + str(heightM))
    
        print('Calculating the Ratios...')
        # Process image with all brain regions
        dataB = list(imgB.getdata())  # convert image data to a list of floats
        # convert that to a 2-dimensional list (list of lists of floats)
        dataB = [dataB[offset:offset + widthB] for offset in range(0, widthB * heightB, widthB)]
        # convert to a 1-dimensional list of integers
        dataB = [int(item) for sublist in dataB for item in sublist]
        # convert to a dictionary using list comprehension
        # dict_data = dict((x,data.count(x)) for x in set(data))
        # convert to a dictionary using Counter (much faster)
        dict_dataB = dict(Counter(dataB))
        # delete the key 0 ( = black background)
        try:
            del dict_dataB[0]
        except KeyError:
            pass

        # Number of all pixels within the image (without black = background)
        areaBrain = sum(dict_dataB.values())

        # Process Stroke Mask (the same way as above)
        dataM = list(imgM.getdata())
        dataM = [dataM[offset:offset + widthM] for offset in range(0, widthM * heightM, widthM)]
        dataM = [int(item) for sublist in dataM for item in sublist]
        dict_dataM = dict(Counter(dataM))
        try:
            del dict_dataM[0]
        except KeyError:
            pass

        # Now we have:
        # - dict_dataB which contains the sizes of all brain regions (in pixels)
        # - dict_dataM which contains the amount of pixels for each region regarding the mask
        # - areaBrain which is the number of all pixels representing the brain slice

        # Calculate the ratios:
        # - lesion size per brain region (%)
        # - lesion size per brain slice / overall (%)
    
        percentageRegions = [round(100 / dict_dataB[key] * dict_dataM[key], 2) for key in dict_dataM]
        percentageOverall = [round(100 / areaBrain * dict_dataM[key], 2) for key in dict_dataM]

        #Add "Region Nr." to every Key Name
        #for key, value in list(dict_dataM.items()):
        #    dict_dataM["Region Nr. " + str(key)] = dict_dataM.pop(key)

        dict_percRegions = dict(zip(dict_dataM.keys(), percentageRegions))
        dict_percOverall = dict(zip(dict_dataM.keys(), percentageOverall))
    
        # Convert to lists to sort descending regarding the %-values
        list_percRegions = list(dict_percRegions.items())
        list_percRegions_Sorted = sorted(list_percRegions, key=lambda x: x[1], reverse=True)
        list_percOverall = list(dict_percOverall.items())
        list_percOverall_Sorted = sorted(list_percOverall, key=lambda x: x[1], reverse=True)
    
        # Size of mask compared to brain slice (in %)
        maskSize = sum(dict_percOverall.values())
    
        # Pandas needs a list of names for all rows for the tabular
        # presentation, which we will decide to be empty
        numberOfRegions = len(list_percRegions_Sorted)
        rowsNames = numberOfRegions*['']
    
        print('Mask Size per Brain Region:')
        print(pandas.DataFrame(list_percRegions_Sorted,rowsNames,['Region Nr.','%']))
        #print(list_percRegions_Sorted)
        #for key, value in list(dict_percRegions_Sorted.items()):
        #    print(key, value)
        print('Mask Size per Brain Slice:')
        print(pandas.DataFrame(list_percOverall_Sorted,rowsNames,['Region Nr.','%']))
        #print(list_percOverall_Sorted)
        #for key, value in list(dict_percOverall_Sorted.items()):
        #    print(key, value)
        print('Mask Size compared to Brain Slice: '+str(maskSize)+' %')
    
        return dict_percRegions, dict_percOverall

parser = argparse.ArgumentParser(description='This function returns the percentage of the affected regions within a brain slice both regarding the region size and the whole brain slice due to a given mask. Please specify both paths as string arguments. Large input images can be resized using the optional parameter -r behind the indication of the paths. ')
parser.add_argument('path1', type=str, help='Path to brain slice image.tif')
parser.add_argument('path2', type=str, help='Path to brain mask image.tif')
parser.add_argument('-r', '--resize', action='store', dest='newSize', help='scales both input images, where NEWSIZE determines the new width in pixels', type=int, default=0, required=False)
args = parser.parse_args()

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
