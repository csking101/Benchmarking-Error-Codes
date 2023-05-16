% txData = [0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0];
% rxData = impulse(txData, 0.5);

function noisy_data = impulse_noise(binary_data, p)
% Transpose the column vector
binary_data = transpose(binary_data)
% Generate uniform random numbers between 0 and 1
rand_nums = rand(size(binary_data));
rand_nums
% Find the indices of the elements in rand_nums that are less than p
impulse_indices = find(rand_nums < p);

% Create a copy of the binary data and set the impulse_indices to 1
noisy_data = binary_data;
noisy_data(impulse_indices) = ~noisy_data(impulse_indices);
end