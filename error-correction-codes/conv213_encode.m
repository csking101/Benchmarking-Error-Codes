function coded = conv213_encode(msg)
    K = 3;
    G1 = 7;
    G2 = 5;
    trel = poly2trellis(K,[G1,G2]);
    coded = convenc(msg,trel);
end