%
% Author: Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
%

function [rutaSalida] = plotScores(scoreMatricesFolderPath,outImgFolderPath)

    addpath(scoreMatricesFolderPath)

    scripts = {
        'bancoCuckoo_sonidoCuckoo_kPropuesto3Arm',
        'bancoCuckoo_sonidoLowchirp_kPropuesto3Arm',
        'bancoCuckoo_sonidoHighchirp_kPropuesto3Arm',
        'bancoCuckoo_sonidoCuckoo_kPropuesto7Arm',
        'bancoCuckoo_sonidoLowchirp_kPropuesto7Arm',
        'bancoCuckoo_sonidoHighchirp_kPropuesto7Arm',
        %'highchirp_cuckoo_kPropuesto',
        %'highchirp_highchirp_kPropuesto',
        %'highchirp_lowchirp_kPropuesto',
        %'lowchirp_cuckoo_kPropuesto',
        %'lowchirp_highchirp_kPropuesto',
        %'lowchirp_lowchirp_kPropuesto',
    };

    nScripts = length(scripts);

    for iS=1:nScripts

        scriptPath = scripts{iS}; %strcat(scoreMatricesFolderPath, strcat('/', scripts{iS}));

        % printf('Analizando: "%s" ...\n', scriptPath)

        feval(scriptPath)
        figure()
        N = max(size(scores));
        t = linspace(0,D,N);
            %subplot(212)
        %[max_values, indices] = max(scores',[],1);
        %contour = f0s(indices);
        %contour = contour .* (alpha<max_values); % set to zero all f0s whose score is less the the threshold
            %plot(t,contour,'k')
            %xlabel('Tiempo (s)')
            %ylabel('F0 (kHz)')
            %xlim([0,D])
        %hold on
        %subplot(211)
        scores(scores<0)=0;
        scores = scores/max(max(scores));
        I = min(size(scores));
        colormap(flipud(ocean))
        imagesc(t,f0s,scores')
        set(gca,'YDir','normal')
        tokens = strsplit(scripts{iS},'_');
        %title(sprintf('Nucleo: %s - Archivo: %s', tokens{1}, tokens{2}));
        xlabel('Tiempo (s)')
        %colorbar('southoutside')
        ylabel('F0 (kHz)')
        set (gca, 'ytick', f0s)
        % plot grid when frequency value changes
        dfGrid = abs(f0s(2)-f0s(1));
        for iB=1:length(f0s)
            hold on
            yV = f0s(iB) + dfGrid/2;
            plot([0 N],[yV yV],'--','color',[0.5 0.5 0.5])
        end
        pbaspect ([4 2 1]);
        set(gca,'fontname','Times')  % Set it to times
        set(gca, 'fontsize', 12)
        rutaSalida = strcat(outImgFolderPath, strcat('/',strcat(scripts{iS},'.pdf')));
        %title(strrep(scripts{iS},'_','\_'))
        print(rutaSalida,'-dpdfwrite') % http://octave.1599824.n4.nabble.com/pdf-page-layout-td4650462.html

    end
    %pause
