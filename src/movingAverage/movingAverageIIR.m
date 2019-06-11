function [w] = movingAverageIIR(outFolderPath)
    pkg load signal;
    %graphics_toolkit("gnuplot")

    %
    % resp. frecuencia
    % H = B/A
    %

    N = 8;
    lambda = 0.98;
    B = [1-lambda];
    A = [1,-lambda];
    w = -pi:(pi/500):pi;
    [H,W]=freqz(B,A,w);

    % retardo de grupo
    figure(1)
    [g,wG] = grpdelay(B,A);
    plot([fliplr(-wG),wG],[fliplr(g),g],'linewidth',3,'b')
    xlabel('Frecuencia (rad/s)')
    ylabel('Entradas')
    xlim([-pi,pi])
    %grid on
    print(strcat(outFolderPath, '/retardoGrupoIntegralFiltrada.pdf'),'-dpdfwrite')
    %grid off

    figure(2)
    subplot(211)
    plot(W,abs(H),'linewidth',2)
    xlim([-pi,pi])
    xlabel('Frecuencia (rad/s)')
    ylabel('|H(z)|')

    subplot(212)
    plot(W,unwrap(angle(H)),'linewidth',2)
    xlabel('Frecuencia (rad/s)')
    ylabel('\angle H(z)')
    xlim([-pi,pi])
    print(strcat(outFolderPath, '/freqzMediaMovilIIR.pdf'),'-dpdfwrite')

    figure(3)
    zplane(B,A)
    %set(gca,'linewidth',2)
    xlabel('Parte real')
    ylabel('Parte imaginaria')
    print(strcat(outFolderPath, '/zplaneIIR.pdf'),'-dpdfwrite')





