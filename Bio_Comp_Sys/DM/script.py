import numpy as np
import matplotlib.pyplot as plt
from sympy.matrices import Matrix
from scipy.integrate import odeint

#Exercice 1
#Q1)
M_q1 = np.array([[-2, 2, -1, 1],
                 [1, -1, -1, 1],
                 [0, 0, 1, -1]])

M_q1 = Matrix(M_q1)
res_q1 = M_q1.transpose().nullspace()

#Q4)
#On  simule les équations 
# P+P -a-> P2
# P2 -b-> P+P
# P+P2 -a-> P3
# P3 -b-> P+P2 

def f(X, t, a, b):
    P, P2, P3 = X[0], X[1], X[2]
    return [(-2*a*P*P)+(2*b*P2)-(a*P*P2)+(b*P3), 
            (a*P*P)-(b*P2)-(a*P*P2)+(b*P3),
            (a*P*P2)-(b*P3)]

t_max = 0.5
X0 = [6, 3, 1] # conditions initiale A,B,C
N = 50
tvals = np.linspace(0, t_max, N+1)
K = (3, 5)

Xvals = odeint(f, X0, tvals, args=K)

plt.figure(figsize=(10,5))
plt.plot(tvals, Xvals, label=["P","P2","P3"])
plt.plot(tvals, Xvals[:,0]+2*Xvals[:,1]+3*Xvals[:,2], '--', label="P+2P_2+3P_3")
plt.title("Simulation de P+P <-a,b-> P2, P+P2 <-a,b-> P3")
plt.xlabel("t")
plt.ylabel("Concentration")
plt.grid()
plt.legend()
plt.savefig("graph_ex1_q4.png")
plt.show()
plt.close()

if __name__ == "__main__":
    print("Exercice 1 :")
    print("Q1)")
    print("coeff p_0, p1_0, p2_0 =", res_q1[0].transpose())
