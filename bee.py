from cmu_graphics import *
import math
import random

class Player:
    def __init__(self, x, y, flowers):
        self.x = x
        self.y = y
        self.playerSize = 20
        self.flowerSize = 10
        self.speed = 5  #this is the speed of the mouse
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

                # Check if the flower can be pollinated
                elif not flower.isPollinator and not flower.gathered and flower.color in self.pollenInventory: 
                    flower.gathered = True
                    flower.grow()
                    self.growOriginalFlower(flower.color)
                    self.growPollen(flower.color)

    def drawPollenInventory(self):
        # Draw the pollen inventory in the top left corner
        x, y = 20, 20
        for flowerColor, pollenSize in self.pollenInventory.items():
            drawCircle(x, y, pollenSize, fill=None, border=flowerColor)
            x += 20

    def drawGatheredPollen(self):
        self.pollenX, self.pollenY = self.x, self.y + self.playerSize 
        pollenSize = 5  # Adjust the size of the gathered pollen circles
        for color, number in self.pollenInventory.items():
                drawCircle(self.pollenX, self.pollenY, pollenSize, fill=color)
                self.pollenX -= pollenSize  # Adjust the distance between pollen circles

    
    def growPollen(self,color):
        # Find the pollen in the inventory based on color and make it grow
        if color in self.pollenInventory:
            self.pollenInventory[color] += 10
                
    
    def growOriginalFlower(self, color):
        # Find the original flower based on color and make it grow
        for flower in self.flowers:
            if flower.color == color and not flower.gathered:
                flower.grow()
    

class Flower:
    def __init__(self, x, y, color, isPollinator):
        self.x = x
        self.y = y
        self.color = color
        self.flowerSize = 10
        self.isPollinator = isPollinator
        self.gathered = False

    def drawFlower(self):
        # Draw the flower based on its type (pollinator or not)
        if self.isPollinator:
            drawCircle(self.x, self.y, self.flowerSize, fill=self.color)
        else:
            drawCircle(self.x, self.y, self.flowerSize, border=self.color,fill=None)
    
    def flowerOnStep(self):
        # Move the flower up the canvas by a fixed amount
        speed = 2  # Adjust this value as needed
        self.y -= speed

        # Check if the flower has left the canvas
        if self.y + self.flowerSize < 0:
            # Remove the flower from the list
            app.toRemove.append(self)
    
    def grow(self):
        # For simplicity, instant growth when pollinated
        self.flowerSize += 10

app.toRemove = list()

# Hardcoded flower for testing
app.flowers = [
    Flower(100, 100, 'red', True),
    Flower(200, 200, 'blue', False),
    Flower(300, 300, 'purple', True),
    Flower (200,300,'blue', True)
]   

def onAppStart(app):
    app.player = Player(app.width/2, app.height/2, app.flowers)
    app.counter = 0

def onMouseMove(app, mouseX, mouseY):
    app.player.playerOnStep(mouseX, mouseY)
    app.player.pollinate(app.flowers)

def onStep(app):
    app.counter += 1

def callOnStep(app):
    # Call the player's onStep method
    app.player.playerOnStep(app)

    # Move and update flowers
    for flower in app.flowers:
        flower.flowerOnStep(app)

    # Remove flowers that have left the top of the canvas
    for flowerToRemove in app.toRemove:
        app.flowers.remove(flowerToRemove)

    # Periodically generate new flowers
    if app.stepCount % 50 == 0:
        newFlower = Flower(random.randint(50, app.width - 50), app.height + 20, 'purple', random.choice([True, False]))
        app.flowers.append(newFlower)
    

def redrawAll(app):

    # Draw the flowers
    for flower in app.flowers:
        flower.drawFlower()
    
    # Draw the player
    app.player.drawPlayer()
    
    # Draw the pollen in the inventory and below the player
    app.player.drawPollenInventory()
    app.player.drawGatheredPollen()

runApp()
