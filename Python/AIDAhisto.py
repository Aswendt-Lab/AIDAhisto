""""
Created on 17.01.2019

@authors: Niklas Pallast, Michael Diedenhofen
Max Planck Institute for Metabolism Research, Cologne
Department of Neurology, University Hospital Cologne

AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology
"""

from __future__ import print_function

import os
import sys
import argparse
import time

import Sfilter
import barfilters
import numpy as np
import matplotlib.pyplot as plt
import imageio


from scipy import signal
from scipy.ndimage import filters
import warnings
warnings.filterwarnings("ignore")

def save_data(image_out, data):
    # save data (NIfTI)
    #image = nib.Nifti1Image(data, None)
    #header = image.get_header()
    #header.set_xyzt_units(xyz=None, t=None)
    #image.to_filename(image_out)

    imageio.imwrite(image_out,data)
    print("Output:", image_out)
    itemindex = np.where(data == 1)
    fileID = open(os.path.splitext(image_out)[0] +'.txt', 'w')
    fileID.write("AIDAhisto - Number of detected cells: %i\ncell postions (xy):\n\n" % np.size(itemindex,1))
    for i in range(np.size(itemindex,1)):
        fileID.write("%i\t%i\n" % (itemindex[0][i]+1,itemindex[1][i]+1))

    print("Output:", fileID.name)
    fileID.close()

def plot_data(x, y, line='', xlim=None, ylim=None, data_title='Data'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, line)
    if not (xlim is None):
        ax.set_xlim(xlim[0], xlim[1])
    if not (ylim is None):
        ax.set_ylim(ylim[0], ylim[1])
    plt.title(data_title)
    plt.show()

def plot_image(data, image_title='Image'):
    plt.figure()
    imgplot = plt.imshow(data)
    imgplot.set_cmap('gray')
    #imgplot.set_cmap('hot')
    #imgplot.set_cmap('nipy_spectral')
    imgplot.set_interpolation('nearest')
    #imgplot.set_interpolation('bicubic')
    plt.title(image_title)
    plt.show()

def get_local_max(image, min_dist, threshold):

    image[image<threshold] = threshold
    image[:] = image - threshold
    neighborhood = get_neighborhood(min_dist)
    image_max = filters.maximum_filter(image,footprint=neighborhood)

    peaks = (image == image_max)
    peaks[image==0] = False
    print("Number of detected cells:", len(peaks[peaks==True]))

    return peaks

def get_neighborhood(radius):
    # Returns an array with a disc full of ones
    # Copyright David Young 2010
    rsq = radius * radius
    R = np.round(radius)-1
    c = int(R + 1)-1
    t = 2 * R + 1
    y = np.zeros([int(t),int(t)])
    y[:,c] = 1
    y[c,:] = 1

    for rstart in range(1,int(R)):
        rend = np.round(np.sqrt(rsq - rstart * rstart))
        if rend < rstart:
            break
        rstart = int(rstart)
        rend = int(rend)

        y[c + rstart, c + rstart] = 1
        y[c + rstart, c - rstart] = 1
        y[c - rstart, c + rstart] = 1
        y[c - rstart, c - rstart] = 1


        y[c + rstart: c + rend, c + rstart] = 1
        y[c + rstart: c + rend, c - rstart] = 1
        y[c - rend: c - rstart, c + rstart] = 1
        y[c - rend: c - rstart, c - rstart] = 1
        y[c + rstart, c + rstart: c + rend] = 1
        y[c - rstart, c + rstart: c + rend] = 1
        y[c + rstart, c - rend: c - rstart] = 1
        y[c - rstart, c - rend: c - rstart] = 1


    return y

def get_threshold(img):
    # Reference :T.W. Ridler, S. Calvard, Picture thresholding using an iterative selection method,
    #    IEEE Trans. System, Man and Cybernetics, SMC-8 (1978) 630-632.
    #   Author: Thuong HD - ASELAB - Hanoi University of Science and Technology

    grayImage=img.flatten(order='C')
    # % The itial threshol is equal the mean of grayscale image
    initialTheta = np.mean(grayImage)

    initialTheta = np.round(initialTheta)
    i = 0

    threshold =np.zeros([255,1])
    threshold[i] = initialTheta

    # Gray levels are greater than or equal to the threshold
    foregroundLevel = grayImage[grayImage >= initialTheta]
    meanForeground = np.mean(foregroundLevel.flatten(order='C'))

    # Gray levels are less than or equal to the threshold
    backgroundLevel = grayImage[grayImage < initialTheta]
    meanBackground = np.mean(backgroundLevel.flatten(order='C'))

    i = 1
    threshold[i] = np.round((meanForeground + meanBackground) / 2)

    # Loop: Consider condition for threshold
    while np.abs(threshold[i] - threshold[i - 1]) >= 1:
        # Gray levels are greater than or equal to the threshold
        foregroundLevel = grayImage[grayImage >= threshold[i]]
        meanForeground = np.mean(foregroundLevel.flatten(order='C'))

        # Gray levels are less than or equal to the threshold
        backgroundLevel = grayImage[grayImage < threshold[i]]
        meanBackground = np.mean(backgroundLevel.flatten(order='C'))

        i = i + 1
        # Setup new threshold
        threshold[i] = np.round((meanForeground + meanBackground) / 2)


    threshold = threshold[threshold>0]
    return (threshold[-1] - 1) / (255 - 1)

