% txData = [0;0;0;0;0;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0];
% rxData = rayleigh(txData);

function rxData = rayleigh(binary_data) 
    txData = transpose(binary_data);
    rayleighchan = comm.RayleighChannel( ...
        'SampleRate',1e3, ...
        'PathDelays',[0 1.5e-3], ...
        'AveragePathGains',[0 -3], ...
        'PathGainsOutputPort',true);
    
    chaninfo = info(rayleighchan);
    coeff = chaninfo.ChannelFilterCoefficients;
    Np = length(rayleighchan.PathDelays);
    state = zeros(size(coeff,2)-1,size(coeff,1));
    nFrames = 10;
    
    data = pskmod(txData, 2);
    [chanout1,pg] = rayleighchan(data);
    fracdelaydata = zeros(size(data,1),Np);
    % Calculate the fractional delayed input signal.
    for ii = 1:Np
        [fracdelaydata(:,ii),state(:,ii)] = ...
            filter(coeff(ii,:),1,data,state(:,ii));
    end
    % Apply the path gains and sum the results for all of the paths.
    % Compare the channel outputs.
    chanout2 = sum(pg .* fracdelaydata,2);
    rxData = pskdemod(chanout2, 2);
end
