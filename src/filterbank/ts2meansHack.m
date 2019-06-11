function [juanmaCentroide] = ts2meansHack(x,dt,wdurationlim,wincrement,woverlap,bias)
% TS2MEANS Time series 2-means clustering
%    IDX = TS2MEANS( X, DT, [WDURATIONMIN WDURATIONMAX], WINCREMENT, 
%    WOVERLAP, BIAS) performs a dynamic weighted two-means clustering on 
%    the time series X, which is assumed to be uniformly sampled with time
%    interval DT seconds. The algorithm determines the clusters at every 
%    instant of time T by assigning the samples in the neighborhood of T to
%    the classes, using as optimization criteria the maximization of the 
%    distance between the centroids. The analysis is performed at different
%    scales by using window sizes that increase by a factor of WSINCREMENT 
%    (greater than 1). The minimum and maximum window durations (in 
%    seconds) are determined by WDURATIONMIN and WDURATIONMAX. The windows
%    are uniformly distributed over time with an overlap factor of WOVERLAP
%    (between 0 and 1). 
%
%    A postprocessing step is performed to avoid an undesirable situation
%    that sometimes occur when the value of the samples is close to the 
%    midpoint between the centroids: A block of samples is assigned to 
%    class 0 (the class normally associated to lower centroids) but the 
%    block is completely above a neighboring block assigned to class 1 
%    (the class normally associated to higher centroids), or vice versa. 
%    This situation is avoided by relabeling one of the blocks with the 
%    label of the other: If BIAS equals ?max? then class-0 blocks are 
%    relabeled as class-1 blocks, and if BIAS equals ?min? then it is done
%    the other way around.
%
%    IDX = TS2MEANS( X ) uses the default parameters: DT = 1 s, 
%    WDURATIONMIN = 0 s, WDURATIONMAX = duration of the time series, 
%    WINCREMENT = 2^1/2, WOVERLAP = 0.5, BIAS = ?max? if before the 
%    postprocessing the most populated class in IDX is class 1, and 
%    BIAS = ?min? if the most populad teclass is class 0.
%
%    IDX = TS2MEANS( X,...,[],... ) uses the default value for the 
%    parameter replaced with the placeholder [].
%
%    REMARKS: For better results, make WOVERLAP as large as possible and
%    WINCREMENT as small as possible. However, take into account that the
%    computational complexity of the algorithm is inversely proportional to
%    1-WOVERLAP and inversely proportional to the logarithm of WINCREMENT.
%    The default values have been found to produce empirically good 
%    results.
%
%    SOURCE: Camacho, A., ?Detection of Pitched/Unpitched Sound Using 
%    Pitch Strength Clustering?, Proceedings of the Ninth International
%    Conference on Music Information Retrieval, pp. 533-537, Philadelphia, 
%    September 2008.    
%
%
%    MAINTENANCE HISTORY:
%    - Fixed bug in line 80 that made TS2MEANS exclude some samples at the
%    end of the time series (12/2010)
if ~exist( 'dt', 'var' ) || isempty(dt), dt = 1; end
if dt<=0, error('Time interval must be positive.'), end
if ~exist( 'wdurationlim', 'var' ) || isempty(wdurationlim)
    wdurationlim = [ 0 (length(x)-1)*dt ];
end
if ~exist( 'wincrement', 'var' ) || isempty(wincrement), wincrement = sqrt(2); end
if wincrement<=1, error('Window increment factor must be greater than 1.'), end
if ~exist( 'woverlap', 'var' ) || isempty(woverlap), woverlap = 0.5; end
if woverlap>1 || woverlap<0, erorr('Window overlap must be between 0 and 1.'), end
if exist( 'bias', 'var' ) && ~strcmpi(bias,'max') && ~strcmpi(bias,'min')
    error('Invalid bias argument. Must be ''max'', ''min'', or [].')
end

% ----YAHA!-----
% Agregamos un vector c para saber cual fue la evolucion del 
% punto medio
juanmaCentroide = [];
% --------------

