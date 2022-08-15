from tkinter import Y

from pynput.keyboard import Key, Listener
from load_hack import AliceGameExeBoardData
from keypress_hack import AliceGameExeInputSender
from directional_graph import DirectionalGraph
from console_interface import ConsoleInterface
from agent import Agent
from table import Table
import time
import threading
import os

clear = lambda: os.system('cls')
keyPressed = ''
activeGame = False

def redrawLoop(consoleInterface, char):
        loop = True
        while loop:
            if keyPressed == Key.esc or char.isDead():
                loop = False
            if activeGame:
                clear()
                consoleInterface.draw()
            time.sleep(0.5)
        if (char.isDead()):
            print('You are Dead.')

def main():
    global activeGame
    while not activeGame:
        aliceGameBoard = AliceGameExeBoardData()
        aliceGameBoard.loadBoard()
        table = Table(aliceGameBoard.getBoardWidth(), aliceGameBoard.getBoardHeight(), 4)
        agent = Agent()
        consoleInterface = ConsoleInterface(table)
        #table.addWallsOnBorders()
        table.loadFromList(aliceGameBoard.getBoard())
        playerPos = aliceGameBoard.getPlayerPosition()
        agent.setPosision(playerPos[0], playerPos[1])
        #agent.setCenterPosision(table.getSize())
        agent.setAgentOnTable(table)
        #table.createFlagOnRandomNumericLocation()
        thread = threading.Thread(target=redrawLoop, args=(consoleInterface, agent,))
        thread.start()
        directionalGraph = DirectionalGraph()

        allValidSquaresOnTable = table.getListOfNumericTablePositions() + [agent.getAgentPosition()]
        directionalGraph.addVerticesFrom(allValidSquaresOnTable)
        for square in allValidSquaresOnTable:
            listOfMovementsInSquare = table.getListOfMovementsInPosition(square[0], square[1])
            for movementsInSquare in listOfMovementsInSquare:
                directionalGraph.addEdge(square, movementsInSquare)
        shortestPath = directionalGraph.shortestPath(agent.getAgentPosition(), table.getFlagCoords(), recalc = False)
        consoleInterface.createPath(shortestPath)
        consoleInterface.draw()

        inputSender = AliceGameExeInputSender()
        inputSender.automate(shortestPath)
        time.sleep(6)

    def on_release(key):
        global activeGame
        global keyPressed
        keyPressed = key
        keyPressedAsString = str(format(keyPressed))
        if (keyPressedAsString == "'p'"):
            consoleInterface.clearPath()
            activeGame = True
        if (activeGame):
            print(keyPressedAsString)
            if (keyPressedAsString == "<104>"):
                agent.moveUpOnTable(table)
            if (keyPressedAsString == "<98>"):
                agent.moveDownOnTable(table)
            if (keyPressedAsString == "<100>"):
                agent.moveLeftOnTable(table)
            if (keyPressedAsString == "<102>"):
                agent.moveRightOnTable(table)
        if key == Key.esc:
            return False

    def on_press(key):
        global keyPressed
        keyPressed = key
        
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()