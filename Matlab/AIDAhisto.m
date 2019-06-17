function [fileStr,peaks,peaks_coord]=AIDAhisto(inputPath, width, varargin)
%% AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology
%
% Syntax:  peaks = AIDAhisto(input_Image, width, 'CHANNEL', int ,...
%                           'MIN_DIST', double, 'BAR_FILTER', boolean...
%                            'DARK_PEKAS',boolean,'SAVE_DATA'str,...
%                            'ROI_PATH',str)
% Inputs:
%   inputPath  - path to input grayscale image
%                or color image (see parameter 'CHANNEL')                 
%   width      - cell width (double)
% Parameter 
%   CHANNEL    - color channel RGB (int) 1 - 3 
%   MIN_DIST   - min tostance betwenne cells (double)
%   BAR_FILTER - set to 1 for detecting non circular cells e.g GFAP or IBA1
%   DARK_PEAKS - set to 1 for detecting dark cells in bright background (int)
%   SAVE_DATA  - set to 0 for avoid saving images (.png) and peak coordinates (.txt)
%   ROI_PATH   - path to mask image with the same size like inputPath image
%   THRES_W    - weighting factor for isodata threshold - default 10
%   RAD        - distance between cell nuclei and current cells - default 1.5   
%   REF_PATH   - path to reference img with cell nuclei   
%
% Outputs:
%   peaks       - 2D binary images with peaks
%   peaks_coord - coordinates of peaks
%

% Author: Niklas Pallast
% Neuroimaging & Neuroengineering
% Department of Neurology
% University Hospital Cologne
% Kerpener Str. 62
% 50937 Cologne, Germany
% Mar 2019; Last revision: 12-May-2004
%------------- BEGIN CODE --------------
%% read parameters
tic;
ch =1;
darkPeaks=0;
save_data=1;
filterType = 0;
thresw = 10;
refPath = '';
roiPath = '';
roiNames = '';
i = 1 ;
rad = 1.5;
while length(varargin)>i
    parameter = varargin{i};
    val = varargin{i+1};
    i = i+2;
    switch upper(parameter)
        case 'CHANNEL'
            ch=val;
            if val > 3
                error(['Input parameter ' num2str(val) ' is no valid RGB channel'])
            end
        case 'MIN_DIST'
            min_dist = val;
        case 'DARK_PEAKS'
            darkPeaks=val;
        case 'BAR_FILTER'
            filterType = val;
        case 'SAVE_DATA'
            save_data = val;      
        case 'ROI_PATH'
            roiPath = val;
        case 'THRES_W'
            thresw = val;
        case 'REF_PATH'
            refPath = val;
        case 'RAD'
            rad = val;
        case 'ROI_NAMES'
            roiNames = val;
        otherwise
            error(['Unknown parameter name ' parameter])
    end
end


if exist(inputPath,'file')
    if save_data == 1
        [p,f]=fileparts(inputPath);
        
        fileStr = fullfile(p,[f 'CH_' num2str(ch)]);
    end
    input_Image = imread(inputPath);
    if size(input_Image,3)>1
        input_Image = input_Image(:,:,ch);
    end
else
    error('Input path does not exist')
end
if width<0
    error("The Cell width has to be larger than 0")     
end

if ~exist('mind_dist','var')
    min_dist = round(width/2);
end

if darkPeaks == 1
    input_Image = imcomplement(input_Image);
end

if sum(input_Image(:))==0
    error(['There is no image information in channel ' num2str(ch)])
end

%% poof Image size - the calculation is proceeded on a downscale image
x_s = size(input_Image,1);
y_s = size(input_Image,2);
if (x_s*y_s)>100000000
    input_Image =imresize(input_Image,0.2);
end

