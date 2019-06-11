%
% Author: Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
%
function [f] = erb(outImgFolderPath)
    d = 1:36;
    f = (2.^(d./5.7)-1)*230;
    plot(d,f,'linewidth',2)
    xlabel('Distancia desde la cuspide (mm)')
    ylabel('Frecuencia (Hz)')
    xlim([0, 36])
    grid on
    print(strcat(outImgFolderPath, '/escalaERB.pdf'),'-dpdfwrite')
