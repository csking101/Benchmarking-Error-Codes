
function decoded_message = decode_hamming_code(encoded_message)
    % Determine the number of parity bits
    n = length(encoded_message);
    m = log2(n + 1);
    
    % Calculate syndrome bits
    syndrome = zeros(1, m);
    for i = 1:m
        syndrome(i) = calculate_parity_bit(encoded_message, 2^(i - 1));
    end

    % Correct errors, if any
    error_position = bi2de(fliplr(syndrome));
    if error_position ~= 0
        encoded_message(error_position) = mod(encoded_message(error_position) + 1, 2);
    end

    % Retrieve the original message
    decoded_message = encoded_message(1:n - m);
end
