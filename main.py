from cmu_graphics import *
import math
import random
from PIL import Image


class Bee:

    def __init__(self, x, y, flowers, isPlayer=False):
        self.x = x
        self.y = y
        self.size = 15
        self.flowerSize = 10
        self.speed = 3 if isPlayer else 2
        self.pollenInventory = []
        self.originalFlower = []
        self.flowers = flowers
        self.target = None
        self.isPlayer = isPlayer
        self.pollenSize = 10


    def drawBee(self, image):
        # drawCircle(self.x, self.y, self.playerSize, fill='yellow')
        drawImage(image, self.x, self.y, width=50, height=50, align='center')


    def pollinate(self, flowers):
        # Loop through all flowers
        for flower in flowers:
            distance = ((flower.x - self.x) ** 2 + (flower.y - self.y) ** 2) ** 0.5

            if distance <= (self.size + self.flowerSize):
                # Check if the flower is a pollinator and not yet gathered
                if flower.isPollinator and not flower.gathered and len(self.pollenInventory) < 6:
                    flower.gathered = True
                    self.pollenInventory.append([flower.color, self.pollenSize])
                    self.originalFlower.append([flower.color,flower])

                # Check if the flower can be pollinated
                elif not flower.isPollinator and not flower.gathered and not flower.isPollinated: 
                    for sublist in self.pollenInventory:
                        if sublist[0] == flower.color: 
                            flower.isPollinated = True
                            flower.grow()
                            self.growPollen(flower.color)
                            # Grow the original flower
                            for originalFlower in self.originalFlower:
                                if originalFlower[0] == flower.color:
                                    originalFlower[1].grow()
                            break
                         
                        
    def chooseTarget(self, otherBee):
        # If the bee has a target, check if it can still be a target
        if self.target and (self.target.gathered or self.target.isPollinator
            or self.target.x < 0 or self.target.x > 400 or self.target.y < 0 or self.target.y > 400):
                self.target = None

        if self.target == None: 
            # Find a new target flower
            minDistance = 1000
            for flower in self.flowers:
                if not flower.gathered or not flower.isPollinator:
                    distance = ((flower.x - self.x) ** 2 + (flower.y - self.y) ** 2) ** 0.5

                    # Check if the flower is close to the other bee
                    otherBeeDistance = ((flower.x - otherBee.x) ** 2 + (flower.y - otherBee.y) ** 2) ** 0.5
                    if otherBeeDistance < 2 * self.size:
                        continue  # Skip this flower if it's close to the other bee
                    
                    if distance < minDistance:
                        minDistance = distance
                        self.target = flower


    def helperBeeOnStep(self, otherBee=None):
        # Choose a target flower 
        self.chooseTarget(otherBee)

       # Move the bee toward the target 
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance > 0:
                dx /= distance
                dy /= distance

           # Move the bee within canvas 
            new_x = self.x + self.speed * dx
            new_y = self.y + self.speed * dy

             # Avoid overlap with the other bee
            separationDistance = 2 * self.size 
            distanceToOtherBee = ((new_x - otherBee.x) ** 2 + (new_y - otherBee.y) ** 2) ** 0.5

            if distanceToOtherBee < separationDistance:
                # Adjust position for distance
                # https://www.w3schools.com/python/ref_math_atan2.asp 
                angle = math.atan2(self.y - otherBee.y, self.x - otherBee.x)
                # https://www.geeksforgeeks.org/python-math-sin-function/  
                new_x = otherBee.x + separationDistance * math.cos(angle)
                new_y = otherBee.y + separationDistance * math.sin(angle)

            # Check if the new position is still in the canvas
            if (0 + self.size) <= new_x <= (400 - self.size) and (0 + self.size) <= new_y <= (400 - self.size):
                self.x = new_x
                self.y = new_y


    def drawGatheredPollen(self):
        pollenX, pollenY = self.x, self.y + self.size 
        pollenSize = 5  # Adjust the size of the gathered pollen circles
        for color,size in self.pollenInventory:
            if size > 0:
                drawCircle(pollenX, pollenY, pollenSize, fill=color)
                pollenX -= pollenSize  # Adjust the distance between pollen circles


    def growPollen(self, color):
        for pollen in self.pollenInventory:
            if pollen[0] == color and pollen[1] == 10:
                # Increase size by 10
                pollen[1] += 10
                break # Makes sure that only one flower grows
    


