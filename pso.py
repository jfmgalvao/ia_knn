#importar modulos
import numpy as np
import matplotlib.pyplot as plt

#implementar funções necessarias 

##função fitness
def fitfunc(x_vals):
  return np.sum(x_vals**2)

##inicializar posição enxame
def init_position(Np, Nd, x_min, x_max):
  return x_min + np.random.rand(Np, Nd)*(x_max - x_min)

##atualizar posições
def update_position(R, V, Np, Nd, x_min, x_max):
  R += V
  
  for particle in range(Np):
    for dimension in range(Nd):
      if R[particle][dimension] > x_max:
        R[particle][dimension] = x_max
      if R[particle][dimension] < x_min:
        R[particle][dimension] = x_min

  return R

##inicializar velocidade
def init_velocity(Np, Nd, v_min, v_max):
  return v_min + np.random.rand(Np, Nd)*(v_max - v_min)

##atualizar velocidades
def update_velocity(R, V, Np, Nd, w, c1, c2, v_min, v_max, chi, p_best_pos, g_best_pos):
  r1 = np.random.rand()
  r2 = np.random.rand()

  for particle in range(Np):
    V[particle, :] = chi*(w*V[particle, :] + c1*r1*(p_best_pos[particle, :] - R[particle, :]) + c2*r2*(g_best_pos - R[particle, :]))

    for dimension in range(Nd):
      if V[particle][dimension] > v_max:
        V[particle][dimension] = v_max
      if V[particle][dimension] < v_min:
        V[particle][dimension] = v_min

    return V

##atualizar fitness
def update_fitness(R, Np, g_best_value, g_best_pos, p_best_value, p_best_pos):
  for particle in range(Np):
    M = fitfunc(R[particle, :])
    
    if M < g_best_value:
      g_best_value = M
      g_best_pos = R[particle, :]

    if M < p_best_value[particle]:
      p_best_value[particle] = M
      p_best_pos[particle, :] = R[particle, :]

  return g_best_value, g_best_pos, p_best_value, p_best_pos

##PSO
Np, Nd, Nt = 10, 200, 100
c1, c2 = 2.05, 2.05
w_min, w_max = 0.4, 0.9
x_min, x_max = -10, 10
v_min, v_max = 0.25*x_min, 0.25*x_max

g_best_value = float('inf')
p_best_value = [float('inf')] * Np

g_best_pos = np.zeros(Nd)
p_best_pos = np.zeros((Np, Nd))

phi = c1 + c2
chi = 2/np.abs(2 - phi - np.sqrt(phi**2 - 4*phi))

R = init_position(Np, Nd, x_min, x_max)
V = init_velocity(Np, Nd, v_min, v_max)

history = []

for j in range(Nt):
  g_best_value, g_best_pos, p_best_value, p_best_pos = update_fitness(R, Np, g_best_value, g_best_pos, p_best_value, p_best_pos)
  
  history.append(g_best_value)
 
  w = w_max - (w_max - w_min)*j/Nt
  V = update_velocity(R, V, Np, Nd, w, c1, c2, v_min, v_max, chi, p_best_pos, g_best_pos)
  R = update_position(R, V, Np, Nd, x_min, x_max)

plt.plot(history)
print('g_best_value: ', g_best_value)
print('g_best_pos: ', g_best_pos)
