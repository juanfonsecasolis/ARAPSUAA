%
% 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
%
function [I] = w2meansDurationOrder(outImgFolderPath)
    I = 1000;
    t = zeros(I,1);
    n = linspace(1,10000,I);
    for i = 1:I
        tic();
        x = rand(n(i),1);
        w = ones(n(i),1);
        w2means(x,w);
        t(i) = toc();
    end
    figure()
    plot(n,t)
    xlabel('No. entrada')
    ylabel('Tiempo (s)')
    print(strcat(outImgFolderPath, '/w2meansDurationOrder.pdf'),'-dpdfwrite')