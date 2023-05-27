function code = polar_encode(msg)
    msg = transpose(msg);
    E = length(msg);
    code = nrPolarEncode(msg,E);