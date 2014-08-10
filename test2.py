from scipy.integrate import odeint
from numpy import arange
from math import exp
from matplotlib.pyplot import plot
from numpy import where


## definitions
# rocket properties
#m_dot = 16.97      # constant fuel+air mass flow rate [kg/s]
#V_e = 2946.0      # constant rocket exhaust velocity [m/s]

m_f0 = 490.0     # initial fuel+ox mass [kg]
m_s = 840.0+72.5+500       # structural mass [kg]

I_sp_sea = 300 # specific impulse at sea level [s]
I_sp_vac = 390 # specific impulse at vacuum [s]
Thrust = 50e3 # (initial?) thrust [N]


# planet properties
G = 6.67e-11      # grav_accitational constant [m^3/kg/s^2]
M = 5.29e22       # mass of Kerbin [kg]
H = 5000.0        # scale height of planet [m]
R = 600000.0      # radius of planet [m]

t_0 = 0 # start time [s]
t_f = 60 # end time [s]
N = 500 # number of time points


## acceleration function
def func(y0, t):

  # unpack the state vector
  x = y0[0] # distance (altitude)
  xd = y0[1] # velocity (radial)
  m_f = y0[2] # current amount of fuel left
  
  # if no fuel left, no thrust!
  T = Thrust
  if(m_f < 0):
    m_f = 0
    T = 0

  # atmospheric conditions
  pressure = 1*exp(-x/H) # atmospheric pressure [atm] NOT PASCAL!?
  density = 1.2230948554874*pressure # atmospheric density [kg/m^3]
  
  # calculate current specific impulse
  I_sp = I_sp_vac - pressure*(I_sp_vac - I_sp_sea)

  
  # calculate the mass flow rate
  m_dot = T/I_sp/9.82 # current mass flow rate [kg/s]

  # engine thrust
  accel_thrust = T/(m_s + m_f)

    
  # drag force (!)
  area = 0.008*(m_s + m_f) # area (func of total mass according to KSP) [m^2]
  cd = .2 # should be mass-averaged
  F_d = 0.5*density*pow(xd, 2)*cd*area
  accel_drag = F_d/(m_s + m_f) # is this okay???
  
  # acceleration due to gravity
  accel_grav = G*M/pow(R+x+74, 2) # accel due to gravity based on dist from Kerbin surface (if going straight out)
  
  xdd = -accel_grav + accel_thrust - accel_drag # acceleration

  return [xd, xdd, -m_dot]


## run the calculations
y0 = [0.0, 0.0, m_f0] # initial dist, init vel, init fuel
times = arange(t_0, t_f, (t_f-t_0)/N)
ans = odeint(func, y0, times)



max_alt = max(ans[:,0])
max_vel = max(ans[:,1])

max_alt_t = times[where(ans[:,0] == max_alt)[0][0]]
max_vel_t = times[where(ans[:,1] == max_vel)[0][0]] # not great way but it works


print("Max altitude: ", max_alt, "@", max_alt_t)
print("Max velocity: ", max_vel, "@", max_vel_t)

plot(times,ans)