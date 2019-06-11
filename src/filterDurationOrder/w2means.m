function [i,m] = w2means(x,w)
%    SOURCE: Camacho, A., ?Detection of Pitched/Unpitched Sound Using
%    Pitch Strength Clustering?, Proceedings of the Ninth International
%    Conference on Music Information Retrieval, pp. 533-537, Philadelphia,
%    September 2008.
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
