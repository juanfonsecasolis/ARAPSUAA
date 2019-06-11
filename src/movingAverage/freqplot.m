% ``Introduction to Digital Filters with Audio Applications'', by Julius O. Smith III, (September 2007 Edition).
% Copyright © 2019-01-09 by Julius O. Smith III
% Center for Computer Research in Music and Acoustics (CCRMA),   Stanford University
% https://ccrma.stanford.edu/~jos/filters/Frequency_Plots_freqplot_m.html
%
function freqplot(fdata, ydata, symbol, ttl, xlab, ylab)
% FREQPLOT - Plot a function of frequency.
%            See myplot for more features.

  if nargin<6, ylab=''; end
  if nargin<5, xlab='Frequency (Hz)'; end
  if nargin<4, ttl=''; end
  if nargin<3, symbol=''; end
  if nargin<2, fdata=0:length(ydata)-1; end

  plot(fdata,ydata,symbol); grid;
  if ttl, title(ttl); end
  if ylab, ylabel(ylab); end
  xlabel(xlab);
