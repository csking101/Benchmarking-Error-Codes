function code = polar(msg)
    msg = transpose(msg);
    E = 256;
    enc = nrPolarEncode(msg,E);
    length(enc)
    code = transpose(enc);