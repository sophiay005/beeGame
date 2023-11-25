from cmu_graphics import *

def onAppStart(app):
    app.x = 10
    app.y = 10

def redrawAll(app):
    drawCircle(app.x,app.y,10)

runApp()