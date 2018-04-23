from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class MyApp(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    
    self.disableMouse()
    
    self.keyMap = {
      'yaw_left'       : 0,
      'yaw_right'      : 0,
      'up'             : 0,
      'down'           : 0,
      'roll_left'      : 0,
      'roll_right'     : 0,
      'forward'        : 0,
      'backward'       : 0
      }
    
    self.taskMgr.add(self.moveShip, "moveShipTask")
    
    self.stars = self.loader.loadModel('models/SkySphere.bam')
    self.stars.reparentTo(self.render)
    self.stars.setPos(0, 0, 0)
    
    self.ship = self.loader.loadModel('models/ship.egg')
    self.ship.reparentTo(self.render)
    self.ship.setPos(0, 0, 0)
    
    self.accept("arrow_left", self.setKey, ['roll_left', True])
    self.accept("arrow_right", self.setKey, ['roll_right', True])
    self.accept("arrow_up", self.setKey, ['up', True])
    self.accept("arrow_down", self.setKey, ['down', True])
    self.accept(",", self.setKey, ['yaw_left', True])
    self.accept(".", self.setKey, ['yaw_right', True])
    self.accept("arrow_left-up", self.setKey, ['roll_left', False])
    self.accept("arrow_right-up", self.setKey, ['roll_right', False])
    self.accept("arrow_up-up", self.setKey, ['up', False])
    self.accept("arrow_down-up", self.setKey, ['down', False])
    self.accept(",-up", self.setKey, ['yaw_left', False])
    self.accept(".-up", self.setKey, ['yaw_right', False])
    self.accept("w", self.setKey, ['forward', True])
    self.accept('w-up', self.setKey, ['forward', False])
    self.accept("s", self.setKey, ['backward', True])
    self.accept('s-up', self.setKey, ['backward', False])
    
    self.impulseEngine    = 0
    self.turnRate         = 1
#    self.maxTurnRate      = 1
    self.maxSpeed         = 350
    self.minSpeed         = -350
    
  def moveShip(self, task):
    dt = globalClock.getDt()
    
    heading  = self.ship.getH()
    pitch    = self.ship.getP()
    rotation = self.ship.getR()
    
    if self.keyMap['yaw_left']:
      heading += self.turnRate * dt
      self.ship.setH(self.ship, heading % 360)
    if self.keyMap['yaw_right']:
      heading -= self.turnRate * dt
      self.ship.setH(self.ship, heading % 360)
    if self.keyMap['up']:
      pitch -= self.turnRate * dt
      self.ship.setP(self.ship, pitch % 360)
    if self.keyMap['down']:
      pitch += self.turnRate * dt
      self.ship.setP(self.ship, pitch % 360)
    if self.keyMap['roll_left']:
      rotation += self.turnRate * dt
      self.ship.setR(self.ship, rotation % 360)
    if self.keyMap['roll_right']:
      rotation -= self.turnRate * dt
      self.ship.setR(self.ship, rotation % 360)
      
      
    if self.keyMap['forward'] and self.impulseEngine <= self.maxSpeed:
      self.impulseEngine += 1
    if self.keyMap['backward'] and self.impulseEngine >= self.minSpeed:
      self.impulseEngine -= 1
      
    self.camera.setPos(self.ship.getX(), self.ship.getY() + 20, self.ship.getZ())
    self.camera.lookAt(self.ship)
    self.stars.setPos(self.ship.getX(), self.ship.getY(), self.ship.getZ())
    
    self.ship.setY(self.ship, (self.impulseEngine * -1) * dt)
    
    return task.cont
  
  def setKey(self, key, value):
    self.keyMap[key] = value
    print self.keyMap
    
app = MyApp()
app.run()
