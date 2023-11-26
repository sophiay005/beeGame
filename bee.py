from cmu_graphics import *
import math
import random
from PIL import Image

class Player:

    def __init__(self, x, y, flowers):
        self.x = x
        self.y = y
        self.playerSize = 20
        self.flowerSize = 10
        self.speed = 2  #this is the speed of the mouse
        self.pollenInventory = {}
        self.flowers = flowers


    def drawPlayer(self):
        drawCircle(self.x, self.y, self.playerSize, fill='yellow')


    def playerOnStep(self, mouseX, mouseY):
        # Move the bee toward the mouse cursor at a fixed speed
        dx = mouseX - self.x
        dy = mouseY - self.y
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5

        if distance > 0:
            dx /= distance
            dy /= distance

        # Move the player
        self.x += self.speed * dx
        self.y += self.speed * dy


    def pollinate(self, flowers):
        # Loop through all flowers
        for flower in flowers:
            distance = ((flower.x - self.x) ** 2 + (flower.y - self.y) ** 2) ** 0.5

            if distance <= (self.playerSize + self.flowerSize):
                # Check if the flower is a pollinator and not yet gathered
                if flower.isPollinator and not flower.gathered:
                    flower.gathered = True
                    self.pollenInventory[flower.color] = self.pollenInventory.get(flower.color, 10)
                  
                    # Grow the original flower
                    self.growOriginalFlower(flower)

                # Check if the flower can be pollinated
                elif not flower.isPollinator and not flower.gathered and flower.color in self.pollenInventory: 
                    flower.gathered = True
                    flower.grow()
                    
                    # Grow the original flower
                    self.growOriginalFlower(flower)
                   
                    self.growPollen(flower.color)
                    del self.pollenInventory[flower.color]


    def drawPollenInventory(self):
        # Draw the pollen inventory in the top left corner
        x, y = 20, 20
        for flowerColor, pollenSize in self.pollenInventory.items():
            drawCircle(x, y, pollenSize, fill=None, border=flowerColor)
            x += 20


    def drawGatheredPollen(self):
        pollenX, pollenY = self.x, self.y + self.playerSize 
        pollenSize = 5  # Adjust the size of the gathered pollen circles
        for color, number in self.pollenInventory.items():
                drawCircle(pollenX, pollenY, pollenSize, fill=color)
                pollenX -= pollenSize  # Adjust the distance between pollen circles


    def growPollen(self,color):
        # Find the pollen in the inventory based on color and make it grow
        if color in self.pollenInventory:
            self.pollenInventory[color] += 10
    

    def growOriginalFlower(self, flower):
        # Find the original flower based on color and make it grow
        for originalFlower in self.flowers:
            if originalFlower.color == flower.color and not originalFlower.gathered and originalFlower.x == flower.x and originalFlower.y == flower.y:
                originalFlower.grow()



class HelperBee:

    def __init__(self, x, y, flowers):
        self.x = x
        self.y = y
        self.HelperBeeSize = 20
        self.flowerSize = 10
        self.speed = 3  #this is the speed of the bee
        self.pollenInventory = {}
        self.flowers = flowers
        self.target = None


    def drawHelperBee(self):
        drawCircle(self.x, self.y, self.HelperBeeSize, fill='yellow')
    

    def pollinate(self, flowers):
        # Loop through all flowers
        for flower in flowers:
            distance = ((flower.x - self.x) ** 2 + (flower.y - self.y) ** 2) ** 0.5

            if distance <= (self.HelperBeeSize + self.flowerSize):
                # Check if the flower is a pollinator and not yet gathered
                if flower.isPollinator and not flower.gathered:
                    flower.gathered = True
                    self.pollenInventory[flower.color] = self.pollenInventory.get(flower.color, 10)

                    # Grow the original flower
                    self.growOriginalFlower(flower)

                # Check if the flower can be pollinated
                elif not flower.isPollinator and not flower.gathered and flower.color in self.pollenInventory: 
                    flower.gathered = True
                    flower.grow()
                    
                    # Grow the original flower
                    self.growOriginalFlower(flower)

                    self.growPollen(flower.color)
                    del self.pollenInventory[flower.color]
    

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
                    if otherBeeDistance < 2 * self.HelperBeeSize:
                        continue  # Skip this flower if it's close to the other bee
                    
                    if distance < minDistance:
                        minDistance = distance
                        self.target = flower


    def helperBeeOnStep(self, otherBee):
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
            separationDistance = 2 * self.HelperBeeSize  # Adjust this value as needed
            distanceToOtherBee = ((new_x - otherBee.x) ** 2 + (new_y - otherBee.y) ** 2) ** 0.5

            if separationDistance < separationDistance:
                # Adjust position to maintain a safe distance
                angle = math.atan2(self.y - otherBee.y, self.x - otherBee.x)
                new_x = otherBee.x + separationDistance * math.cos(angle)
                new_y = otherBee.y + separationDistance * math.sin(angle)

            # Check if the new position is within the canvas
            if (0 + self.HelperBeeSize) <= new_x <= (400 - self.HelperBeeSize) and (0 + self.HelperBeeSize) <= new_y <= (400 - self.HelperBeeSize):
                self.x = new_x
                self.y = new_y


    def drawGatheredPollen(self):
        pollenX, pollenY = self.x, self.y + self.HelperBeeSize 
        pollenSize = 5  # Adjust the size of the gathered pollen circles
        for color, number in self.pollenInventory.items():
                drawCircle(pollenX, pollenY, pollenSize, fill=color)
                pollenX -= pollenSize  # Adjust the distance between pollen circles


    def growPollen(self,color):
        # Find the pollen in the inventory based on color and make it grow
        if color in self.pollenInventory:
            self.pollenInventory[color] += 10
    

    def growOriginalFlower(self, flower):
        # Find the original flower based on color and make it grow
        for originalFlower in self.flowers:
            if originalFlower.color == flower.color and not originalFlower.gathered and originalFlower.x == flower.x and originalFlower.y == flower.y:
                originalFlower.grow()



