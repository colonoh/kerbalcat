from scipy.integrate import odeint
from numpy import arange, where
from math import exp, copysign
from matplotlib.pyplot import plot, xlabel, ylabel, legend
from Component import Component

import Stage
import Rocket

## definitions

Stage1 = Stage.Stage()
Stage1.addComp(Component(1.5,.2, 950, thrust = 200, I_sp_sea = 320, I_sp_vac = 370)) #LV-T45 Liquid Fuel Engine
Stage1.addComp(Component(4.5, .2, 1600, m_fuel = 1.8, m_ox = 2.2)) #FL-T800 Fuel Tank
Stage1.addComp(Component(.84, .2, 600)) #Command Pod Mk1

Rocket = Rocket.Rocket()
Rocket.addStage(Stage1)


# rocket properties
m_f0 = 4000     # initial fuel+ox mass [kg]

# planet properties
G = 6.67e-11      # grav_accitational constant [m^3/kg/s^2]
M = 5.29e22       # mass of Kerbin [kg]
H = 5000.0        # scale height of planet [m]
R_planet = 600000.0      # radius of planet [m]

t_0 = 0.0 # start time [s]
t_f = 230 # end time [s]
N = 100 # number of time points


## acceleration function
def func(y0, t):

  # unpack the state vector
  x = y0[0] # distance (altitude)
  xd = y0[1] # velocity (radial)
  #m_f = y0[2] # current amount of fuel left
  
  #Rocket.stages[0].fuel = m_f
  Rocket.stages[0].setCurrentFuelOx(y0[2])

  # atmospheric conditions
  pressure = 1*exp(-x/H) # atmospheric pressure [atm]
  density = 1.2230948554874*pressure # atmospheric density [kg/m^3]
  

  # engine thrust
  accel_thrust = Rocket.stages[0].getCurrentThrust() / Rocket.getTotalMass()
    
  # drag force (!)
  F_d = 0.5*density*pow(xd, 2) * Rocket.getCd() * Rocket.getArea()
  accel_drag = copysign(F_d/Rocket.getTotalMass(), -xd)
  
  # acceleration due to gravity
  accel_grav = G*M/pow(R_planet + x + 74, 2) # accel due to gravity based on dist from Kerbin surface (if going straight out)
  
  xdd = -accel_grav + accel_thrust + accel_drag 
  
  return [xd, xdd, -Rocket.stages[0].getMassFlowRate(pressure)] # velocity, acceleration, mass flow rate (m_dot)


## run the calculations
y0 = [0.0, 0.0, m_f0] # initial dist, init vel, init fuel
times = arange(t_0, t_f, (t_f-t_0)/N) # array of time points
ans = odeint(func, y0, times)

max_alt = max(ans[:,0])
max_vel = max(ans[:,1])

max_alt_t = times[where(ans[:,0] == max_alt)[0][0]]
max_vel_t = times[where(ans[:,1] == max_vel)[0][0]] # not great way but it works


print("Max altitude: ", max_alt, "@", max_alt_t)
print("Max velocity: ", max_vel, "@", max_vel_t)

plot(times,ans)
xlabel("Time [s]")
legend(('Distance', 'Velocity', 'Remaining fuel mass'), loc=7)