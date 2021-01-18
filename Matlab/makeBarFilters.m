function F=makeBarFilters(size)
% Returns Bar filter bank of given size
% modified version of code provided at
% http://www.robots.ox.ac.uk/~vgg/research/texclass/filters.html
% see this website for details.

  SUP=size;                 % Support of the largest filter (must be odd)
  SCALEX=[1,2,4];         % Sigma_{x} for the oriented filters
  NORIENT=6;              % Number of orientations

  NBAR=length(SCALEX)*NORIENT;
  NF=NBAR;
  F=zeros(SUP,SUP,NF);
  hsup=(SUP-1)/2;
  [x,y]=meshgrid([-hsup:hsup],[hsup:-1:-hsup]);
  orgpts=[x(:) y(:)]';

  count=1;
  for scale=1:length(SCALEX)
    for orient=0:NORIENT-1
      angle=pi*orient/NORIENT;  % Not 2pi as filters have symmetry
      c=cos(angle);s=sin(angle);
      rotpts=[c -s;s c]*orgpts;
      F(:,:,count)=makefilter(SCALEX(scale),0,2,rotpts,SUP);
      count=count+1;
    end
  end

return

function f=makefilter(scale,phasex,phasey,pts,sup)
  gx=gauss1d(3*scale,0,pts(1,:),phasex);
  gy=gauss1d(scale,0,pts(2,:),phasey);
  f=normalise(reshape(gx.*gy,sup,sup));
return

function g=gauss1d(sigma,mean,x,ord)
% Function to compute gaussian derivatives of order 0 <= ord < 3
% evaluated at x.

  x=x-mean;num=x.*x;
  variance=sigma^2;
  denom=2*variance;  
  g=exp(-num/denom)/(pi*denom)^0.5;
  switch ord
    case 1, g=-g.*(x/variance);
    case 2, g=g.*((num-variance)/(variance^2));
  end
return

function f=normalise(f), f=f-mean(f(:)); f=f/sum(abs(f(:))); return