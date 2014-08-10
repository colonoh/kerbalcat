## Rocket components
# when you create a class, use the values from the info page with in-game units [tonnes]
# component returns computational units [kg/m/s]
# unspecified optional components are set to zero

''' 
required arguments:
  mass [tonne]
  drag [-]
  cost [currency]
  
optional engine arguments:
  thrust [kN]
  specific impulse at sea level [-]
  specific impulse at vacuum [-]
  
optional fuel tank arguments:
  mass of fuel [tonne]
  mass of oxygen [tonne]

'''
class Component:
  def __init__(self, mass, drag, cost, thrust = 0, I_sp_sea = 0, I_sp_vac = 0, m_fuel = 0, m_ox = 0):
    self.m_fuel = m_fuel*1000 # mass of fuel [kg]
    self.m_ox = m_ox*1000 # mass of oxygen [kg]
    self.struct_mass = mass*1000 - self.m_fuel - self.m_ox # STRUCTURAL mass [kg]
    self.drag = drag # drag [-]
    self.thrust = thrust*1000 # thrust [N]
    self.I_sp_sea = I_sp_sea # specific impulse at sea level [-]
    self.I_sp_vac = I_sp_vac # specific impulse at vacuum [-]
    self.cost = cost + self.m_fuel*.16 + self.m_ox*.04 # listed cost including fuel/ox