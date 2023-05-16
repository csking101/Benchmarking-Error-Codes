function [decoded, cnumerr, ccode] = rs_decode(msg,m,n,k)
    f = gf(msg,m);
    [decoded,cnumerr,ccode] = rsdec(f,n,k);
    decoded = decoded.x;
    ccode = ccode.x;
end