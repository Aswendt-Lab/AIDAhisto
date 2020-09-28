% Running run_example demonstrates the properties of AIDAhisto.
% All results are stored in the same folder as the image data.
% All identified cells are marked by a single pixel

%% whole brain
% Processsing wholebrain_slice.tif
fprintf("Processing wholebrain slice...\n")
AIDAhisto('../testImages/wholebrain_slice.tif',...
    10 ,'DARK_PEAKS', 1, 'BAR_FILTER', 1,'CHANNEL',1,'ROI_PATH',...
    '../testImages/wholebrain_atlas.tif');

%% low resoultion
% Processsing GFAP_lowResolution.tif with low resoltution
fprintf("Processing GFAP with blue channel...\n")
filename=AIDAhisto('../testImages/GFAP_lowResolution.tif',...
    8 , 'DARK_PEAKS', 1,'CHANNEL',3);

fprintf("Using blue channel as reference for red channel...\n")
AIDAhisto('../testImages/GFAP_lowResolution.tif',...
    10 , 'DARK_PEAKS', 1,'CHANNEL',1,'REF_PATH',[filename '.png']);

% Processsing IBA1_lowResolution.tif with low resoltution
fprintf("Processing IBA1 with blue channel...\n")
filename=AIDAhisto('../testImages/IBA1_lowResolution.tif',...
    8 , 'DARK_PEAKS', 1,'CHANNEL',3);

fprintf("Using blue channel as reference for green channel...\n")
AIDAhisto('../testImages/IBA1_lowResolution.tif',...
    10 , 'DARK_PEAKS', 1,'CHANNEL',2,'REF_PATH',[filename '.png']);

%% high resolution
% Processsing IBA1_lowResolution.tif with high resoltution
fprintf("Processing IBA1 with blue channel...\n")
filename=AIDAhisto('../testImages/IBA1_highResolution.tif',...
    25,'Channel',3);

fprintf("Using blue channel as reference for green channel...\n")
AIDAhisto('../testImages/IBA1_highResolution.tif',...
    25,'THRES_W',15,'Channel',1,'REF_PATH',[filename '.png']);

% Processsing GFAP_highResolution.tif with high resoltution
fprintf("Processing GFAP with blue channel...\n")
filename=AIDAhisto('../testImages/GFAP_highResolution.tif',...
    25,'Channel',3);

fprintf("Using blue channel as reference for green channel...\n")
AIDAhisto('../testImages/GFAP_highResolution.tif',...
    25,'THRES_W',10,'Channel',2,...
    'REF_PATH',[filename '.png']);