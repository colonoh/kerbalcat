from scipy.integrate import odeint
from numpy import arange
import matplotlib.pyplot as plot


m_dot = 10 # constant fuel+air mass flow rate [kg/s]
V_e = 1500 # constant rocket exhaust velocity [m/s]
m_s = 100 # structural mass [kg]
m_f0 = 1000 # initial fuel+ox

G = 6.67e-11 # universal grav const
M = 5.29e22 # mass of Kerbin


def acceleration(y0,t):
  # unpack the state vector
  x = y0[0]
  xd = y0[1]
  
  # current mass of rocket
  m_f = m_f0 - m_dot*t


  g = G*M/pow(600000+x,2) # accel due to gravity based on dist from Kerbin surface (if going straight out)

  

  # compute engine thrust
  if m_f > 0:
    thrust = (m_dot*V_e)/(m_s + m_f)
  else:
    thrust = 0


  xdd = thrust - g
  return [xd, xdd]

y0 = [00.0, 0.0]
t = arange(0.0, 1000., 0.1)

ans = odeint(acceleration, y0, t)

plot.plot(t, ans)


#check

from math import log
#vel = -V_e*(log(m_0-10*m_dot)-log(m_0))
# #print(vel)
# from math import pow
# h_bo = V_e/m_dot*(m_0)-.5*pow(m_0/m_dot,2)*9.8
# print(h_bo)
# print(ans[-1,0])
# print(h_bo/ans[-1,0])