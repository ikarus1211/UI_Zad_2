
from multiprocessing import *
from time import *

# This set represent all possible offsets that knight can move
possibleMoves = [[1, 2], [1, -2], [-1, 2], [-1, -2],
                 [2, 1], [2, -1], [-2, 1], [-2, -1]]

testfile = '4'
# Global stack for storing nodes to be visited
stack = []

# Time limit for every route
timeA = 0
timeB = 0

# List of starting positions for 5x5 and 6x6 chessboard
positionA= []
positionB= []
position = []


# My own node that represent one move and tile on chessboard
class MyNode:
    xCor = int(0)
    yCor = int(0)
    visitable = 0
    currentPath = []
    def __init__(self, corX, corY, vis):
        self.xCor = corX
        self.yCor = corY
        self.visitable = vis


#Function which parse the config file and extract values for computing
def initValues():
    global timeA
    global timeB
    global positionA
    global positionB

    file = open('cnf'+testfile+'.txt','r')
    for i in range(0,15):
        line = file.readline()
        if line[0] == '#' or line[0] == ' ':
            continue
        else:
            line = line.split(' ')
        if line[0] == 'timeA=':
            timeA = int(line[1][:-1])
        if line[0] == 'timeB=':
            timeB = int(line[1][:-1])
        if line[0][:4] == 'posA':
            positionA.append([int(line[1]),int(line[2][:-1])])
        if line[0][:4] == 'posB':
            positionB.append([int(line[1]), int(line[2][:-1])])
    print(positionA,positionB)


# This function is choosing the next valid move
# It's not so random as the name says. The moves are
#chosen based on their position in list
def randomMove(node, width):
    global moveCounter
    global stack

    # Picking every move from the list of moves.
    for move in possibleMoves:
        yOffset = node.yCor + move[1]
        xOffset = node.xCor + move[0]
        # Controlling borders of chessboard
        if yOffset < 0 or yOffset > width - 1 or xOffset < 0 or xOffset > width - 1:
            continue
        # Checking if the node is not already part of the path
        if [xOffset,yOffset] in node.currentPath:
            continue
        # If none of the condition above are fulfilled then it must be legal move
        if [xOffset,yOffset] not in node.currentPath:
            newNode = MyNode(xOffset, yOffset, node.visitable + 1)
            newNode.currentPath = node.currentPath.copy()
            newNode.currentPath.append([xOffset,yOffset])
            stack.append(newNode)


# Main drive function with main loop
def driveF(position):
    global moveCounter
    global stack

    # Initialising first node
    width = position[2]
    startNode = MyNode(int(position[0]), int(position[1]), 1)
    startNode.currentPath = MyNode.currentPath.copy()
    startNode.currentPath.append([int(position[0]), int(position[1])])
    stack.append(startNode)

    # Main loop that run until stack is empty which means that the algorithm
    #tried every possible move
    while True:

        # If stack is empty
        if not stack:
            print("Not a valid root")
            break

        # If not it pops the last node
        else:
            nextNode = stack.pop()
        # Checks if I did not finished
        if nextNode.visitable == width * width:
            print("I've done it")
            print(nextNode.currentPath, end= '\n')
            return nextNode.currentPath
        randomMove(nextNode,width)
    return -1

# Main function
# It checks if the process is not running longer than it should be
if __name__ == '__main__':
    initValues()
    for pos in positionA:
        pos.append(6)
        proc = Process(target=driveF, args=[pos])
        proc.start()
        startTime = time()
        while proc.is_alive():
            sleep(1)
            currTime = time()
            if currTime > startTime+timeA:
                print('Process run out of time')
                proc.terminate()
                sleep(1)
        proc.join()
        stack.clear()
    for pos in positionB:
        pos.append(5)
        proc = Process(target=driveF, args=[pos])
        proc.start()
        startTime = time()
        while proc.is_alive():
            sleep(1)
            currTime = time()
            if currTime > startTime+timeB:
                print('Process run out of time')
                proc.terminate()
        proc.join()
        stack.clear()
