%% ISODATA ALGORITHM - for taking the threshold - Image processing

%  Author: Thuong HD - ASELAB - Hanoi University of Science and Technology
%  Date: 29-3-2018

function finalThreshold = isodataAlgorithm(grayImage)

grayImage =  grayImage(:);

% The itial threshol is equal the mean of grayscale image
initialTheta = mean(grayImage); 

initialTheta = round(initialTheta); % Rounding
i = 1;
threshold(i) = initialTheta;

% Gray levels are greater than or equal to the threshold
foregroundLevel =  grayImage(find((grayImage >= initialTheta)));
meanForeground = mean(foregroundLevel(:));

% Gray levels are less than or equal to the threshold
backgroundLevel = grayImage(find((grayImage < initialTheta)));
meanBackground = mean(backgroundLevel(:));

% Setup new threshold
i = 2;
threshold(i) = round((meanForeground + meanBackground)/2);

%Loop: Consider condition for threshold
while abs(threshold(i)-threshold(i-1))>=1
    
    % Gray levels are greater than or equal to the threshold
    foregroundLevel =  grayImage(find((grayImage >= threshold(i))));
    meanForeground = (mean(foregroundLevel(:)));
    
    % Gray levels are less than or equal to the threshold
    backgroundLevel = grayImage(find((grayImage < threshold(i))));
    meanBackground = (mean(backgroundLevel(:)));
    
    i = i+1;
    % Setup new threshold
    threshold(i) = round((meanForeground + meanBackground)/2);
    
end

finalThreshold = (threshold(end) - 1) / (255 - 1);