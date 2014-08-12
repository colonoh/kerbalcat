class Rocket:
  stages = list()
  def addStage(self, stage):
    self.stages.append(stage)
    
  # get the rocket's total structural mass [kg]
  def getStructMass(self):
    struct_mass = 0.0
    for stage in self.stages:
      for comp in stage.components:
        struct_mass += comp.struct_mass
    return struct_mass
    
  # current structral and fuel/ox mass of the entire rocket
  def getTotalMass(self):
    mass = self.getStructMass()
    
    for stage in self.stages:
      mass += stage.getCurrentFuelOx()
    
    return mass
    
    
    
  # rocket's mass averaged coefficient of drag
  def getCd(self):
    top_cd = 0.0 # cd*mass
    total_mass = 0.0
    
    for stage in self.stages:
      for comp in stage.components:
        comp_mass = comp.struct_mass + comp.m_fuel + comp.m_ox # mass of this component
        
        top_cd += comp.drag * comp_mass
        total_mass += comp_mass
    
    return top_cd/total_mass    
    
  # drag area is based on mass in KSP
  def getArea(self):
    fuel_mass = 0.0
    for stage in self.stages:
      fuel_mass += stage.getCurrentFuelOx()
    
    return 0.008*(self.getStructMass() + fuel_mass) # area [m^2]