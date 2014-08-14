from scipy.integrate import odeint
from numpy import arange, where
from math import exp, copysign
from matplotlib.pyplot import plot, xlabel, ylabel, legend
from Component import Component


import Stage    
import Rocket

## definitions

Rocket = Rocket.Rocket()

Stage1 = Stage.Stage()
#Stage1.addComp(Component(.05, .2, 400)) #TR-18A Stack Decoupler
Stage1.addComp(Component(.5625, .2, 250, m_fuel = .22, m_ox = .27)) #FL-T100 Fuel Tank
Stage1.addComp(Component(.5,.2, 750, thrust = 50, I_sp_sea = 300, I_sp_vac = 390)) #LV-909 Liquid Fuel Engine

Rocket.addStage(Stage1)

Stage2 = Stage.Stage()
Stage2.addComp(Component(.84, .2, 600)) #Command Pod Mk1
Rocket.addStage(Stage2)


# planet properties
G = 6.67e-11        # grav_accitational constant [m^3/kg/s^2]
M = 5.29e22         # mass of Kerbin [kg]
H = 5000.0          # scale height of planet [m]
R_planet = 600000.0 # radius of planet [m]

t_0 = 0.0 # start time [s]
t_f = 60 # end time [s]

# issue where integrator doesn't work with certain times


## acceleration function
def func(y0, t):
  global Rocket # boo global 
  
# check to see if the stage has any fuel left and there are still stages left
  #if(Rocket.stages[0].getCurrentFuelOx() <= 0.0 and len(Rocket.stages) > 1):
    #Rocket.delStage()
    #y0[2] = Rocket.stages[0].getCurrentFuelOx() 
    #t = t_f
    
  # this only changes the value here, not the actual solver value for fuelox mass >:O
  # can't figure out how to leave function either

  
  # unpack the state vector
  x = y0[0] # distance (altitude)
  xd = y0[1] # velocity (outwards)
  Rocket.stages[0].setCurrentFuelOx(y0[2]) # the stage's current amount of stage fuel [kg]

  # atmospheric conditions
  pressure = 1.0 * exp(-x / H) # atmospheric pressure [atm] (the 1.0 is pressure at sea level)
  density = 1.2230948554874 * pressure # atmospheric density [kg/m^3]
  
  accel_thrust = Rocket.stages[0].getCurrentThrust() / Rocket.getTotalMass() # engine thrust
  
  accel_grav = G * M / pow(R_planet + x, 2) # accel due to gravity based on dist from Kerbin surface (if going straight out)

  # drag force (!)
  F_d = 0.5 * density * pow(xd, 2) * Rocket.getCd() * Rocket.getArea()
  accel_drag = copysign(F_d / Rocket.getTotalMass(), -xd) # drag should always be opposite of velocity
  
  xdd = -accel_grav + accel_thrust + accel_drag # total acceleration
  
  return [xd, xdd, -Rocket.stages[0].getMassFlowRate(pressure)-.000001 ] # velocity, acceleration, mass flow rate (m_dot)


## run the calculations
y0 = [0.0, 0.0, Rocket.stages[0].getCurrentFuelOx()] # initial alt, init vel, init fuelox mass
times = arange(t_0, t_f, .01) # array of time points

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