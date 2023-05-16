function [decoded,cnumerr,ccode] = bch_decode(code,n,k)
    c = gf(code);
    [d,err,cc] = bchdec(c,n,k);
    decoded = d.x;
    cnumerr = err;
    ccode = cc.x;
end