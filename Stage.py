class Stage:
  def __init__(self):
    self.components = list()
    self.fuelox = 0.0

  # add a component (engine/pod/fuel tank/etc) to the stage
  def addComp(self, comp):
    self.components.append(comp)
    self.fuelox += comp.m_fuel + comp.m_ox
    
  def getCurrentFuelOx(self):
    return self.fuelox

  def setCurrentFuelOx(self, amount):
    if(amount < 0):
      self.fuelox = 0.0
    else:
      self.fuelox = amount

  # get this stage's total thrust as long as there is fuel left
  def getCurrentThrust(self):
    thrust = 0.0
    
    if(self.getCurrentFuelOx() > 0.0):
      for comp in self.components:
        thrust += comp.thrust
    return thrust
    
  # current mass flow rate as a function of atmospheric pressure [kg/s]
  def getMassFlowRate(self, pressure):
    total_mass_flow_rate = 0.0
    
    # for each engine
    for comp in self.components:
      I_sp = comp.I_sp_vac - pressure * (comp.I_sp_vac - comp.I_sp_sea) # linearly interpolated between sea and vac
      
      if(I_sp != 0.0 and self.getCurrentThrust() > 0):
        total_mass_flow_rate += comp.thrust / I_sp / 9.82
      
    return total_mass_flow_rate