#Importing pygame and randint
from pygame import *
from random import randint

#Activating music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound=mixer.Sound('fire.ogg')

#Activating fonts
font.init()
font1 = font.SysFont(None,80)
win=font1.render('YOU WIN!',True,(255,255,255))
lose=font1.render('YOU LOSE!',True,(180,0,0))
font2 = font.SysFont(None,36)

#Importing images
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet ='bullet.png'
img_ast = 'asteroid.png'

#Creating main counters
score=0
goal=100
lost=0
max_lost=3

#Creating main class 
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
       
   #bliting images
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#Creating Player class with GameSprite
class Player(GameSprite):
    #Movement
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #Fire ability
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#Creating Enemy class with GameSprite
class Enemy(GameSprite):
    #Movement
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x =randint(80,win_width - 80)
            self.rect.y = 0
            lost=lost + 1

#Creating Asteroid class with GameSprite
class Asteroid(GameSprite):
    #Movement
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x =randint(80,win_width - 80)
            self.rect.y = 0


#Creating Bullet class with GameSprite
class Bullet(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y < 0:
            self.kill()

#Creating window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Creating player with Player class
ship = Player('rocket.png', 5, win_height - 80,50,50, 20)

#Spawning enemies with Enemy class
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80,win_width - 80),-40,80,50,randint(1,5))
    monsters.add(monster)

#Spawning asteroids with Enemy class
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets=sprite.Group()

finish=False

run=True

#Main cycle
while run:
    for e in event.get():
        if e.type == QUIT:
            run=False
        
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    if not finish:
        window.blit(background,(0,0))
        #Activating fonts
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        #Updating 
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        #Collisions
        collides =sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score=score+1
            monster=Enemy(img_enemy,randint(80,win_width - 80),-40,80,50,randint(1,5))
            monsters.add(monster)
        #Death
        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish=True
            window.blit(lose,(200,200))
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) :
           sprite.spritecollide(ship, monsters, True)
           sprite.spritecollide(ship, asteroids, True)
           window.blit(lose,(200,200))
           finish = True
        #Win
        if score >= goal:
            finish=True
            window.blit(win,(200,200))
        
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()
    
    else:
        finish=False
        score=0
        lost=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()  
        
        time.delay(3000)
        for i in range(1,6):
            monster=Enemy(img_enemy,randint(80,win_width - 80),-40,80,50, randint(1,6))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid) 

    time.delay(50)
