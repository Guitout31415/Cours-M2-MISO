import numpy as np
import matplotlib.pyplot as plt
from sympy.matrices import Matrix
from scipy.integrate import odeint
from sympy.core.symbol import symbols
from sympy.solvers.solveset import nonlinsolve

#Exercice 1
#Q1)
M_q1 = np.array([[-2, 2, -1, 1],
                 [1, -1, -1, 1],
                 [0, 0, 1, -1]])

M_q1 = Matrix(M_q1)
res_q1 = M_q1.transpose().nullspace()
########################################
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
t_max = 5
X01 = [6, 0, 1] # 1ere conditions initiale P,P2,P3
X02 = [2, 2, 2] # 2eme conditions initiale P,P2,P3
X03 = [0, 1, 3] # 3eme conditions initiale P,P2,P3
X04 = [2, 5, 3] # 4eme conditions initiale P,P2,P3
N = 50
tvals = np.linspace(0, t_max, N+1)
K1 = (1, 0.5)
K2 = (1.2, 0.2)
K3 = (1, 0.25)
K4 = (2, 1)
Xvals1 = odeint(f, X01, tvals, args=K1)
Xvals2 = odeint(f, X02, tvals, args=K2)
Xvals3 = odeint(f, X03, tvals, args=K3)
Xvals4 = odeint(f, X04, tvals, args=K4)
########################################
#Q6)
p0, p20, p30, a, b, P0, P20, P30 = \
symbols("p0, p20, p30, a, b, P0, P20, P30", real=True)

T = np.linspace(0,1000,100)
y = []
for t in T: 
    sys = [P0-t, P20-0, P30-0, # conditions initiale
           a-1, b-1,
           p0+2*p20+3*p30-(P0+2*P20+3*P30),
           (-2*a*p0*p0)+(2*b*p20)-(a*p0*p20)+(b*p30), 
           (a*p0*p0)-(b*p20)-(a*p0*p20)+(b*p30),
           (a*p0*p20)-(b*p30)]

    # On lance le solveur
    sols = nonlinsolve(sys, [p0, p20, p30, P0, P20, P30, a, b])
    y.append(list(sols)[0][2])

if __name__ == "__main__":
    print("Exercice 1 :")
    print("Q1)")
    print("coeff p, p1, p2 =", res_q1[0].transpose(), "\n")
    ########################################
    print("Q4)")
    print("Voir 'graph_ex1_q4.png'\n")
    fig, ax = plt.subplots(2, 2, figsize=(10,7), sharex=True)
    fig.suptitle("Simulation de "+r"$P+P \overset{a}{\underset{b}{\rightleftharpoons}} P_2, P+P_2 \overset{a}{\underset{b}{\rightleftharpoons}} P_3$")
    for i in range(4):
        exec(f"Xvals = Xvals{i+1}")
        exec(f"K = K{i+1}")
        ax[i%2,i//2].plot(tvals, Xvals, label=["P","P2","P3"])
        ax[i%2,i//2].set_xlabel("t")
        ax[i%2,i//2].set_ylabel("Concentration")
        ax[i%2,i//2].grid()
        ax[i%2,i//2].legend(loc='right')
        ax[i%2,i//2].set_title(f"(a,b) = {K}")
    plt.savefig("graph_ex1_q4.png")
    plt.show()
    ########################################
    print("Q6)")
    print("Voir 'graph_ex1_q6.png'")
    plt.figure(figsize=(10,5))
    plt.plot(T, y)
    plt.grid(True, which="both", linestyle='--')
    plt.xlabel("T")
    plt.xscale("log")
    plt.ylabel("$p_{3,0}$")
    plt.title("$p_{3,0}$ en fonction de $T=P(0)+2P_2(0)+3P_3(0)$")
    plt.savefig("graph_ex1_q6.png")
