function coded = ldpc_encode(msg)
    msg_len = length(msg);

    iden = eye(msg_len);

    pcm = sparse([iden iden]);

    encoder = comm.LDPCEncoder(pcm); 

    coded = encoder(msg);

end


