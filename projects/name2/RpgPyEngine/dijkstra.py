from heapq import *
import time
from random import randint
from math import dist
import os
arr = []
clear = lambda: os.system('cls')

for i in range(50):
    arr.append([0]*50)
def draw(arr, a, b, path):
    #clear()
    #strDraw = ""
    #for i in range(len(arr)-1, -1, -1):
    #    for i2 in range(len(arr[0])):
    #        flagP = False
    #        for i3 in range(len(path)):
    #            if i2==path[i3][0] and i==path[i3][1]:
    #                flagP = True
#
    #        if i2 == a[0] and i == a[1]:
    #            strDraw += f"Я  "
    #        elif i2 == b[0] and i == b[1]:
    #            strDraw += f"@  "
    #        elif flagP:
    #            strDraw += f"^  "
    #        else:
    #            strDraw += f"{arr[i][i2]}  "
    #    strDraw += "\n"
    #clear()
    #print(strDraw)
    pass


def draw2(arr):
    sisa = [len(arr), len(arr[0])]
    print("ssssss", sisa, "eeeee")
    for i in range(len(arr)):
        for i2 in range(len(arr[0])):
            if arr[i2][i] == 1:
                print("#", end=" ")
            elif arr[i2][i] == 0:
                print(".", end=" ")
            else:
                print(arr[i2][i], end=" ")
        print()

def fill(arr):
    for i in range(50):
        for i2 in range(50):
            if randint(0,10)>10:
                arr[i2][i] = 1

#def fill(arr):
#    graph = dict()





def get_neighbours(x, y, grid, cols, rows):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]  # , [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]







def heuristic(a, b):
    return dist(a, b)

def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited

def pathSearch(a, b, arr):
    graph = {}
    #print("pipa")
    arr2 = arr.copy()


    #print("popa")
    grid = arr


    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            #print(len(arr), len(arr[0]))
            size = [len(arr[0]), len(arr)]
            #if size[0]>50:
            #    size[0] = 50
            #if size[1]>50:
            #    size[1] = 50
            graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y, grid, size[0], size[1])

    path = []


    start = a
    goal = b
    visited = dijkstra(start, goal, graph)
    cur_node = goal
    while cur_node != start:
        cur_node = visited[cur_node]
        path.append(cur_node)

    draw(arr2, a, b, path)
    return path

#print(pathSearch((0,0), (40, 40), arr))