def get_peaks(data, width, min_dist, dark_peaks,barFilterType,fastDetect,thresW):
    t = time.time()

    if not dark_peaks:
        data = 255 - data

    if not fastDetect:

        print("Find Kernel")
        kernel = find_Fastkernel(width)
        print("Fast Convolution")
        image = signal.convolve2d(data, kernel, mode='same')

    else:

        if not barFilterType:
            print("Find LM Kernel")
            kernel = barfilters.getfilters(width, dark_peaks)
        else:
            print("Find S Kernel")
            kernel = Sfilter.getfilters(width, dark_peaks)

        image_vec=np.zeros([np.size(data,0),np.size(data,1),np.size(kernel,2)])

        print("Convolution")
        for i in range(np.size(kernel,2)):
            image_vec[:,:,i] = signal.convolve2d(data, kernel[:,:,i],mode='same')

        image= np.mean(image_vec,2)


    print("Thresholding")
    threshold = thresW * get_threshold(data)
    print("Calculated Threshold "+str(threshold))
    print("Finding maxima")
    peaks = get_local_max(image, min_dist, threshold)
    print('Elapsed time in sec: %.2f ' % (time.time() - t))


    return np.int8(peaks)

def find_Fastkernel(width):
    bounds = (float(width) - 1.0) / 2.0
    sigma = (float(width) - 1.0) / 3.0
    variance = sigma * sigma

    n1 = np.outer(np.ones(width, dtype=np.float64), np.linspace(-bounds, bounds, num=width, endpoint=True, dtype=np.float64))
    n2 = np.outer(np.linspace(-bounds, bounds, num=width, endpoint=True, dtype=np.float64), np.ones(width, dtype=np.float64))
    h = np.square(n1) + np.square(n2)
    hg = np.exp(h / (-2.0 * variance))
    h = (h - (2.0 * variance)) * hg / (variance * variance)
    hgSum = np.sum(hg)
    hSum = sum(h)

    h = (h - (hSum / float(width * width))) / hgSum
    kSum = np.sum(h)
    kOffset = kSum / float(width * width)

    h = h - kOffset
    return h

def get_refPeaks(peaks,refPath,radius):
    img_refPeaks = imageio.imread(refPath)
    coord_refPeaks = np.array(np.where(img_refPeaks >= 1))
    coord_peaks = np.array(np.where(peaks>=1))
    idxValid = nearestneighbour(coord_peaks,coord_refPeaks,radius)

    #coord_refPeaks=np.squeeze(np.array([coord_peaks[0][idxValid],coord_peaks[1][idxValid]]))
    img_validPeaks = np.zeros([np.size(img_refPeaks,0),np.size(img_refPeaks,1)],dtype='int8')
    img_validPeaks[coord_peaks[0][idxValid], coord_peaks[1][idxValid]] = 1

    return img_validPeaks

def minn(x,n):

    n = np.min([n, np.size(x,0)])
    xt = x[0:n]
    xsn = xt
    I = np.argsort(xt)

    for i in range((n+1),np.size(x,0)+1):
        j=n

        while j > 0 and np.size(xsn,0)>0 and x[i-1] < xsn[j-1] :
            j = j - 1

        if j < n:

            xsn = [xsn[1:j], x[i-1], xsn[(j): (n - 1)]]
            I = [I[1:j], i-1, I[(j+1): (n - 1)]]
            
            xsn = np.array([e for e in xsn if e])
            I = np.array([e for e in I if e])

    return I

def nearestneighbour(X,P,r):
    NumberOfNeighbours = 1
    Radius = r


    idx = np.zeros([NumberOfNeighbours, np.size(P, 1)],dtype='int')

    # Loop through the set of points P, finding the neighbours
    Y = np.zeros([np.size(X,0),np.size(X,1)])
    for iPoint in range(np.size(P,1)):
        x = P[:, iPoint]
        for i in range(np.size(Y, 0)):
            Y[i,:] = X[i,:] - x[i]

        dSq = np.sum(np.abs(Y)**2, 0)
        iRad=0
        while np.size(iRad)==1:
            iRad = np.squeeze((dSq < Radius**2).nonzero())
            Radius=Radius+1

        iSorted = iRad[ minn(dSq[iRad],NumberOfNeighbours)]

        if iSorted.size == 0:
            print("No nearest neighbors in given radius")
            return
        idx[:,iPoint]=iSorted

    return idx

