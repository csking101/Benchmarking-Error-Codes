%Test Fountain

%flag to control implementation
LTFlag = 0;

%******
%parameters
K = 520;
MaxN = 1016; %maximum N

%parameters for Reed-Solomon Raptor code
FountainDelta = 1.1; %to determine the N of the outer code for Raptor
RS_Base = 8;
NRaptor = ceil(K/RS_Base*FountainDelta);
if floor((NRaptor-K)/2) ~= (NRaptor-K)/2
    error('Code rate infeasible');
end
if floor(K/RS_Base) ~= K/RS_Base
    error('Change FountainDelta or K');
end
NRaptorBig = 2^(ceil(log2(NRaptor + 1))) - 1;

RaptorCoderRS = fec.rsenc(NRaptorBig, K/RS_Base);
RaptorPuncRS = RaptorCoderRS.PuncturePattern;
RaptorPuncture = NRaptorBig - NRaptor;
RaptorPuncRS(end - RaptorPuncture + 1: end) = ~(RaptorPuncRS(end - RaptorPuncture + 1: end));
RaptorCoderRS.PuncturePattern = RaptorPuncRS;
RaptorDecoderRS = fec.rsdec(RaptorCoderRS);

LTBase = 8; %base for codeword 
MatrixBase = 2; %base for codeword 
%(Note: for matrix implementation, MatrixBase has to be a GF field, i.e, prime or power of prime)
% This implementation supports prime base only till base=7. For other bases, fill in the
% lookup table at MakeLoopUp.m. For non-prime bases, matrix inversion will
% have to be in gf.
%******

%current N: this value should change as part of a loop
CurrentN = floor(MaxN/4*3);

%Fountain matrix
if LTFlag
    G = GenerateG(K, CurrentN); %LT
    G_Raptor = GenerateG(NRaptor*RS_Base, CurrentN);
else
    G = GenerateGMatrix(K, CurrentN); %Matrix
    G_Raptor = GenerateGMatrix(NRaptor*RS_Base, CurrentN);
end

%-------------------
%generate message
msg = randi(RaptorDecoderRS.N, K/RS_Base, 1);
if LTFlag
    Bits = (dec2base(msg, LTBase, RS_Base))';
else
    Bits = (dec2base(msg, MatrixBase, RS_Base))';
end
Bits = (Bits(:))';
BitsVec = zeros(length(Bits), 1);
for Ind = 1: length(Bits)
    BitsVec(Ind) = str2double(Bits(Ind));
end
%-----------------
%encode

%Fountain
if LTFlag
    F = EncodeFountain(G, BitsVec, LTBase);
else
    F = EncodeFountain(G, BitsVec, MatrixBase);
end

%Raptor
RaptorCodeRS = encode(RaptorCoderRS, msg);

%Transfer into base
if LTFlag
    RaptorCodeRS_Sym = (dec2base(RaptorCodeRS, LTBase, RS_Base))';
else
    RaptorCodeRS_Sym = (dec2base(RaptorCodeRS, MatrixBase, RS_Base))';
end
RaptorCodeRS_Sym = RaptorCodeRS_Sym(:);
RaptorCodeRS_SymVec = zeros(length(RaptorCodeRS_Sym), 1);
for ind = 1: length(RaptorCodeRS_Sym)
