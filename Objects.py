import pygame

class Object():

	instances = []

	def __init__(self,x,y,size_x,size_y):
		self.x = x
		self.y = y
		self.size_x = size_x
		self.size_y = size_y

		self.x_vel = 0
		self.y_vel = 0
		"""
		self.corner0 = (self.x,self.y) #top left
		self.corner1 = (self.x+self.size_x,self.y) #top right
		self.corner2 = (self.x+self.size_x,self.y+self.size_y) #bottom right
		self.corner3 = (self.x,self.y+self.size_y) #bottom left
		"""


		self.__class__.instances.append(self)

	def move(self):

		

		if isinstance(self,floatingEnemy):
			self.x +=  self.x_vel
			self.y +=  self.y_vel
			
			if self.x < self.start[0] or self.x > self.goal[0] or self.y < self.start[1] or self.y > self.goal[1]:
				self.x -=  self.x_vel
				self.y -=  self.y_vel

				self.x_vel *= -1
				self.y_vel *= -1
			
			self.hitbox_x = self.x + self.hitbox_x_offset
			self.hitbox_y = self.y + self.hitbox_y_offset





		elif isinstance(self,Character):
			

			self.x += self.x_vel

			#if not player.inAir and not 

			self.y += self.y_vel



			if not self.inAir: 
				standing_on_something = False
				for obj in Object.instances:
					if not self.isLeftOf(obj) and not self.isRightFrom(obj) and obj.y - (self.y + self.size_y) == 1:
						standing_on_something = True
				if standing_on_something:
					self.y -= self.y_vel
				else:
					self.inAir = True

			


			else:
				self.y_vel += 0.3
				if self.collideWithAnything():
					for obj in Object.instances:
						if self.collide(obj) and not self == obj:
							self.y = obj.y - self.size_y
							self.y -= 1

					self.y_vel = 0
					self.inAir = False

				if self.direction == "left":
					self.mode = "walking_left"
				elif self.direction == "right":
					self.mode = "walking_right"

				else:
					 #gravity
					self.inAir = True






			if self.inAir:
				self.mode = "falling"

			if not self.inAir and self.x_vel == 0 and self.y_vel == 0:
				self.mode = "idle"



			self.hitbox_x = self.x + self.hitbox_x_offset
			self.hitbox_y = self.y + self.hitbox_y_offset




	def isLeftOf(self,obj):
		return self.hitbox_x + self.hitbox_size_x < obj.x

	def isAboveOf(self,obj):
		return self.hitbox_y + self.hitbox_size_y < obj.y

	def isRightFrom(self,obj):
		return self.hitbox_x > obj.x + obj.size_x

	def isBelow(self,obj):
		return self.hitbox_y > obj.y + obj.size_y

	def collide(self,obj):
		return not self.isLeftOf(obj) and not self.isAboveOf(obj) and not self.isRightFrom(obj) and not self.isBelow(obj)

	def collideWithAnything(self):
		for obj in Object.instances:
			if self.collide(obj) and not self == obj:
				return True
		return False

	def overlap_from_above(self,obj):
		return self.hitbox_y + self.hitbox_size_y - obj.y




	"""
	def isStandingOn(self,obj):
		return self.y + self.size_y in [obj.y-0,obj.y-1,obj.y-2,obj.y-3,obj.y-4,obj.y-5,obj.y-6,obj.y-7,obj.y-8,obj.y-9,obj.y-10] and not self.isLeftOf(obj) and not self.isRightFrom(obj) and not self.isBelow(obj)
	"""

	def drawHitbox(self,screen):
		pygame.draw.rect(screen,(0,255,0),[self.hitbox_x,self.hitbox_y,self.hitbox_size_x,self.hitbox_size_y],1)

	def draw(self,screen):
		
		if isinstance(self,Wall):
			pygame.draw.rect(screen,self.color,[self.x,self.y,self.size_x,self.size_y])

		elif isinstance(self,Character):
			self.drawHitbox(screen)
			self.updateSprite()

			screen.blit(pygame.transform.scale(pygame.transform.flip(self.sprite,self.direction == "left",False),(100,74)),(self.x,self.y))

			#pygame.draw.rect(screen,(255,0,0),[self.x,self.y,self.size_x,self.size_y],1) #red border






class Wall(Object):
	def __init__(self,x,y,size_x,size_y,color):
		super().__init__(x,y,size_x,size_y)
		self.color = color





class Character(Object):
	def __init__(self,x,y,size_x,size_y,hitbox_x_offset,hitbox_y_offset,hitbox_size_x_offset,hitbox_size_y_offset):
		super().__init__(x,y,size_x,size_y)

		self.sprite = pygame.image.load('sprites/adventurer-idle-00.png')


		self.hitbox_x = self.x + hitbox_x_offset
		self.hitbox_y = self.y + hitbox_y_offset
		self.hitbox_size_x = self.size_x + hitbox_size_x_offset
		self.hitbox_size_y = self.size_y + hitbox_size_y_offset

		self.hitbox_x_offset = hitbox_x_offset
		self.hitbox_y_offset = hitbox_y_offset



		self.inAir = True

		self.mode = "idle"
		self.direction = "right"
		self.spriteNumber = 0

		self.spriteUpdateSpeed = 5 #lower = faster
		self.spriteUpdateCounter = 0


	def ableToUpdateSprite(self):
		if self.spriteUpdateCounter == self.spriteUpdateSpeed:
			self.spriteUpdateCounter = 0
			return True
		return False


	def updateSprite(self):
		self.spriteUpdateCounter += 1

		if isinstance(self,floatingEnemy):
			if self.ableToUpdateSprite():
				self.spriteNumber += 1

				self.spriteNumber %= 2
				self.sprite = pygame.image.load('firesprites/fireblast'+str(self.spriteNumber)+'.png')



		else:

			if self.ableToUpdateSprite():

				self.spriteNumber += 1

				if self.mode == "idle":
					self.spriteNumber %= 3
					self.sprite = pygame.image.load('sprites/adventurer-idle-0'+str(self.spriteNumber)+'.png')

				if self.mode == "falling":
					self.spriteNumber %= 2
					self.sprite = pygame.image.load('sprites/adventurer-fall-0'+str(self.spriteNumber)+'.png')

				if self.mode == "walking_right" or self.mode == "walking_left":
					self.spriteNumber %= 6
					self.sprite = pygame.image.load('sprites/adventurer-run-0'+str(self.spriteNumber)+'.png')










class floatingEnemy(Character):
	def __init__(self,x,y,size_x,size_y,hitbox_x_offset,hitbox_y_offset,hitbox_size_x_offset,hitbox_size_y_offset,target,speed_multiplier):
		super().__init__(x,y,size_x,size_y,hitbox_x_offset,hitbox_y_offset,hitbox_size_x_offset,hitbox_size_y_offset)
		self.target = target # [x,y]


		self.start = [self.x,self.y]
		self.goal = [self.x + self.target[0], self.y + self.target[1]]


		self.x_vel = self.target[0] * speed_multiplier
		self.y_vel = self.target[1] * speed_multiplier



		self.sprite = pygame.image.load('firesprites/fireblast0.png')




"""
asd = Character(13,170,140,107,"awsd")
vn = Character(-37.171,199.966,48,39,"jawsd")

print(asd.collide(vn))
"""