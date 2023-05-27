function decoded = ldpc_decode(code,msg_len)
    iden = eye(msg_len);
    pcm = sparse([iden iden]);
    decoder = comm.LDPCDecoder(pcm);
    decoded_temp = decoder(code);
    decoded = 1-decoded_temp;
end