class Player(Bee):

    def __init__(self, x, y, flowers):
        Bee.__init__(self, x, y, flowers, isPlayer=True)


    def playerOnStep(self, mouseX, mouseY):
        # Move the bee toward the mouse cursor at a fixed speed
        dx = mouseX - self.x
        dy = mouseY - self.y
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5

        # Set maximum speed and acceleration 
        maxSpeed = 5
        acceleration = 0.1

        # Calculate the speed based on distance
        speed = min(maxSpeed, acceleration * distance)

        # Move the player to the mouse
        self.x += speed * dx / distance if distance > 0 else 0
        self.y += speed * dy / distance if distance > 0 else 0


    def drawPollenInventory(self):
        # Draw the pollen inventory in the top left corner
        x, y = 20, 20 
        for pollen in self.pollenInventory:
            drawCircle(x, y, pollen[1], fill=None, border=pollen[0], borderWidth = 4)
            x += 20

            # Remove pollen from inventory
            if pollen[1] == 20:
                self.pollenInventory.remove(pollen)

                

class Flower:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(['pink', 'blue', 'purple', 'red']) # https://www.w3schools.com/python/ref_random_choice.asp
        self.flowerSize = 10
        self.originalFlowerSize = 10
        self.isOriginalFlower = False
        self.isPollinator = random.choice([True, False])
        self.gathered = False
        self.isPollinated = False
        self.angle = 0  # Initial angle for the sinusoidal motion
        self.wobble = 40  # Adjust this value to control the wobbling 
    
    
    def __repr__(self):
        return f'Flower X: {self.x}  Flower Y:{self.y}'
    

    def grow(self):
        self.flowerSize += 10
        # If it's the original flower, also update its size
        if self.isOriginalFlower:
            self.originalFlowerSize += 10
    

    def drawFlower(self):
        # Draw the flower based on its type (pollinator or not)
        if self.gathered: 
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, self.flowerSize, border=self.color,borderWidth = 4, fill=None)
        elif self.isPollinator:
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, self.flowerSize, fill=self.color)
        else: 
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, self.flowerSize, border=self.color, fill=None)
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, (self.flowerSize - 4), fill=self.color)
    

    def flowerOnStep(self,removeList):
        # Move the flower up the canvas by a fixed amount
        speed = 2 
        self.y -= speed

        # Update the angle for sinusoidal motion
        self.angle += 0.05  # Adjust this value for the wobbling angle

        # Check if the flower has left the canvas
        if self.y + self.flowerSize < 0:
            # Remove the flower from the list
            removeList.append(self)
        


# Hardcoded flower for testing
app.flowers = [
    Flower(100, 100),
    Flower(200, 200),
    Flower(300, 300),
    Flower (200,300)
]   

