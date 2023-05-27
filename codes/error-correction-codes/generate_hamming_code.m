function encoded_message = generate_hamming_code(message)
    % Determine the number of parity bits required
    k = length(message);
    n = 2^ceil(log2(k + 1)) - 1;
    encoded_message = encode(m  );
end