%% apply AIDAhist
disp("Finding Kernel");
if filterType == 1
    
    kernel = makeBarFilters(width);
    
    imageVec = zeros([size(input_Image'),size(kernel,3)]);
    disp("Convolution")
    for i=1:size(kernel,3)
        imageVec(:,:,i)=conv2(input_Image',kernel(:,:,i),'same');
    end
    image = (mean(imageVec,3));
else
      kernel = makeSfilters(width);
    imageVec = zeros([size(input_Image'),size(kernel,3)]);
    disp("Convolution")
    for i=1:size(kernel,3)
        imageVec(:,:,i)=conv2(input_Image',kernel(:,:,i),'same');
    end
    image = imcomplement(mean(imageVec,3));
end


disp("Thresholding")
threshold = thresw*isodataAlgorithm(input_Image);
for i = 1:size(image,1)
    for j = 1:size(image,2)
        if (image(i,j) < threshold)
            image(i,j) = threshold;
        end
        image(i,j) = image(i,j)-threshold;
    end
end


disp("Finding Maximums");
neighborhood = filldisc(floor(min_dist));
J = imdilate(image,neighborhood);
peaks= image==J;
peaks(image==0)=0;

peaks=peaks';
[r,c] = find(peaks==1);
peaks_coord=[r,c];
fprintf("Found %i cells\n", size(peaks_coord,1));
%% save image and peak coordinates if SAVE_DATA=1
disp("Save data");
if save_data==1
    figure;
    % save and plot image
    se = strel('disk',2);
    imshow(imoverlay(uint8(255*mat2gray(input_Image)),imdilate(peaks,se),'r'),[])
    
    if (x_s*y_s)>100000000
        peaks =imresize(peaks,[x_s,y_s]);
        input_Image = imresize(input_Image,[x_s,y_s]);
    end
    
    imwrite(peaks,[fileStr '.png'])
    % save txt
    fileID = fopen([fileStr '.txt'],'w');
    fprintf(fileID, 'AIDAhisto - advanced Image-based Tool for Counting Nuclei \nNumber of identified Cells %i \n\n',length(peaks_coord));
    for i=1:length(peaks_coord)
        fprintf(fileID,'%i %i\n',peaks_coord(i,2),peaks_coord(i,1));
    end
    
    fclose(fileID);
end


%% find next cell nuclei in reference channel of REF_CH
if exist(refPath,'file')
    
    img_refPeaks=imread(refPath);
    [r,c] = find(img_refPeaks==1);    
    peaks_coord_ref=[r,c];

    [idx,distance] = knnsearch(peaks_coord,peaks_coord_ref,'K',1);
    idx=idx(distance<min_dist*rad);
    
    idx_unique = unique(idx);
    idx_unique(idx_unique==0)=[];
    
    coord_verified=[peaks_coord(idx_unique,1) peaks_coord(idx_unique,2)];
    peaks_verified = false(size(img_refPeaks));
    for i=1:size(coord_verified,1)
        peaks_verified(coord_verified(i,1),coord_verified(i,2))=1;
    end
    found_refCells = length(coord_verified);
    fprintf("Verified cells %i\n", found_refCells);
    if save_data==1
        
        % save and plot image with verified cells 
        figure;
        imshow(imoverlay(input_Image,peaks_verified,'g'))
        imwrite(peaks_verified,[fileStr '_v.png'])
        
        % save txt
        fileID = fopen([fileStr '_v.txt'],'w');
        fprintf(fileID, 'AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology \nNumber of identified Cells %i \nx-y Cell Postitions \n',found_refCells);
        for i=1:size(coord_verified,1)
            fprintf(fileID,'%i %i\n',coord_verified(i,2),coord_verified(i,1));
        end
        
        fclose(fileID);
    end
end


%% process registered atlas given with ROI_PATH
if exist(roiPath,'file')
    mask = double(imread(roiPath));
    if size(peaks) ~= size(mask)
        disp('Dimension of input image and mask do not agree')
    else
        roiNo = unique(mask);
        fprintf('Processing %i ROIs\n',length(roiNo))
        cells = zeros(size(roiNo));
        for i = 1:length(roiNo)
            roi = roiNo(i);
            cells(i)=sum(peaks(mask==roi));
        end
        % save txt
        if exist(roiPath,'file')
            fileID = fopen([fileStr 'ROIs.txt'],'w');
            fileROIID = fopen(roiPath,'r');
            textROI =textscan(fileROIID,'%s%s%[^\n\r]','Delimiter', '\t', 'TextType', 'string');
            textROINum = textROI{1};
            textROIAcro = textROI{2};
            fprintf(fileID, 'AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology \nNumber of identified Cells in %i given ROIs \n\n',length(roiNo));
            for i=1:length(cells)
                fprintf(fileID,'%i %i\n',roiNo(i),cells(i));
            end
        else
            fileID = fopen([fileStr 'ROIs.txt'],'w');
            fprintf(fileID, 'AIDAhisto: Atlas-based imaging data analysis tool for mouse brain histology \nNumber of identified Cells in %i given ROIs \n\n',length(roiNo));
            for i=1:length(cells)
                fprintf(fileID,'%i %i\n',roiNo(i),cells(i));
            end
        end
        
        fclose(fileID);
    end
    
end

toc;
fprintf('\n')
end

%% get neighborhood
function y = filldisc(radius)
%FILLDISC  Returns an array with a disc full of ones.
%    Y = FILLDISC(R)  Returns a square array of size 2*ROUND(R)+1.
%    Elements less than R from the central elements are set to 1, rest to
%    0. This is done fairly efficiently, taking advantage of symmetries.

% Copyright David Young 2010

rsq = radius * radius;
R = round(radius);
c = R + 1;
t = 2*R + 1;
y = zeros(t);

% points on St George's cross
y(:, c) = 1;
y(c, :) = 1;

for rstart = 1:R
    rend = round(sqrt(rsq - rstart * rstart));
    if rend < rstart
        break
    end
    
    % points on St Andrew's cross
    y(c+rstart, c+rstart) = 1;
    y(c+rstart, c-rstart) = 1;
    y(c-rstart, c+rstart) = 1;
    y(c-rstart, c-rstart) = 1;
    
    % fill in octants
    y(c+rstart:c+rend, c+rstart) = 1;
    y(c+rstart:c+rend, c-rstart) = 1;
    y(c-rend:c-rstart, c+rstart) = 1;
    y(c-rend:c-rstart, c-rstart) = 1;
    y(c+rstart, c+rstart:c+rend) = 1;
    y(c-rstart, c+rstart:c+rend) = 1;
    y(c+rstart, c-rend:c-rstart) = 1;
    y(c-rstart, c-rend:c-rstart) = 1;
end

end

