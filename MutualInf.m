function [ Inf ] = MutualInf(Prob,Probprime, ProbJoint )
%Mutual information between the associated random variables
%Prob, Probprime and their joint distribution ProbJoint

K = size(Prob,1);
Kprime = size(Probprime,1);
Infie = zeros(K,Kprime);
logie = zeros(K,Kprime);

%Inf=0;
for i = 1:K
  for j = 1:Kprime
    if ProbJoint(i,j) == 0
      Infie(i,j) = 0;
    else
      %logie(i,j)= log(ProbJoint(i,j)/(Prob(i)*Probprime(j)));
      %Inf = Inf + ProbJoint(i,j).*( log(ProbJoint(i,j)/(Prob(i)*Probprime(j))) );
      Infie(i,j) = ProbJoint(i,j).*( log(ProbJoint(i,j)/(Prob(i)*Probprime(j))) );
    end
    %Infie(i,j) = ProbJoint(i,j).*( logie(i,j) );
  end
end

%Inf.logie=logie;
Inf.inf = sum(sum(Infie));
Inf.infie=Infie;

end

