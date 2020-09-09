from math import inf, sqrt
from heapq import heappop, heappush


def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    path = []
    boxes = {}
    startingBox = findBox(source_point, mesh, boxes)
    goalBox = findBox(destination_point, mesh, boxes)
    queue = [(0,startingBox)]
    costs = {}
    costs[startingBox] = 0
    parents = {}
    parents[startingBox] = None
    parentCoordinates = {}
    parentCoordinates[startingBox] = source_point
    detailPoints = {}

    if startingBox not in mesh['boxes'] or goalBox not in mesh['boxes']:
        print("No Path Found!")
        return ([],[])

    while queue:
        currentCost, current = heappop(queue)
        if current == goalBox:
            path = [[parentCoordinates[current], destination_point]]
            parentBox = parents[current]
            parentBoxCoordinate = parentCoordinates[current]
            while parentBox:
                path.insert(0,[parentCoordinates[parentBox], parentBoxCoordinate])
                parentBoxCoordinate = parentCoordinates[parentBox]
                parentBox = parents[parentBox]
            return path, boxes.keys()


        for adj in mesh['adj'][current]:
            boxes[adj] = current

            xRange = [max(current[0], adj[0]),min(current[1], adj[1])]
            yRange = [max(current[2], adj[2]),min(current[3], adj[3])]

            currentDist = inf, source_point
            newDist = 0, (0,0)
            if((xRange[0]-xRange[1]) != 0):
                if xRange[0] > xRange[1]:
                    for x in range(xRange[1], xRange[0]):
                        newDist = (euclidian(parentCoordinates[startingBox], (x,yRange[0])) + heuristic(destination_point, (x,yRange[0])), (x,yRange[0]))
                        if newDist[0] < currentDist[0]:
                            currentDist = newDist
                else:
                    for x in range(xRange[0], xRange[1]):
                        newDist = (euclidian(parentCoordinates[startingBox], (x,yRange[0])) + heuristic(destination_point, (x,yRange[0])), (x,yRange[0]))
                        if newDist[0] < currentDist[0]:
                            currentDist = newDist

            elif((yRange[0]-yRange[1]) != 0):
                if xRange[0] > xRange[1]:
                    for y in range(yRange[1], yRange[0]):
                        newDist = (euclidian(parentCoordinates[startingBox], (xRange[0], y)) + heuristic(destination_point, (xRange[0], y)), (xRange[0], y))
                        if newDist[0] < currentDist[0]:
                            currentDist = newDist
                else:
                    for y in range(yRange[0], yRange[1]):
                        newDist = (euclidian(parentCoordinates[startingBox], (xRange[0], y)) + heuristic(destination_point, (xRange[0], y)), (xRange[0], y))
                        if newDist[0] < currentDist[0]:
                            currentDist = newDist



            pathCost = currentDist[0]

            if adj not in costs:
                parentCoordinates[adj] = currentDist[1]
                parents[adj] = current
                costs[adj] = pathCost
                heappush(queue, (pathCost, adj))
            else:
                continue
    print("No Path Found!")
    return ([], [])



def findBox(point, mesh, boxes):
    for box in mesh['boxes']:
        if found(box, point) and box not in boxes:
            return box
        else:
            continue

def found(box, point):
    x1, x2, y1, y2 = box
    x, y = point
    return (x > x1 and x < x2 and y > y1 and y < y2)

def euclidian(a, b):
    delta_x = a[0] - b[0]
    delta_y = a[1] - b[1]
    return (sqrt(delta_x ** 2 + delta_y ** 2) * 0.5)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
