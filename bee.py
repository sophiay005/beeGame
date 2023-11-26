from cmu_graphics import *
import math
import random

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

                # Check if the flower can be pollinated
                elif not flower.isPollinator and not flower.gathered and flower.color in self.pollenInventory: 
                    flower.gathered = True
                    flower.grow()
                    self.growOriginalFlower(flower.color)
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
    
    def growOriginalFlower(self, color):
        # Find the original flower based on color and make it grow
        for flower in self.flowers:
            if flower.color == color and not flower.gathered:
                flower.grow()

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

                # Check if the flower can be pollinated
                elif not flower.isPollinator and not flower.gathered and flower.color in self.pollenInventory: 
                    flower.gathered = True
                    flower.grow()
                    self.growOriginalFlower(flower.color)
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
    
    def growOriginalFlower(self, color):
        # Find the original flower based on color and make it grow
        for flower in self.flowers:
            if flower.color == color and not flower.gathered:
                flower.grow()


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
            drawCircle(self.x + math.sin(self.angle) * self.wobble, self.y, self.flowerSize, border=self.color,fill=None)
    
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

    # Periodically generate new flowers every 30 steps
    if app.counter % 30 == 0:
        newFlower = Flower(random.randint(40, app.width - 40), app.height + 20)
        app.flowers.append(newFlower)

def redrawAll(app):

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

runApp()
