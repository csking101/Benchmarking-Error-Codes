txData = [0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0];
rxData = rayleigh(txData);

% Defining object from RayleighChannel
raylchan = comm.RayleighChannel( ...
    'SampleRate',1e3, ...
    'PathDelays',[0 1.5e-3], ...
    'AveragePathGains',[0 -3], ...
    'PathGainsOutputPort',true);

chaninfo = info(raylchan);
coeff = chaninfo.ChannelFilterCoefficients;
Np = length(rayleighchan.PathDelays);
state = zeros(size(coeff,2)-1,size(coeff,1));
nFrames = 10;
chkChan = zeros(nFrames,1);

function rxData = rayleigh(txData)
    [chanout1,pg] = raylchan(txData);
    fracdelaydata = zeros(size(txData,1),Np);
    % Calculate the fractional delayed input signal.
    for ii = 1:Np
        [fracdelaydata(:,ii),state(:,ii)] = filter(coeff(ii,:),1,txData,state(:,ii));
    end
    % Apply the path gains and sum the results for all of the paths.
    % Compare the channel outputs.
    chanout2 = sum(pg .* fracdelaydata,2);
    rxData = pskdemod(chanout2, 2);
end