from scipy.integrate import odeint
from numpy import arange, where
from math import exp, copysign
from matplotlib.pyplot import plot, xlabel, ylabel, legend
from Component import Component

class Stage:
  components = list()
  def addComp(self, comp):
    self.components.append(comp)
    
  def getStructMass(self):
    struct_mass = 0
    for comp in self.components:
      struct_mass += comp.struct_mass
    return struct_mass
  
class Rocket:
  stages = list()
  def addStage(self, stage):
    self.stages.append(stage)
    
  def getStructMass(self):
    struct_mass = 0
    for stage in self.stages:
      struct_mass =+ stage.getStructMass()
    return struct_mass
  

## definitions

Stage1 = Stage()
Stage1.addComp(Component(1.5,.2, 950, thrust = 200, I_sp_sea = 320, I_sp_vac = 370)) #LV-T45 Liquid Fuel Engine
Stage1.addComp(Component(4.5, .2, 1600, m_fuel = 1.8, m_ox = 2.2)) #FL-T800 Fuel Tank
Stage1.addComp(Component(.84, .2, 600)) #Command Pod Mk1

Rocket = Rocket()
Rocket.addStage(Stage1)


# rocket properties
m_f0 = 4000     # initial fuel+ox mass [kg]



# planet properties
G = 6.67e-11      # grav_accitational constant [m^3/kg/s^2]
M = 5.29e22       # mass of Kerbin [kg]
H = 5000.0        # scale height of planet [m]
R_planet = 600000.0      # radius of planet [m]

t_0 = 0 # start time [s]
t_f = 230 # end time [s]
N = 100 # number of time points


## acceleration function
def func(y0, t):

  # unpack the state vector
  x = y0[0] # distance (altitude)
  xd = y0[1] # velocity (radial)
  m_f = y0[2] # current amount of fuel left

  # atmospheric conditions
  pressure = 1*exp(-x/H) # atmospheric pressure [atm]
  density = 1.2230948554874*pressure # atmospheric density [kg/m^3]
  

  I_sp_sea = 320 # specific impulse at sea level [s]
  I_sp_vac = 370 # specific impulse at vacuum [s]
  Thrust = 200e3 # (initial?) thrust [N]

  
  area = 0.008*(Rocket.getStructMass()+m_f) # area (func of mass) [m^2]
  cd = .2 # should be mass-averaged

  
  # if no fuel left, no thrust!
  T = Thrust
  if(m_f < 0):
    m_f = 0
    T = 0


  
  # calculate current specific impulse
  I_sp = I_sp_vac - pressure*(I_sp_vac - I_sp_sea)

  # calculate the mass flow rate
  m_dot = T/I_sp/9.82 # current mass flow rate [kg/s]

  # engine thrust
  accel_thrust = T/(Rocket.getStructMass() + m_f)
    
  # drag force (!)
  F_d = 0.5*density*pow(xd, 2)*cd*area
  accel_drag = copysign(F_d/(Rocket.getStructMass()+m_f), -xd)
  
  # acceleration due to gravity
  accel_grav = G*M/pow(R_planet + x + 74, 2) # accel due to gravity based on dist from Kerbin surface (if going straight out)
  
  xdd = -accel_grav + accel_thrust + accel_drag 
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
xlabel("Time [s]")
legend(('Distance', 'Velocity', 'Remaining fuel mass'), loc=7)