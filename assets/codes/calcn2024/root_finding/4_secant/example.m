f = @(x)(x+1)^2-9;
g = @(x)2*x + 2;
disp(secant(f,-3 , 3 ,10^-6 , 100));