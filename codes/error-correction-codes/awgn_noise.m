%txData = [0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0];
%rxData = awgn_noise(txData, 0.1);

function rxData = awgn_noise(txData, SNR)
    txData = transpose(txData);
    modSig = pskmod(txData, 2);        % Modulate
    rxSig = awgn(modSig, SNR);         % Pass through AWGN
    rxData = pskdemod(rxSig, 2);       % Demodulate
 %   biterr(txData,rxData);
end

