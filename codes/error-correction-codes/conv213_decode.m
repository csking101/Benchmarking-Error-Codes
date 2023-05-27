function decoded = conv213_decode(code)
    k=3;g1=7;g2=5;
    trel = poly2trellis(k,[g1 g2]);
    decoded = vitdec(code,trel,2,'trunc','hard');
end