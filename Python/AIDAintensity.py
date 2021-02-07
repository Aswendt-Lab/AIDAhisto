""""
Created on 28.10.2019
Updated on 28.01.2021

@authors: Niklas Pallast, Michael Diedenhofen, Leon Scharwächter
Max Planck Institute for Metabolism Research, Cologne
Department of Neurology, University Hospital Cologne

AIDAhisto: Atlas-based imaging data analysis tool for mouse brain intensity
"""

from __future__ import print_function

import os
import sys
import argparse

import numpy as np
import imageio



def get_roiEval(roiPath, peaks, image_out, txt_file):
    if roiPath is not None and os.path.isfile(roiPath):
        mask = imageio.imread(roiPath)
        if np.size(mask.shape) > 2:
            mask = np.squeeze(mask[:, :, 0])
        if np.size(mask) != np.size(peaks):
            print("Dimension of input image and mask do not agree")
        else:

            indices = None
            ref_lines = None
            if txt_file is not None:

                ref_lines = open(txt_file).readlines()
                indices = np.zeros_like(ref_lines)
                for idx in range(np.size(ref_lines)):
                    curNum = int(str.split(ref_lines[idx], '\t')[0])

                    indices[idx] = curNum
                indices = np.uint32(indices)

            roiNo = np.unique(mask)
            roiNo = np.delete(roiNo, 0)
            cells = np.zeros(np.size(roiNo))
            cells_norm = np.zeros(np.size(roiNo))
            cellMap = np.zeros_like(mask, dtype=float)
            for i in range(np.size(roiNo)):
#                cells[i] = np.sum(peaks[mask == roiNo[i]])*1e-5
                cells[i] = np.sum(peaks[mask == roiNo[i]])
                cells_norm[i] = round(cells[i]/np.size(peaks[mask == roiNo[i]]),2)
            # misc.toimage(cellMap, cmin=0.0, cmax=1).save(os.path.splitext(image_out)[0] + 'Map.jpg')
            fileID = open(os.path.splitext(image_out)[0] + 'ROIs.txt', 'w')
            fileID.write(
                "AIDAhisto: Atlas-based imaging data analysis tool for mouse brain intensity \nIntensity measured for %i given ROIs\n\n" % np.size(
                    roiNo))
            fileID.write(
                  "Intensity: sum of pixel values\nIntensity (normalised): normalised by total number of pixels in ROI (=region size)\n\n")
            fileID.write(
                "Region Atlas-Nr.\tIntensity\t\tIntensity (normalised)\n\n")

            if indices is None:
                for i in range(np.size(cells)):
                    fileID.write("%i\t\t\t%i\t\t\t%.2f\n" % (roiNo[i], cells[i], cells_norm[i]))
            else:
                for i in range(np.size(cells)):
                    tempIdx = np.argwhere(indices == roiNo[i])
                    if not tempIdx:
                        continue
                    str_idx = ref_lines[int(tempIdx[0])]

                    acro = str.split(str_idx, '\t')[1][:-1]
                    fileID.write("%i\t%s\t%i\t\t\t%.2f\n" % (roiNo[i], acro, cells[i], cells_norm[i]))

            print("Output:", fileID.name)
            fileID.close()


def main():
    # default values
    color_ch = 0

    parser = argparse.ArgumentParser(description='AIDAintensity')
    parser.add_argument('image_in', help='input image path (TIFF,PNG,JPG)')
    parser.add_argument('roi_in', help='input roi image path (NIfTI,TIFF)')
    parser.add_argument('-o', '--image_out', help='output image path')
    parser.add_argument('-c', '--channel', default=color_ch, help='color channel (default red with %i)' % (color_ch,),
                        type=int)
    parser.add_argument('-l', '--listRoiNames',
                        help='txt file to translate ROI Number to acronyms', type=str)
    args = parser.parse_args()


    color_ch = args.channel
    channel_color = ["Red", "Green", "Blue"]
    # read image data
    if os.path.isfile(args.image_in):
        data = imageio.imread(args.image_in)
        if np.size(data.shape) > 2:
            print('CHANNEL: ' + channel_color[color_ch])
            if color_ch > 2:
                color_ch = 2

            data = np.squeeze(data[:, :, color_ch])
    else:
        sys.exit(1)
    if args.image_out is not None and os.path.isdir(args.image_out):
        image_out = args.image_out + "/" + \
                    os.path.splitext(os.path.basename(args.image_in))[0] + "_int" + os.path.splitext(args.image_in)[1]
    else:
        image_out = os.path.splitext(args.image_in)[0] + "_ch" + str(color_ch + 1) + "_int" + \
                    os.path.splitext(args.image_in)[1]

    print("Input:", args.image_in, data.dtype, data.shape)

    peaks = data

    # read translation TXT file
    txt_file = None
    if args.listRoiNames is not None:
        txt_file = args.listRoiNames
        if not os.path.exists(args.listRoiNames):
            sys.exit("Error: '%s' is not an existing translation txt file." % (txt_file))

    # save output image and txtFile
    print(sys.argv[1:])
    file = open(os.path.join(os.path.dirname(args.image_in), os.path.basename(args.image_in) + "_process.log"), 'w')
    file.write(str(sys.argv[1:]))
    file.close()
    # evaluate cell number in given regions
    get_roiEval(args.roi_in, peaks, image_out, txt_file)


if __name__ == '__main__':
    main()