def onAppStart(app):
    app.player = Player(app.width/2, app.height/2, app.flowers)
    app.helperBee1 = Bee(app.width/4, app.height/2, app.flowers)
    app.helperBee2 = Bee(3 * app.width/4, app.height/2, app.flowers)
    app.counter = 0
    app.toRemove = []
    app.mouseX = 0
    app.mouseY = 0
    app.startScreen = True
    app.instructions = False
    app.backgroundImage = CMUImage(Image.open('images/background.jpg'))

    # Set up animated gif
    beeGif = Image.open('images/beeGIF.gif')
    app.spriteList = []
    # I got the code below from cmu F23_Demos folder's animatedGifs.py
    for frame in range(beeGif.n_frames):
        # Set the current frame
        beeGif.seek(frame)
        # Resize the image
        fr = beeGif.resize((beeGif.size[0]//2, beeGif.size[1]//2))
        # Flip the image
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        # Convert to CMUImage
        fr = CMUImage(fr)
        # Put in our sprite list
        app.spriteList.append(fr)
    
    # Fix for broken transparency on frame 0
    # app.spriteList.pop(0)
    app.spriteCounter = 0
    app.stepsPerSecond = 20

    onStep(app)


def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

    app.helperBee1.chooseTarget(app.helperBee2)
    app.helperBee2.chooseTarget(app.helperBee1)
    
    app.player.playerOnStep(mouseX, mouseY)
    app.helperBee1.helperBeeOnStep(app.helperBee2)
    app.helperBee2.helperBeeOnStep(app.helperBee1)

    app.player.pollinate(app.flowers)
    app.helperBee1.pollinate(app.flowers)
    app.helperBee2.pollinate(app.flowers)


def onStep(app):
    app.counter += 1
    # Call the player's onStep method
    app.player.playerOnStep(app.mouseX, app.mouseY)
    app.helperBee1.helperBeeOnStep(app.helperBee2)
    app.helperBee2.helperBeeOnStep(app.helperBee1)

    # Move and update flowers
    for flower in app.flowers:
        flower.flowerOnStep(app.toRemove)

    # Remove flowers that have left the top of the canvas
    for flowerToRemove in app.toRemove:
        if flowerToRemove in app.flowers:
            app.flowers.remove(flowerToRemove)

    # Periodically generate new flowers every 20 steps
    if app.counter % 20 == 0:
        newFlower = Flower(random.randint(40, app.width - 40), app.height + 20)
        app.flowers.append(newFlower)
    
    # Set spriteCounter to next frame
    app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)


def redrawAll(app):

    if app.startScreen:
        drawRect(0,0,app.width,app.height)

        drawImage(app.spriteList[app.spriteCounter], app.width/2, app.height/2 - 84, width = 100, height = 100, align = 'center')
 
        # Heading
        drawLabel('Bee Game', app.width/2, app.height/15, font='monospace', align='center', size=50, bold=True, fill='white')
        
        # Instructions
        instructions1 = 'Are you ready to play the Bee Game?'
        instructions2 = 'Click "?" to read the instructions'
        drawLabel(instructions1, app.width/2, app.height/2, fill='white', bold=True, size = 18, font='monospace')
        drawLabel(instructions2, app.width/2, app.height/2 + 40, fill='white', bold=True, size = 18, font='monospace')
 
        # Buttons
        drawRect(app.width/2, app.height/2 + 110, 100, 50, border='white',align = 'center')
        drawLabel('Yes!', app.width/2, app.height/2 + 110, bold=True,size=18, font='monospace', fill = 'white')
        drawCircle(app.width*15/16, app.height*15/16,20,fill = "white")
        drawLabel('?', app.width*15/16, app.height*15/16, bold=True,size=22, font='monospace')

        if app.instructions:
            drawRect(app.width/2, app.height/2, 370, 200, align='center', fill = 'white')
            drawLabel('Instructions',app.width/2,app.height/3, size = 25, fill = 'grey',  font='monospace',bold = True)
            info1 = "Welcome to the Bee Game!!" 
            info2 = 'Your job is to pollinate as many flowers as you can.' 
            info3 = 'There are helper bees to help you pollinate.'
            info4 = "Hover over a flower to gather its pollen"
            info5 = "Check your inventory to see the pollen you gathered."
            info6 = 'Hover over another flower to pollinate it'
            info7 = 'Good luck!'
            info8 = 'Press escape to close instructions.'
            drawLabel(info1,app.width/2,app.height/3 + 25, size = 11, fill = 'black',  font='monospace')
            drawLabel(info2,app.width/2,app.height/3 + 40 , size = 11, fill = 'black',  font='monospace')
            drawLabel(info3,app.width/2,app.height/3 + 55 , size = 11, fill = 'black',  font='monospace')
            drawLabel(info4,app.width/2,app.height/3 + 70 , size = 11, fill = 'black',  font='monospace')
            drawLabel(info5,app.width/2,app.height/3 + 85 , size = 11, fill = 'black',  font='monospace')
            drawLabel(info6,app.width/2,app.height/3 + 100 , size = 11, fill = 'black',  font='monospace')
            drawLabel(info7,app.width/2,app.height/3 + 115 , size = 11, fill = 'black',  font='monospace')
            drawLabel(info8,app.width/2,app.height/3 + 140 , size = 11, fill = 'black',  font='monospace')

    else:
        
        # Draw the background
        drawImage(app.backgroundImage, 0, 0, width = app.width, height = app.height)

        # Draw the flowers
        for flower in app.flowers:
            flower.drawFlower()
        
        # Draw the helper bees
        app.helperBee1.drawBee(app.spriteList[app.spriteCounter])
        app.helperBee2.drawBee(app.spriteList[app.spriteCounter])
        
        # Draw the player
        app.player.drawBee(app.spriteList[app.spriteCounter])
        
        # Draw the pollen in the inventory and below the player/helper bee
        app.player.drawPollenInventory()

        # Draw the gathered pollen below the player/helper bee
        app.player.drawGatheredPollen()
        app.helperBee1.drawGatheredPollen()
        app.helperBee2.drawGatheredPollen()


def onMousePress(app, mouseX, mouseY):
    # Calculates whether the instruction button is pressed 
    cx, cy = app.width*15/16, app.height*15/16
    distance = ((mouseX - cx) ** 2 + (mouseY - cy) ** 2) ** 0.5
 
    if distance <= 20:
        app.instructions = not app.instructions
    
    buttonPressed(app, mouseX, mouseY)


def buttonPressed(app, mouseX, mouseY):
    # If yes! button is pressed, game starts 
    xRight = app.width/2 - 100
    xLeft = app.width/2 + 100
    yTop = app.height/2 + 60
    yBot = app.height/2 + 160
    if xRight <= mouseX <= xLeft and yTop <= mouseY <= yBot:
        app.startScreen = False
        return True
    return False


def onKeyPress(app,key):
    # if escape is pressed, close instructions
    if app.instructions and key == 'escape':
        app.instructions = False



runApp()


