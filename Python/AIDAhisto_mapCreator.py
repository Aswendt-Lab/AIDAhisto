""""
Created on 24.06.2019

@authors: Niklas Pallast, Michael Diedenhofen
Max Planck Institute for Metabolism Research, Cologne
Department of Neurology, University Hospital Cologne

AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology
"""


import os
import sys
import argparse
import nibabel as nii
import numpy as np
from scipy import misc

def mapCreator(txtfile,atlasfile,norm):
    imgdata = nii.load(atlasfile)
    img = imgdata.get_fdata()
    cellMap = np.zeros_like(img, dtype=float)

    f = open(txtfile, "r")
    lines = f.readlines()
    startIndex = lines.index('\n')+1
    cellColumn =2
    for i in range(startIndex,np.size(lines)):
        roiNo = int(lines[i].split('\t')[0])
        try:
            cellNo = int(lines[i].split('\t')[cellColumn].split('\n')[0])
        except:
            print('Problem using function.  Assigning column value to 1.')
            cellColumn = 1
            cellNo = int(lines[i].split('\t')[cellColumn].split('\n')[0])

        if norm:
            cellMap[img == roiNo] = cellNo/np.sum(img==roiNo)
        else:
            cellMap[img == roiNo] = cellNo

    f.close()
    cellMapdata = nii.Nifti1Image(cellMap, imgdata.affine)
    nii.save(cellMapdata,os.path.splitext(txtfile)[0] + 'Map.nii.gz')


def main():
    # default values
    width = 10.0
    color_ch = 0


    parser = argparse.ArgumentParser(description='AIDAhisto')
    parser.add_argument('-t','--txt_file', help='ROI txt file with cell number (.txt)')
    parser.add_argument('-a','--atlas_file', help='related atlas of given txt file')
    parser.add_argument('-n', '--norm', action='store_false', help='set if avoid normalizing by region size')
    args = parser.parse_args()

    if not os.path.isfile(args.txt_file):
        sys.exit("Error: '%s' is not an existing translation txt file." % (args.txt_file))
    if not os.path.isfile(args.atlas_file):
        sys.exit("Error: '%s' is not an existing translation txt file." % (args.atlas_file))

    print("Generate cell map  \33[5m...\33[0m (wait!)", end="\r")
    mapCreator(args.txt_file,args.atlas_file,args.norm)
    print('Generate cell map  \033[0;30;42m COMPLETED \33[0m')

if __name__ == '__main__':
    main()
