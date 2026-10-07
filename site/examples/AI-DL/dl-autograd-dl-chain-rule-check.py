# Leon | Original learning example
# Check a gradient and update the network
# Python 3.12+ | Run: python dl-autograd-dl-chain-rule-check.py
x, target = 2., 1.
w, b, v = 0.5, 0., 2.
def loss(weight, bias, output_weight):
    prediction = output_weight * max(0., weight*x+bias)
    return 0.5 * (prediction-target)**2
z = w*x+b; a = max(0., z); error = v*a-target
gv = error*a; gw = error*v*int(z>0)*x; gb = error*v*int(z>0)
epsilon = 1e-6
numeric = (loss(w+epsilon,b,v)-loss(w-epsilon,b,v))/(2*epsilon)
print(f'gradient w: {gw:.6f}; finite difference: {numeric:.6f}')
w, b, v = w-0.05*gw, b-0.05*gb, v-0.05*gv
print(f'new loss: {loss(w,b,v):.7f}')