def get_roiEval(roiPath,peaks,image_out,txt_file):
    if roiPath is not None and os.path.isfile(roiPath):
        mask = imageio.imread(roiPath)
        if np.size(mask.shape)>2:
            mask = np.squeeze(mask[:,:,0])
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
            roiNo = np.delete(roiNo,0)
            cells = np.zeros(np.size(roiNo))
            cellMap = np.zeros_like(mask,dtype=float)
            for i in range(np.size(roiNo)):
                cells[i] = np.sum(peaks[mask==roiNo[i]])
                cellMap[mask==roiNo[i]] = cells[i]/np.sum(mask==roiNo[i])

            # maxCellNo=np.max(cells)
            # colormap = cm.ScalarMappable(cmap="hot")
            # im = colormap.to_rgba(cellMap)
            imageio.imwrite(os.path.splitext(image_out)[0] + 'Map.tif', cellMap)
            print("Output:", os.path.splitext(image_out)[0] + 'Map.tif')
            # misc.toimage(cellMap, cmin=0.0, cmax=1).save(os.path.splitext(image_out)[0] + 'Map.jpg')
            fileID = open(os.path.splitext(image_out)[0] + 'ROIs.txt', 'w')
            fileID.write("AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology \nNumber of identified Cells in %i given ROIs \n\n" % np.size(roiNo))

            if indices is None:
                for i in range(np.size(cells)):
                    fileID.write("%i\t%i\n" % (roiNo[i], cells[i]))
            else:
                for i in range(np.size(cells)):
                    tempIdx=np.argwhere(indices == roiNo[i])
                    if not tempIdx:
                        continue
                    str_idx = ref_lines[int(tempIdx[0])]

                    acro = str.split(str_idx, '\t')[1][:-1]
                    fileID.write("%i\t%s\t%i\n" % (roiNo[i], acro,cells[i]))

            print("Output:", fileID.name)
            fileID.close()

def main():
    # default values
    width = 10.0
    color_ch = 0


    parser = argparse.ArgumentParser(description='AIDAhisto')
    parser.add_argument('image_in', help='input image path (TIFF,PNG,JPG)')
    parser.add_argument('-o', '--image_out', help='output image path')
    parser.add_argument('-w', '--width', default=10.0, help='kernel width (default %d)' % (width,),type=float)
    parser.add_argument('-c', '--channel', default=0, help='color channel (default red with %i)' % (color_ch,),type=int)
    parser.add_argument('-m', '--min_dist', help='min. distance (default width/2)',type=float)
    parser.add_argument('-d', '--dark_peak_inv', action='store_false', help='dark peak inverter')
    parser.add_argument('-b', '--barFilterType', action='store_false', help='detect not circular square cells')
    parser.add_argument('-f', '--fastDetect', action='store_false', help='fast detection')
    parser.add_argument('-t', '--thres_weighting',default =1.0, help='weighting factor for isodata threshold - default 1.0',type=float)
    parser.add_argument('-a', '--roi_in', help='input roi image path (NIfTI,TIFF)')
    parser.add_argument('-r', '--ref_in', help='path to reference img with cell nuclei', default="")
    parser.add_argument('-n','--neighborRad', help='radius to define neighbors in reference image', default=25, type=int)
    parser.add_argument('-l', '--listRoiNames',
                        help='txt file to translate ROI Number to acronyms', type=str)
    args = parser.parse_args()

    min_dist = float(args.width) / 2.0 if args.min_dist is None else float(args.min_dist)
    color_ch=args.channel
    channel_color = ["Red","Green","Blue"]
    # read image data
    if os.path.isfile(args.image_in):
        data = imageio.imread(args.image_in)
        if np.size(data.shape)>2:
            print('CHANNEL: ' +channel_color[color_ch])
            if color_ch>2:
                color_ch=2

            data = np.squeeze(data[:,:,color_ch])
    else:
        sys.exit(1)
    if args.image_out is not None and os.path.isdir(args.image_out):
        image_out = args.image_out + "/" + \
                    os.path.splitext(os.path.basename(args.image_in))[0] + "_cC" + os.path.splitext(args.image_in)[1]
    else:
        image_out = os.path.splitext(args.image_in)[0] + "_ch" + str(color_ch+1) + "_cC" + os.path.splitext(args.image_in)[1]

    print("Input:", args.image_in, data.dtype, data.shape)

    peaks = get_peaks(data, int(args.width), min_dist, args.dark_peak_inv, args.barFilterType,args.fastDetect,args.thres_weighting)

    # if reference peaks exists
    if os.path.isfile(args.ref_in):
        ref_peaks=get_refPeaks(peaks,args.ref_in,args.neighborRad)
        print('%i valid cells were identified from %i cells' % (len(peaks[ref_peaks==True]),len(peaks[peaks==True])))
        peaks=ref_peaks

    # read translation TXT file
    txt_file = None
    if args.listRoiNames is not None:
        txt_file = args.listRoiNames
        if not os.path.exists(args.listRoiNames):
            sys.exit("Error: '%s' is not an existing translation txt file." % (txt_file))

    # save output image and txtFile
    save_data(image_out, peaks)
    print(sys.argv[1:])
    file = open(os.path.join(os.path.dirname(args.image_in), os.path.basename(args.image_in)+"_process.log"), 'w')
    file.write(str(sys.argv[1:]))
    file.close()
    # evaluate cell number in given regions
    get_roiEval(args.roi_in, peaks, image_out,txt_file)



if __name__ == '__main__':
    main()
