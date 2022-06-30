from Objects import *

player = Character(100,100,100,74,35,10,-70,-10)  #50:37 original size

wall1 = Wall(300,300,100,20,(0,0,0))

wall2 = Wall(100,320,100,10,(120,0,120))

floor = Wall(0,550,800,50,(128,64,64))

fireguy1 = floatingEnemy(500,200,50,50,0,0,0,0,[200,300],0.01)