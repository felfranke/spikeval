function H = EntropyH( Prob)
%Entropy of a discrete random variable Probdist taking K values

K = size(Prob,1);
logP = zeros(K,1);

%logP= log(Prob);

for k = 1:K
    if Prob(k) == 0
        logP(k) = 0; %avoid the minus infinity when Prob(k) = 0
    else
        logP(k) = log(Prob(k));
    end
end

H = -dot(Prob,logP);


end

