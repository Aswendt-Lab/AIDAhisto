clc
clear


%% User Input 

%   inputPath  - path to input grayscale image or color image (see parameter 'CHANNEL')                 
%   ROI_PATH   - path to mask image with the same size like inputPath image
%   REF_PATH   - path to reference img with cell nuclei   
%   ROI_NAMES  - path to text file with roi names with format %i\t%s\n 

%%%ADRESSES%%%
inputPath = '../Test_Images/wholebrain_slice.tif';

ROI_PATH = '../Test_Images/wholebrain_atlas.tif';

ROI_NAMES = '../ARA/acronyms_ARA.txt';

REF_PATH = '';
%%%ADRESSES%%%
  

%%%PARAMETERS%%%
Cell_Width = 10;    %   width      - cell width (double)
THRES_W = 8;        %   THRES_W    - weighting factor for isodata threshold - default 10
MIN_DIST = 8;       %   MIN_DIST   - min tostance betwenne cells (double)
DARK_PEAKS = 1;     %   DARK_PEAKS - set to 1 for detecting dark cells in bright background (int)
BAR_FILTER = 1;     %   BAR_FILTER - set to 1 for detecting non circular cells e.g GFAP or IBA1
CHANNEL = 1;        %   CHANNEL    - color channel RGB (int) 1 - 3
NORM = '';          %   NORM       - set to 1 for normlaize cell number by region size
SAVE_DATA = '';     %   SAVE_DATA  - set to 0 for avoid saving images (.png) and peak coordinates (.txt)
RAD = '';           %   RAD        - distance between cell nuclei and current cells - default 1.5   
%%%PARAMETERS%%%



%% Function 

AIDAhisto(inputPath, Cell_Width, 'THRES_W', THRES_W, 'MIN_DIST', MIN_DIST, ...
    'DARK_PEAKS', DARK_PEAKS, 'BAR_FILTER', BAR_FILTER, 'CHANNEL',CHANNEL, ...
    'ROI_PATH', ROI_PATH, 'ROI_NAMES',ROI_NAMES, 'REF_PATH' ,REF_PATH,'RAD',RAD);
