import pygame, random, time
pygame.init()
pygame.font.init()
pygame.mixer.init()

#Window setup
screen = pygame.display.set_mode([800, 700])
background = pygame.image.load("pictures/taust800x600.png")
pygame.display.set_caption("Rallimäng")

#UI elements

UIfont = pygame.font.SysFont(None, 30)
UIfontBigger = pygame.font.SysFont(None, 50)
UIfontSmaller = pygame.font.SysFont(None, 25)

backgroundUI = pygame.image.load("pictures/UI_background.jpg")
backgroundUI = pygame.transform.scale(backgroundUI, (800, 100))

distanceText = UIfont.render("Distance:", True, (0, 0, 0))

score = 0
scoreText = UIfontBigger.render(str(score), True, (0,0,0))
fuelText = UIfontSmaller.render("Fuel:", True, (155, 155, 155))

boostText = UIfontSmaller.render("Boost:", True, (155, 155, 155))
overtakeText = UIfontSmaller.render("Overtakes:", True, (155,155,155))

timeText = UIfontSmaller.render("Time:", True, (155, 155, 155))

#Game assets
carPic = pygame.image.load("pictures/auto2.png")
carPic = pygame.transform.scale(carPic, (150, 75))

gasPic = pygame.image.load("pictures/gascan.png")
gasPic = pygame.transform.scale(gasPic, (70, 70))

badCarPic = pygame.image.load("pictures/badcar.png")
badCarPic = pygame.transform.scale(badCarPic, (150, 75))

clock = pygame.time.Clock()

#sound
startupSound = pygame.mixer.Sound("audio/startup.mp3")
drivingSound = pygame.mixer.Sound("audio/driving.mp3")
crashSound = pygame.mixer.Sound("audio/crash.wav")
collectSound = pygame.mixer.Sound("audio/collect.wav")
pygame.mixer.Sound.set_volume(crashSound, 0.25)



#Starting variables

carPosY = 320
gasPosX = 800
step = 70

#Player class
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = carPic
        self.rect = self.image.get_rect()
        
        self.x = 20
        self.y = carPosY
        self.rect.x = 20
        self.rect.y = carPosY
        self.mask = pygame.mask.from_surface(self.image)
        
    def drawCar(self, surface):
        surface.blit(self.image, [self.x, self.y])

    def moveCar(self, DownOrUp):

        if DownOrUp == pygame.K_UP:
            if self.y > 350:
                self.y -= step
                self.rect.y -= step
            
       
        if DownOrUp == pygame.K_DOWN:
            if self.y < 400:
                self.y += step
                self.rect.y += step
    def boostCar(self, outOfBoost, boost):      
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_SPACE] and not outOfBoost and boost > 0:
            self.x += 3
            self.rect.x += 3
            boost -= 3
            boostMultip = 2
            if boost <= 0:
                boost = 0
                            
        if boost <= 0:
            outOfBoost = True
        if not keyPressed[pygame.K_SPACE] and boost >= 0 and boost <= 100:
            outOfBoost = True
            boost += 0.25
            boostMultip = 1
        if outOfBoost:
            self.x -= 1
            self.rect.x -= 1
            boostMultip = 1
            
            
        if self.x <= 20:
            outOfBoost = False
            self.x = 20
            self.rect.x = self.x
            boostMultip = 1
        
            
        return outOfBoost, boost, boostMultip

#Gas can class
class Gas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = gasPic
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def drawGas(self, surface, Xcoord, Ycoord):
        
        self.x = Xcoord
        self.y = Ycoord
        self.rect.x = Xcoord
        self.rect.y = Ycoord
       
        surface.blit(self.image, [self.x, self.y])
       
    def isCollision(self, gas, car):      
        if pygame.sprite.collide_mask(gas, car):
            #global collectSound
            pygame.mixer.Sound.play(collectSound)
            #print("collision")
            return True
        else:
            return False
            
    def YcoordRoll(self):
        randInt = random.randint(1,3)
        
        if randInt == 1:
            Ycoord = 320
        elif randInt == 2:
            Ycoord = 400
        else:
            Ycoord = 470
        return Ycoord
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = badCarPic
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def drawObstacle(self, surface, Xcoord, Ycoord):
        self.x = Xcoord
        self.y = Ycoord
        self.rect.x = Xcoord
        self.rect.y = Ycoord
        
        surface.blit(self.image, [self.x, self.y])
        
    def isCollision(self, obstacle, car):      
        if pygame.sprite.collide_mask(obstacle, car):
            return True
        else:
            return False
    def YcoordRoll(self):
        randInt = random.randint(1,3)
        
        if randInt == 1:
            Ycoord = 320
        elif randInt == 2:
            Ycoord = 390
        else:
            Ycoord = 470
        return Ycoord
