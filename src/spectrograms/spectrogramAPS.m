%
% Author: Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
%
function [paths] = spectrogramAPS(outImgFolderPath)

    pkg load signal

    paths = {
        'data/cucu_slsem5o2016_10_22_15_39_10.wav'
        'data/chirrido-alto_slsem7o2016_10_22_06_41_28.wav',
        'data/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav'
        'data/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav',
        'data/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav',
        'data/slsem0s2016_10_15_06_00_00.wav'
    };

    analizarToda = 0; % 1: gráficas usadas en sección de umbral adaptativo alfa, 0: usadas en apéndice de sonidos
    wLen = 512;
    for iP=1:length(paths)
        [x,fs] = wavread(paths{iP});
        if 0==analizarToda
            x=x(floor(numel(x)/4):floor(numel(x)/2.05));
        end
        figure()
        colormap(jet());
        specgram(x,wLen,fs,hamming(wLen),wLen/2);
        [dir, name, ext] = fileparts(paths{iP});
        nName = strrep(name,'_','\_');
        title(sprintf('Espectrograma: %s (fs=%i Hz)',nName,fs))
        xlabel('Tiempo (s)')
        ylabel('Frecuencia (Hz)')
        if analizarToda
            name = strcat(name,'_full')
        end

        %print(sprintf('%s.pdf',name),'-dpdfwrite')
        print(sprintf('%s/%s.png',outImgFolderPath,name),'-dpng')
    end
