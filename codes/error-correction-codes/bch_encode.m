function code = bch_encode(m,n,k)
    
    msg = gf(m);
    c = bchenc(msg,n,k);
    code = c.x;
end