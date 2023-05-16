txData = [0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0];
rxData = phase(txData, 120, 10, 0);

function [noisy_data] = phase(data, phase_noise_power, sample_rate, f_offset)
    % Inputs:
    % - data: Binary data as a row vector.
    % - phase_noise_power: Power of the phase noise in dBc/Hz.
    % - sample_rate: Sampling rate of the data in Hz.
    % - f_offset: Frequency offset of the phase noise in Hz.
    
    % Generate phase noise
    time = 0:(1/sample_rate):(length(data)/sample_rate - 1/sample_rate);
    phase_noise = sqrt(2*10^(phase_noise_power/10)/sample_rate) * cos(2*pi*f_offset*time + 2*pi*rand);
    
    % Apply phase noise to data
    noisy_data = data .* exp(1i*phase_noise);
    
    % Convert back to binary
    noisy_data = real(noisy_data) >= 0;
end