#UI elements
def UI(score, fuel, boost, red, green, overtakes):

    
    #UI background
    pygame.draw.rect(screen, [0, 0, 0], [0, 598, 800, 5])         #game and UI border
    screen.blit(backgroundUI,(0, 600))
    
    #distance/score
    
    scoreText = UIfontBigger.render(str(int(score)) , True, (0,0,0))
    screen.blit(distanceText, (430, 610))
    
    screen.blit(scoreText, (430, 640))                            #distance driven
    #fuel
    screen.blit(fuelText, (55, 624))
    pygame.draw.rect(screen, [255,255,255], [55, 640, 150, 30])   #fuel indicator background
    pygame.draw.rect(screen, [red, green, 0], [58, 643, fuel[0], 24]) #fuel indicator
    
    #boost
    pygame.draw.rect(screen, [255,255,255], [230, 640, 150, 30]) # boost indicator background
    pygame.draw.rect(screen, [96, 142, 247], [233, 643, 144*(int(boost)/100), 24])
    screen.blit(boostText, (230, 624))
    
    #overtakes
    screen.blit(overtakeText, (585, 624))
    overtakesText = UIfontBigger.render(str(int(overtakes)), True, (155,155,155))
    screen.blit(overtakesText, (640, 640))
    
def backgroundDraw(backgroundX):
    global background
    screen.blit(background, (backgroundX, 0))
    screen.blit(background, (800+backgroundX, 0))
    
    return backgroundX

