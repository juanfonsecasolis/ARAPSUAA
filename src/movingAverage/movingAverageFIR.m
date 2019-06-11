function [w] = movingAverageFIR(outFolderPath)
    pkg load signal;
    %graphics_toolkit("gnuplot")

    N = 30;
    B = ones(1,N);
    A = 1;
    w = -pi:(pi/500):pi;
    W = w;

    absH = 1/N * sin(w*N/2)./sin(w/2);
    angH = exp(-j*(N-1)/2*w);
    %[H,W]=freqz(B,A,w);

    % retardo de grupo
    figure(1)
    [g,wG] = grpdelay(B,A);
    plot([fliplr(-wG),wG],[fliplr(g),g],'linewidth',3,'b')
    xlabel('Frecuencia (rad/s)')
    ylabel('Entradas')
    xlim([-pi,pi])
    %grid on
    print(strcat(outFolderPath ,'/retardoGrupoMA.pdf'),'-dpdfwrite')
    %grid off

    figure(2)
    subplot(211)
    plot(W,abs(absH),'linewidth',2)
    xlim([-pi,pi])
    xlabel('Frecuencia (rad/s)')
    ylabel('|H(z)|')

    subplot(212)
    plot(W,angle(angH),'linewidth',2)
    xlabel('Frecuencia (rad/s)')
    ylabel('\angle H(z)')
    xlim([-pi,pi])
    print(strcat(outFolderPath, '/freqzMediaMovil.pdf'),'-dpdfwrite')

    figure(3)
    zplane(B,A)
    %set(gca,'linewidth',2)
    xlabel('Parte real')
    ylabel('Parte imaginaria')
    print(strcat(outFolderPath, '/zplane.pdf'),'-dpdfwrite')

