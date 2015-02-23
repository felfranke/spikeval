function [ metric ] = VImetric( ConfusionMatrix )
%Computes Marina Meila's Variation of Information Metric 
%between two clusterings of the same data

[nbKlust,nbKlustprime] = size(ConfusionMatrix);

Pk = zeros(nbKlust,1);
Pkprime = zeros(nbKlustprime,1);
%PJoint = zeros(nbKlust, nbKlustprime);

totalN = sum(sum(ConfusionMatrix));

for k = 1:nbKlust
 Pk(k) = sum(ConfusionMatrix(k,:))/totalN;
end

for k = 1:nbKlustprime
 Pkprime(k) = sum(ConfusionMatrix(:,k))/totalN;
end

PJoint = ConfusionMatrix/totalN;

HC = EntropyH(Pk);
HCprime = EntropyH(Pkprime);
Inf = MutualInf(Pk,Pkprime,PJoint);

metric.VI = HC+HCprime - 2*Inf.inf;

metric.Inf=Inf;
metric.PJoint = PJoint;
metric.Pk = Pk;
metric.Pkprime = Pkprime;
metric.HC = HC;
metric.HCprime = HCprime;

end

