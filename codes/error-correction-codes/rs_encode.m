function code = rs_encode(msg,m,n,k)
    f = gf(msg,m)
    code = rsenc(f,n,k).x;
end