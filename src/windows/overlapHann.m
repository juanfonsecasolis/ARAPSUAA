function [f] = overlapHann(outImgFolderPath)

    F0 = 1000;
    Fs = 8000;
    FMax = 2.5*F0;
    f = 0:1:FMax;
    Tv = 8.0/F0;

    F1 = sinc((f-F0)*Tv) + 0.5*sinc(Tv*((f-F0)-1/Tv)) + 0.5*sinc(Tv*((f-F0)+1/Tv));
    F2 = sinc((f-2*F0)*Tv) + 0.5*sinc(Tv*((f-2*F0)-1/Tv)) + 0.5*sinc(Tv*((f-2*F0)+1/Tv));
    plot(f,F1+F2,'linewidth',2,'color','blue')
    xlim([F0/2,FMax])
    set (gca, 'xticklabel', {'0', 'F0', '', '2F0',''})
    yAxis = ylim;
    xAxis = xlim;
    cruceX = 2/Tv;
    corte1 = [F0+cruceX 0];
    corte2 = [2*F0-cruceX 0];
    line([xAxis(1) xAxis(2)],[0 0],'color','black','linestyle','--'); % eje x
    line([corte1(1) corte1(1)],[yAxis(1) yAxis(2)],'color','black','linestyle','--'); % corte 1
    line([corte2(1) corte2(1)],[yAxis(1) yAxis(2)],'color','black','linestyle','--'); % corte 2
    line([corte1(1) corte1(1)+cruceX/4],[0 0.4],'color','black','linestyle','-'); % etiqueta de corte 1
    line([corte2(1) corte2(1)-cruceX/2],[0 0.2],'color','black','linestyle','-'); % etiqueta de corte 2
    text(corte1(1)+cruceX/4,0.4,'F0+2/Tv')
    text(corte2(1)-cruceX*3/4,0.215,'2F0-2/Tv')
    xlabel('Frecuencia (Hz)')
    ylabel('Amplitud')
    copied_legend = findobj(gcf(),'type','axes','Tag','legend');
    set(copied_legend, 'fontsize', 1);
    saveas(1,strcat(outImgFolderPath,'/traslapeHann.pdf'),'pdf')
