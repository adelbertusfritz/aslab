from tabulate import tabulate
from random import randint

class Infantry:
    def __init__(self, position, number):
        self.divisionNumber = number
        self.position = position
        self.path = ''
        self.finalDestination = position

    def setPath(self, path):
        self.path = path

    def setFinalDestination(self, position):
        self.finalDestination = position

class FrontLine:
    def __init__(self, position):
        self.position = position
        self.reachableInfantries = []
        self.infantryDispatch = None

    def addReachableInfantries(self, infantry, distance):
        self.reachableInfantries.append({
            "infantry": infantry,
            "distance": distance
        })
    
    def findClosestInfantry(self):
        if len(self.reachableInfantries) == 0:
            return None
        closest = self.reachableInfantries[0]
        for reachable in self.reachableInfantries:
            if reachable["distance"] < closest["distance"]:
                closest = reachable
        return closest["infantry"]
    
    def removeInfantry(self, infantry):
        index = -1
        while self.reachableInfantries[index]["infantry"] != infantry:
            index += 1
        self.reachableInfantries.pop(index)
    
    def setInfantryDispatch(self, infantry):
        self.infantryDispatch = infantry

class BattleField:
    def __init__(self, size):
        self.grid = [['' for i in range(size)] for i in range(size)]
        self.size = size
        self.obstacleCount = randint(size, 2*size)
        self.frontLines = [FrontLine((i, size-1)) for i in range(size)]
        self.infantries = []
    
    def show(self):
        tableView = [['' for i in range(self.size)] for i in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if isinstance(self.grid[row][col], Infantry):
                    tableView[row][col] = 'D'
                else:
                    tableView[row][col] = self.grid[row][col]
        print(tabulate(tableView, tablefmt='simple_grid'))
    
    def showFinal(self):
        tableView = [['' for i in range(self.size)] for i in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if isinstance(self.grid[row][col], Infantry):
                    tableView[row][col] = ''
                    (x,y) = self.grid[row][col].finalDestination
                    tableView[x][y] = 'R'
                elif tableView[row][col] != 'R':
                    tableView[row][col] = self.grid[row][col]
        print(tabulate(tableView, tablefmt='simple_grid'))

    def emptyFields(self):
        result = []
        for i in range(self.size):
            for j in range(self.size-2):
                if self.grid[i][j] == '':
                    result.append((i,j))
        return (result, len(result))
    
    def isValidField(self, position):
        (x,y) = position
        if x not in range(0, self.size) or y not in range(0, self.size):
            return False
        elif self.grid[x][y] == 'X':
            return False
        return True
    
    def setObstacles(self, obstacles=None):
        if obstacles != None:
            for obstacle in obstacles:
                (x,y) = obstacle
                self.grid[x][y] = 'X'
        else:
            for i in range(self.obstacleCount):
                (ef, efSize) = self.emptyFields()
                (x,y) = ef[randint(0, efSize-1)]
                self.grid[x][y] = 'X'
    
    def addInfantry(self, divisionNumber, location=None):
        if location == None:
            (ef, efSize) = self.emptyFields()
            (x,y) = ef[randint(0, efSize-1)]
        else:
            (x,y) = location
            if x not in range(0, self.size) or y not in range(0, self.size):
                return (False, 'Gagal. Anda menempatkan divisi di luar medan perang.')
            elif isinstance(self.grid[x][y], Infantry):
                return (False, 'Gagal. Ada divisi lain di posisi ini.')
            elif self.grid[x][y] == 'X':
                return (False, 'Gagal. Ada halangan di posisi ini.')
            elif y == self.size-1 :
                return (False, 'Gagal. Anda menempatkan divisi di posisi tujuan.')
        newInfantry = Infantry((x,y), divisionNumber)
        self.infantries.append(newInfantry)
        self.grid[x][y] = newInfantry
        return (True, f'Divisi-{divisionNumber} masuk ke posisi ({x},{y})')

    def findReachableInfantries(self, frontLine:FrontLine):
        path_queue = [{ "position": frontLine.position, "distance": 0 }]
        visited = [frontLine.position]
        while len(path_queue) > 0:
            (next_x, next_y) = path_queue[0]["position"]
            distance = path_queue[0]["distance"]
            path_queue.pop(0)
            
            if isinstance(self.grid[next_x][next_y], Infantry):
                frontLine.addReachableInfantries(self.grid[next_x][next_y],  distance)

            up_path = (next_x-1, next_y)
            down_path = (next_x+1, next_y)
            left_path = (next_x, next_y-1)
            right_path = (next_x, next_y+1)
            if self.isValidField(up_path) and up_path not in visited:
                path_queue.append({ "position": up_path, "distance": distance+1 })
                visited.append(up_path)
            if self.isValidField(down_path) and down_path not in visited:
                path_queue.append({ "position": down_path, "distance": distance+1 })
                visited.append(down_path)
            if self.isValidField(left_path) and left_path not in visited:
                path_queue.append({ "position": left_path, "distance": distance+1 })
                visited.append(left_path)
            if self.isValidField(right_path) and right_path not in visited:
                path_queue.append({ "position": right_path, "distance": distance+1 })
                visited.append(right_path)

    def removeInfantryFromOtherFrontLines(self, infantry: Infantry):
        for frontLine in self.frontLines:
            frontLine.removeInfantry(infantry)

    def findShortestPath(self, infantry:Infantry, frontline: FrontLine):
        start = infantry.position
        (x,y) = frontline.position
        end = (x,y-1)
        path_queue = [{"end": start, "path": ''}]
        visited = [start]
        (next_x, next_y) = path_queue[0]["end"]
        currpath = path_queue[0]["path"]
        path_queue.pop(0)
        while (next_x, next_y) != end:
            up_path = (next_x-1, next_y)
            down_path = (next_x+1, next_y)
            left_path = (next_x, next_y-1)
            right_path = (next_x, next_y+1)
            if self.isValidField(up_path) and up_path not in visited:
                path_queue.append({ "end": up_path, "path": currpath + "U" })
                visited.append(up_path)
            if self.isValidField(down_path) and down_path not in visited:
                path_queue.append({ "end": down_path, "path": currpath + "S" })
                visited.append(down_path)
            if self.isValidField(left_path) and left_path not in visited:
                path_queue.append({ "end": left_path, "path": currpath + "B" })
                visited.append(left_path)
            if self.isValidField(right_path) and right_path not in visited:
                path_queue.append({ "end": right_path, "path": currpath + "T" })
                visited.append(right_path)
            (next_x, next_y) = path_queue[0]["end"]
            currpath = path_queue[0]["path"]
            path_queue.pop(0)
        infantry.setPath(currpath + 'T')
        infantry.setFinalDestination(frontline.position)
        
    def solve(self):
        for frontLine in self.frontLines:
            self.findReachableInfantries(frontLine)
        for frontLine in self.frontLines:
            closestInfantry = frontLine.findClosestInfantry()
            if closestInfantry != None:
                frontLine.setInfantryDispatch(closestInfantry)
                self.removeInfantryFromOtherFrontLines(closestInfantry)
        for frontLine in self.frontLines:
            if frontLine.infantryDispatch != None:
                self.findShortestPath(frontLine.infantryDispatch, frontLine)
    
    def printResult(self):
        for infantry in self.infantries:
            print(f"Divisi ke-{infantry.divisionNumber}:")
            print(f"Posisi awal = {(infantry.position[1], infantry.position[0])}")
            print(f"Arah perjalanan = {infantry.path}")
            fD = (infantry.finalDestination[1], infantry.finalDestination[0]) 
            print(f"Posisi akhir = {fD}")
            print("---------------------------------")

running = True
while running:
    n = int(input("Masukkan banyaknya divisi: "))
    input2 = input("Apakah anda ingin menempatkan divisi secara manual (y/n): ")
    randomInfantry = True if input2 == 'n' else False
    print("Berikut adalah tampilan grid awal")
    battlefield = BattleField(n)
    battlefield.setObstacles()
    battlefield.show()
    
    if randomInfantry:
        for i in range(battlefield.size):
            (status, message) = battlefield.addInfantry(i+1)
    else:
        for i in range(battlefield.size):
            position = eval(input(f"Masukan posisi divisi ke-{i+1} (x,y): "))
            (status, message) = battlefield.addInfantry(i+1, (position[1], position[0]))
            while status == False:
                print(message)
                position = eval(input(f"Masukan posisi divisi ke-{i+1} (x,y): "))
                (status, message) = battlefield.addInfantry(i+1, (position[1], position[0]))
    print("Berikut adalah tampilan grid setelah dimasukkan divisi")
    battlefield.show()
    print("Berikut adalah jalur yang dilalui tiap divisi")
    battlefield.solve()
    battlefield.printResult()
    print("Berikut adalah tampilan grid akhir")
    battlefield.showFinal()

    again = input('Apakah anda ingin mengulang program? (y/n): ')
    running = True if again == 'y' else False
print("Vive la France!")