x = x(:); % Convert into column vector
t = [ 0: length(x)-1 ]' * dt; % Times
wsize = 2 .^ [ 2: log2(wincrement): log2(2*length(x)) ]';
wsize = 2 * round(wsize/2); % Force window sizes to be multiples of two
wsize = unique(wsize); % Remove repeated sizes
wduration = wsize * dt; % Window durations (in seconds)
tf = wduration > min(wdurationlim) & wduration < max(wdurationlim);
wduration = wduration(tf);
wsize = wsize(tf);
C = repmat( NaN, [ length(t), 2, length(wsize) ] ); % Cluster centroids
d = repmat( NaN, [ length(t), length(wsize) ] ); % Distance between centroids
for i = 1 : length(wsize) 
    dn = max( 1, round( (1-woverlap) * wsize(i) ) ); % Hop size (in samples)
    % Pad signal with NaNs
    xnp = [ repmat( NaN, wsize(i)/2, 1 ); x; repmat( NaN, dn + wsize(i), 1 ) ];
    % Segment input into columns of a matrix 
    ti = [ 0: wduration(i)*(1-woverlap): t(end) + wduration(i)*(1-woverlap) ];
    base = repmat( round( ti/dt+1 ), wsize(i), 1 );
    displacement = repmat( (0:wsize(i)-1)', 1, length(ti) );
    X = xnp( base + displacement );
    % Compute clusters' (weighted) centroids
    w = hanning( wsize(i) ); % Weighting window
    Ci = repmat( NaN, 2, size(X,2) ); % Cluster centroids for this wsize
    for j = 1:size(X,2)
        k = ~isnan( X(:,j) );
        [IDX,c] = w2means( X(k,j), w(k) ); % Weighted 2-means algorithm
        Ci(:,j) = c';
    end
    C(:,:,i) = interp1( ti, Ci', t ); % Interpolate at desired times
    d(:,i) = C(:,2,i) - C(:,1,i); % Distance between centroids
end
% Choose windows with maximum centroids separation
[v,ind] = max(d,[],2); 
ind1 = sub2ind( size(C), (1:size(C,1))', repmat(1,size(C,1),1), ind );
ind2 = sub2ind( size(C), (1:size(C,1))', repmat(2,size(C,1),1), ind );
c = [ C(ind1), C(ind2) ];
% Compute midpoint between centroids
m = mean(c,2);
juanmaCentroide = [juanmaCentroide, m];
% Use midpoint as threshold to determine the class
idx = x > m;
% Remove undesired class switchings in the neighborhood of the midpoint
if exist( 'bias', 'var' )
    bias = strcmp(bias,'max');
else
    % Bias towards most likely class
    bias = mean(idx) > 0.5;
end
idx = postprocessing( x, idx, bias );
if 1 % set this to 0 to turn plotting off
    clf
    hold on
    plot(t(idx),(x(idx)),'.c')
    plot(t(~idx),(x(~idx)),'.g')
    
    plot(t,fliplr(c),'-','linewidth',2)
    plot(t,m,'-r','linewidth',2)
    xlim([t(1) t(end)])
    grid on
    xlabel('Time (s)');
    legend('C1','C0','C1 centroid','C0 centroid','Midpoint','Location','BestOutside')
end

function [i,m] = w2means(x,w)
x = x(:);
w = w(:)';
maxIter = 100;
[v,i] = min( [ abs(x-min(x)), abs(x-max(x)) ], [], 2 );
i = i == 2;
iOld = repmat(nan,size(i));
nIter = 0; % maximum number of iterations
while any( i ~= iOld ) && nIter < maxIter
    nIter = nIter+1;
    iOld = i;
    % Compute new weighted means
    ni = ~i;
    wni = w(ni);
    wni = wni / sum(wni);
    wi = w(i);
    wi = wi / sum(wi);
    m = [ wni*x(ni), wi*x(i) ]; % Means
    if length(m) == 1
        i = repmat(nan,size(x));
        m = [m,m];
        return
    end
    d = [ abs(x-m(1)), abs(x-m(2)) ];
    [v,i] = min(d,[],2);
    i = i == 2;
end

function i = postprocessing(x,i,b)
d = diff(i); 
c = find( abs(d) ~= 0 ); % Find changes of class
if length(c) == 1
    k = 1 : c;
    l = c+1 : length(i);    
    if d( c ) > 0
        if min( x(k) ) > max( x(l) ) 
            if b
                i(k) = 1;
            else
                i(l) = 0;
            end
        end
    else
        if max( x(k) ) < min( x(l) )
            if ~b
                i(k) = 0;
            else
                i(l) = 1;
            end
        end
    end    
else
    k =      1 : c(1);
    l = c(1)+1 : c(2);    
    if d( c(1) ) > 0
        if min( x(k) ) > max( x(l) )
            if b
                i(k) = 1;
            else
                i(l) = 0;
            end
        end
    else
        if max( x(k) ) < min( x(l) )
            if ~b
                i(k) = 0;
            else
                i(l) = 1;
            end
        end
    end
	for j = 2 : length(c)-1
        k = c(j-1)+1 : c( j );
        l = c( j )+1 : c(j+1);
        if d( c(j) ) > 0
            if min( x(k) ) > max( x(l) )
                if b
                    i(k) = 1;
                else
                    i(l) = 0;
                end
            end
        else
            if max( x(k) ) < min( x(l) )
                if ~b
                    i(k) = 0;
                else
                    i(l) = 1;
                end
            end
        end
	end
	k = c(end-1)+1 : c(end);
	l = c( end )+1 : length(i);
    if d( c(end) ) > 0
        if min( x(k) ) > max( x(l) )
            if b
                i(k) = 1;
            else
                i(l) = 0;
            end
        end
    else
        if max( x(k) ) < min( x(l) )
            if ~b
                i(k) = 0;
            else
                i(l) = 1;
            end
        end
    end
end


