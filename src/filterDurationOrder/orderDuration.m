%
% 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
%
function [g] = durationOrder(outImgFolderPath)

    G = 1290; % largo señal
    N = 30; % largo respuesta al impulso
    g = 1:5:G;
    a = 0; % constante de proporcionalidad
    O1 = g + a; % MA
    O2 = g .* log(g) + a; % filtrado en Fourier y retorno a dominio temporal
    O3 = g.^2; % integral filtrada: y[n] = lamda*y[n-1] + (1-lambda)*x[n]

    figure()
    subplot(211)
    plot(g,O1,'linewidth',2)
    hold on
    plot(g,O2,'linewidth',2)
    hold on
    plot(g,O3,'linewidth',2)
    legend('O(G)','O(G log G)','O(G^2)')
    title(sprintf('Orden de duracion con G=%i',G))
    xlabel('Entradas de la senial')
    ylabel('No. operaciones')

    subplot(212)
    plot(g,O1,'linewidth',2)
    hold on
    plot(g,O2,'linewidth',2)
    hold on
    plot(g,O3,'linewidth',2)
    xlim([0,600])
    ylim([0,1000])
    legend('O(G)','O(G log G)','O(G^2)')
    xlabel('Entradas de la senial')
    ylabel('No. operaciones')

    print(strcat(outImgFolderPath, '/ordenDuracionFiltros.pdf'),'-dpdfwrite')