def startMenu():
    pygame.mixer.music.load("audio/menumusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)
    
    car = Car()
    startRunning = True
    mainRunning = False
    gameNameFont = pygame.font.SysFont(None,100)
    startFont = pygame.font.SysFont(None, 50)
    backgroundX = 0
    gameName = gameNameFont.render("Climb Hill Racing", True, (0,0,0))
    startText = startFont.render("Play", True, (255, 255, 255))
    
    exitText = startFont.render("Exit", True, (255, 255, 255))
    
    while startRunning:
        deltaTime = clock.tick(60)
        
        screen.blit(background, (0,0))
        pygame.draw.rect(screen, [0, 0, 0], [0, 598, 800, 5])         #game and UI border
        screen.blit(backgroundUI,(0, 600))
        #pygame.draw.rect(screen, [255,255,255], [0,0, 800, 597])
        backgroundDraw(backgroundX)
        backgroundX -= 0.2 * deltaTime
        
        if backgroundX < -800:
            screen.blit(background, (800+backgroundX, 0))
            backgroundX = 0
        
        car.drawCar(screen)
        pygame.draw.rect(screen, [0, 0, 0], [300, 200, 200, 100])    #start menu buttons 
        pygame.draw.rect(screen, [0, 0, 0], [300, 310, 200, 100])
        
        
        pygame.draw.rect(screen,[110, 110, 110], [305, 205, 190, 90])
        pygame.draw.rect(screen,[110, 110, 110], [305, 315, 190, 90])
        
   
        screen.blit(startText, (360, 240))
        screen.blit(exitText, (360, 345))
        
        screen.blit(gameName, (150, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startRunning = False
            if event.type == pygame.KEYDOWN:
                eventKey = event.key
                if eventKey == pygame.K_SPACE:
                    startRunning = False
                    pygame.mixer.music.stop()
                    
                    time.sleep(0.2)
                    mainRunning = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if mouseX in range (300, 500) and mouseY in range(200,300):
                    startRunning = False
                    pygame.mixer.Sound.play(startupSound)
                    time.sleep(.5)
                    
                    mainRunning = True
                if mouseX in range (300, 500) and mouseY in range(310, 410):
                    startRunning = False
                
                    
        pygame.display.flip()
    return mainRunning

#Main loop
def main(running):
    pygame.mixer.music.load("audio/drivingmusic.mp3")
    pygame.mixer.music.play(-1)
    score = 0
    car = Car()
    gas = Gas()
    obstacle = Obstacle()

    Ycoord = gas.YcoordRoll()
    Xcoord = random.randint(1000, 1200)

    YcoordObstacle = obstacle.YcoordRoll()
    XcoordObstacle = random.randint(1000,1200)
 
    backgroundX = 0
    overtakes = 0

    fuel = [float(144), 255, 255, 255]
    difficultyMultip = 1
    redFuel = 0
    greenFuel = 255
    boost = [None, 100]
    pygame.mixer.Sound.stop(startupSound)
    pygame.mixer.Sound.set_volume(drivingSound, 0.25)
    pygame.mixer.Sound.play(drivingSound, -1)
    while running:
        
        
        #spacePressed = False
        deltaTime = clock.tick(60)
        backgroundDraw(backgroundX)
        backgroundX -= 0.2 * deltaTime
        gas.isCollision(gas, car)
        obstacle.isCollision(obstacle, car)
     
        
        if Xcoord < random.randint(-600, -400):
            Xcoord = random.randint(900, 1200)
            Ycoord = gas.YcoordRoll()
            
        if XcoordObstacle < random.randint(-600, -400):
            XcoordObstacle = random.randint(1000, 1200)
            YcoordObstacle = obstacle.YcoordRoll()
            overtakes += 1
            if overtakes >= 99:
                overtakes = 99
            
        if gas.isCollision(gas, car):
            Xcoord = random.randint(1000, 1200)
            Ycoord = gas.YcoordRoll()
            redFuel = 0
            greenFuel = 255
            fuel[0] = 144
            
        if obstacle.isCollision(obstacle, car):
            gameOver("You crashed!", score)
            running = False
            
        gas.drawGas(screen, Xcoord, Ycoord)
        car.drawCar(screen)
        obstacle.drawObstacle(screen, XcoordObstacle, YcoordObstacle)
        
        boost = car.boostCar(boost[0], boost[1])   
        
        if backgroundX < -800:
            screen.blit(background, (800+backgroundX, 0))
            backgroundX = 0
            
            
        
        Xcoord -= 0.2 * deltaTime
        XcoordObstacle -= 0.1 * deltaTime
        if score >= 9999:
            score == 9999
        score += 1 * boost[2]
        fuel[0] = float(fuel[0]) - 0.2 * difficultyMultip
        
        if fuel[0] <= 0:
            gameOver("You ran out of fuel!", score)
            running = False
        #difficultyMultip += 0.001
        if redFuel < 255:
            if redFuel < 255:
                redFuel += 0.01 * fuel[0]
        else:
            if greenFuel > 0:
                greenFuel -= 0.01 * fuel[0]
        UI(score, fuel, boost[1], redFuel, greenFuel, overtakes)
       
        #print(spacePressed)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                eventKey = event.key
                if eventKey == pygame.K_UP or event.key == pygame.K_DOWN:
                    DownOrUp = eventKey
                    car.moveCar(DownOrUp)

def gameOver(message, score):
    pygame.mixer.music.load("audio/gameover.mp3")
    pygame.mixer.music.play(-1)
    gameOverRunning = True
    while gameOverRunning:
        pygame.mixer.Sound.stop(drivingSound)
        startFont = pygame.font.SysFont(None, 50)
        screen.blit(background,(0, 600))
        screen.blit(backgroundUI,(0, 600))
        
        pygame.draw.rect(screen, [0, 0, 0], [300, 200, 200, 100])    #start menu buttons 
        pygame.draw.rect(screen, [0, 0, 0], [300, 310, 200, 100])
        
        pygame.draw.rect(screen,[110, 110, 110], [305, 205, 190, 90])
        pygame.draw.rect(screen,[110, 110, 110], [305, 315, 190, 90])
        pygame.draw.rect(screen, [0, 0, 0], [0, 598, 800, 5])

            
        messageText = startFont.render(message, True, (0, 0, 0))
        scoreText = startFont.render("Your score: "+ str(score), True, (0,0,0))
        
        tryAgainText = startFont.render("Try Again", True, (255, 255, 255))
        exitText = startFont.render("Exit", True, (255,255,255))
        if message == "You ran out of fuel!":
            messageCoord = 260
        else:
            messageCoord = 295
        screen.blit(messageText, (messageCoord, 50))
        screen.blit(scoreText, (280, 120))
        screen.blit(tryAgainText, (325, 240))
        screen.blit(exitText, (360, 345))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOverRunning = False
            if event.type == pygame.KEYDOWN:
                eventKey = event.key
                if eventKey == pygame.K_SPACE:
                    gameOverRunning = False
                    time.sleep(0.2)
                    mainRunning = True
                    main(mainRunning)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if mouseX in range (300, 500) and mouseY in range(200,300):
                    time.sleep(0.2)
                    mainRunning = True
                    main(mainRunning)
                if mouseX in range (300, 500) and mouseY in range(310, 410):
                    gameOverRunning = False
                    pygame.display.flip()
                    
                    

running = startMenu() 
main(running)
                        
pygame.quit()