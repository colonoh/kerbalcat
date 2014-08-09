from scipy.integrate import odeint
from numpy import arange
from math import exp
import matplotlib.pyplot as plt

m_f, area, pressure, density = list(), list(), list(), list()
F_d, grav_acc, thrust_acc = list(), list(), list()
fuel_used = list()

# rocket properties
m_dot = 10      # constant fuel+air mass flow rate [kg/s]
V_e = 1500      # constant rocket exhaust velocity [m/s]
m_f0 = 1000     # initial fuel+ox [kg]
m_s = 100 # structural mass [kg]

# constants
G = 6.67e-11    # grav_accitational constant [m^3/kg/s^2]

# planet properties
M = 5.29e22     # mass of Kerbin [kg]
H = 5000        # scale height of planet [m]
R = 600000      # radius of planet [m]

def acceleration(y0,t):
  # unpack the state vector
  x = y0[0] # distance / altitude 
  xd = y0[1] # velocity (outwards)
  
  # current mass of the fuel+ox [kg]
  m_f.append(m_f0 - m_dot*t) 
  area.append(0.008*(m_s+m_f[-1])) # area (func of total mass according to KSP) [m^2]
  pressure.append(1*exp(-x/H)) # atmospheric pressure [atm] NOT PASCAL!?
  density.append(1.2230948554874*pressure[-1]) # atmospheric density [kg/m^3]

  grav_acc.append(G*M/pow(R+x,2)) # accel due to grav_accity based on dist from Kerbin surface (if going straight out) [m/s^2]
  
  c_d = 0.2
  
  # drag
  F_d.append(0.5*density[-1]*pow(xd, 2)*c_d*area[-1])

  # compute engine acceleration
  # thrust only contributes while mass of fuel is greater than zero
  if m_f[-1] > 0:
    thrust_acc.append((m_dot*V_e)/(m_s + m_f[-1]))
  else:
    thrust_acc.append(0)

  xdd = thrust_acc[-1] - grav_acc[-1]# - F_d[-1]
  return [xd, xdd]

y0 = [00.0, 0.0]
t = arange(0.0, 200., 0.1)

ans = odeint(acceleration, y0, t)

plt.plot(t, ans)