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
    self.taskMgr.add(self.skySphereTask, "SkySphere")
    
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
    self.heading          = 0
    self.pitch            = 0
    self.rotation         = 0
    
  def moveShip(self, task):
    dt = globalClock.getDt()
    
    if self.keyMap['yaw_right']:
      heading = self.ship.getH(self.ship)
      self.ship.setH(self.ship, heading + self.turnRate)
    if self.keyMap['yaw_left']:
      heading = self.ship.getH(self.ship)
      self.ship.setH(self.ship, heading - self.turnRate)
    if self.keyMap['up']:
      pitch = self.ship.getP(self.ship)
      self.ship.setP(self.ship, pitch - self.turnRate)
    if self.keyMap['down']:
      pitch = self.ship.getP(self.ship)
      self.ship.setP(self.ship, pitch + self.turnRate)
    if self.keyMap['roll_left']:
      rotation = self.ship.getR(self.ship)
      self.ship.setR(self.ship, rotation + self.turnRate)
    if self.keyMap['roll_right']:
      rotation = self.ship.getR(self.ship)
      self.ship.setR(self.ship, rotation - self.turnRate)
      
    if self.keyMap['forward'] and self.impulseEngine <= self.maxSpeed:
      self.impulseEngine += 1
    if self.keyMap['backward'] and self.impulseEngine >= self.minSpeed:
      self.impulseEngine -= 1
      
    self.camera.setPos(self.ship, 0, -20, -10)
    self.camera.setR(self.ship, self.ship.getR())
    self.camera.lookAt(self.ship)
    
    self.ship.setY(self.ship, (self.impulseEngine * -1) * dt)
    
    return task.cont
  
  def setKey(self, key, value):
    self.keyMap[key] = value
    print self.keyMap
    
  def skySphereTask(self, task):
    self.stars.setPos(self.camera, 0, 0, 0)
    return task.cont
    
app = MyApp()
app.run()
