'''
Created on 17.01.2019

@author: michaeld
'''

import os

def main():

    os.system('python AIDAhisto.py ../testImages/wholebrain_slice.tif -f -w 9 -d -c 0 -a ../testImages/wholebrain_atlas.tif -l ./acronyms_ARA.txt')
    os.system('python AIDAhisto.py ../testImages/GFAP_lowResolution.tif -w 8 -c 2')
    os.system('python AIDAhisto.py ../testImages/GFAP_lowResolution.tif -w 33 -b -d -c 0 -r ../testImages/GFAP_lowResolution_ch3_cC.tif')

if __name__ == '__main__':
    main()