class Flower:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(['pink', 'blue', 'purple', 'red'])
        self.flowerSize = 10
        self.isPollinator = random.choice([True, False])
        self.gathered = False
        self.angle = 0  # Initial angle for sinusoidal motion
        self.wobble = 40  # Adjust this value to control the wobbling 


    def drawFlower(self):
        # Draw the flower based on its type (pollinator or not)
        if self.isPollinator:
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, self.flowerSize, fill=self.color)
        else:
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, self.flowerSize, border=self.color, fill=None)
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, (self.flowerSize - 4), fill=self.color)
    

    def flowerOnStep(self,removeList):
        # Move the flower up the canvas by a fixed amount
        speed = 2  # Adjust this value as needed
        self.y -= speed

        # Update the angle for sinusoidal motion
        self.angle += 0.05  # Adjust this value for the wobbling effect

        # Check if the flower has left the canvas
        if self.y + self.flowerSize < 0:
            # Remove the flower from the list
            removeList.append(self)
    

    def grow(self):
        # For simplicity, instant growth when pollinated
        self.flowerSize += 10



# Hardcoded flower for testing
app.flowers = [
    Flower(100, 100),
    Flower(200, 200),
    Flower(300, 300),
    Flower (200,300)
]   


def onAppStart(app):
    app.player = Player(app.width/2, app.height/2, app.flowers)
    app.helperBee1 = HelperBee(app.width/4, app.height/2, app.flowers)
    app.helperBee2 = HelperBee(3 * app.width/4, app.height/2, app.flowers)
    app.counter = 0
    app.toRemove = []
    app.mouseX = 0
    app.mouseY = 0
    app.beeImage = CMUImage(Image.open('images/beeimage.jpg'))
    onStep(app)
    restart(app)


def restart(app):
    app.startScreen = True
    app.instructions = False


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

    # Periodically generate new flowers every 30 steps
    if app.counter % 30 == 0:
        newFlower = Flower(random.randint(40, app.width - 40), app.height + 20)
        app.flowers.append(newFlower)


def redrawAll(app):

    if app.startScreen:
        drawRect(0,0,app.width,app.height)

        drawImage(app.beeImage, app.width/2, app.height/2 - 84, width = 100, height = 100, align = 'center')
 
        # heading
        drawLabel('Bee Game', app.width/2, app.height/15, font='monospace', align='center', size=50, bold=True, fill='white')
        
        # instructions
        instructions1 = 'Are you ready to play the Bee Game?'
        instructions2 = 'Click "?" to read the instructions'
        drawLabel(instructions1, app.width/2, app.height/2, fill='white', bold=True, size = 18, font='monospace')
        drawLabel(instructions2, app.width/2, app.height/2 + 40, fill='white', bold=True, size = 18, font='monospace')
 
        # buttons
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
        # Draw the flowers
        for flower in app.flowers:
            flower.drawFlower()
        
        # Draw the helper bees
        app.helperBee1.drawHelperBee()
        app.helperBee2.drawHelperBee()
        
        # Draw the player
        app.player.drawPlayer()
        
        # Draw the pollen in the inventory and below the player/helper bee
        app.player.drawPollenInventory()

        # Draw the gathered pollen below the player/helper bee
        app.player.drawGatheredPollen()
        app.helperBee1.drawGatheredPollen()
        app.helperBee2.drawGatheredPollen()


def onMousePress(app, mouseX, mouseY):
    #calculates whether the instruction button is pressed 
    cx, cy = app.width*15/16, app.height*15/16
    distance = ((mouseX - cx) ** 2 + (mouseY - cy) ** 2) ** 0.5
 
    if distance <= 20:
        app.instructions = not app.instructions
    
    buttonPressed(app, mouseX, mouseY)


def buttonPressed(app, mouseX, mouseY):
    #if yes! button is pressed, game starts 
    xRight = app.width/2 - 100
    xLeft = app.width/2 + 100
    yTop = app.height/2 + 60
    yBot = app.height/2 + 160
    if xRight <= mouseX <= xLeft and yTop <= mouseY <= yBot:
        app.startScreen = False
        return True
    return False


def onKeyPress(app,key):
    # restart if r pressed
    if key == 'r':
        restart(app)

    # if escape is pressed, close instructions
    if app.instructions and key == 'escape':
        app.instructions = False



runApp()
