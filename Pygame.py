def initialiseState(col, row, orientation, agility, strength):
  return {
    "playerSquare": (col, row),
    "player": {
      "type": "player",
      "orientation": orientation,
      "agility": agility,
      "strength": strength
    },
    "others": {}
  }


def addHerb(state, col, row, agility):
  state["others"][(col, row)] = {"type": "herb", "agility": agility}


def addBread(state, col, row, strength):
  state["others"][(col, row)] = {"type": "bread", "strength": strength}


def addBlock(state, col, row, height):
  state["others"][(col, row)] = {"type": "block", "height": height}


def getEntityAt(state, col, row):
  if state["playerSquare"] == (col, row):
    return state["player"]
  elif (col, row) in state["others"]:
    return state["others"][(col, row)]
  return {}


def showBoard(state, cols, rows):

  startCol = int(state["playerSquare"][0] - cols)
  endCol = startCol + (2 * cols + 1)
  startRow = int(state["playerSquare"][1] - rows)
  endRow = startRow + (2 * rows + 1)
  # Iterate through each square on the board
  for row in range(startRow, endRow):
    for col in range(startCol, endCol):
      entity = getEntityAt(state, col, row)
      # If there's nothing here
      if not entity:
        print(". ", end="")
      # If it's a player, show arrow based on orientation
      elif entity["type"] == "player":
        if entity["orientation"] == "left":
          print("\u2190 ", end="")
        elif entity["orientation"] == "up":
          print("\u2191 ", end="")
        elif entity["orientation"] == "right":
          print("\u2192 ", end="")
        else:
          print("\u2193 ", end="")
      # If it's an herb
      elif entity["type"] == "herb":
        print("# ", end="")
      # If it's a bread
      elif entity["type"] == "bread":
        print("@ ", end="")
      # If it's a block, show height
      elif entity["type"] == "block":
        print(entity['height'], end="")
    print()


def getPlayer(state):
  return state["player"]


def getPlayerSquare(state):
  return state["playerSquare"]


def turn(state, direction):
  player = getPlayer(state)

  if direction == "up" or direction == "down" or direction == "left" or direction == "right":
    player["orientation"] = direction
    state["player"] = player
    return 1
  else:
    return -1


def step(state):
  # Copy player square into a list
  square = list(state["playerSquare"])
  # Change col or row of square based on orientation to get adjacent square
  if state["player"]["orientation"] == "up":
    square[1] -= 1
  elif state["player"]["orientation"] == "down":
    square[1] += 1
  elif state["player"]["orientation"] == "left":
    square[0] -= 1
  else:
    square[0] += 1
  # If there's an entity at the square, failure
  ent = getEntityAt(state, square[0], square[1])
  if ent != {} and ent["type"] != "player":
    return -1
  state["playerSquare"] = tuple(square)
  if ent == {}:
    return 1


def showPlayer(state):
  p1 = getPlayer(state)
  print("column: ", state["playerSquare"][0])
  print("row: ", state["playerSquare"][1])
  print("orientation: ", p1["orientation"])
  print("agility: ", p1["agility"])
  print("strength: ", p1["strength"])


def showFacing(state):
  # Copy player square into a list
  square = list(state["playerSquare"])
  # Change col or row of square based on orientation to get adjacent square
  if state["player"]["orientation"] == "up":
    square[1] -= 1
  elif state["player"]["orientation"] == "down":
    square[1] += 1
  elif state["player"]["orientation"] == "left":
    square[0] -= 1
  else:
    square[0] += 1
  # Get entity at adjacent square
  facing = getEntityAt(state, square[0], square[1])
  # If there isn't an entity
  if not facing:
    print("This square is unoccupied")
    return
  print("column: ", square[0], "\n")
  print("row: ", square[1])

  # Iterate through key value pairs to print stats
  for item, value in facing.items():
    print(item, value)


def eat(state):
  # Copy player square into a list
  square = list(state["playerSquare"])
  # Change col or row of square based on orientation to get adjacent square
  if state["player"]["orientation"] == "up":
    square[1] -= 1
  elif state["player"]["orientation"] == "down":
    square[1] += 1
  elif state["player"]["orientation"] == "left":
    square[0] -= 1
  else:
    square[0] += 1
  # Get entity at adjacent square
  facing = getEntityAt(state, square[0], square[1])
  # If there isn't an entity
  if not facing:
    return -1
  # If it's an herb, add agility to player and remove
  if facing["type"] == "herb":
    state["player"]["agility"] += facing["agility"]
    del state["others"][tuple(square)]
    return 1
  # If it's a bread, add strength to player and remove
  elif facing["type"] == "bread":
    state["player"]["strength"] += facing["strength"]
    del state["others"][tuple(square)]
    return 1
  # If it's a block
  else:
    return -2


def batter(state):
  # Copy player square into a list
  square = list(state["playerSquare"])
  # Change col or row of square based on orientation to get adjacent square
  if state["player"]["orientation"] == "up":
    square[1] -= 1
  elif state["player"]["orientation"] == "down":
    square[1] += 1
  elif state["player"]["orientation"] == "left":
    square[0] -= 1
  else:
    square[0] += 1
  # Get entity at adjacent square
  facing = getEntityAt(state, square[0], square[1])
  # If there isn't an entity
  if not facing:
    return -1
  # If it's not a block
  if facing["type"] != "block":
    return -2
  # If the height is 2 or less, remove it
  if facing["height"] <= 2:
    del state["others"][tuple(square)]
  # Otherwise lower the height of the block
  else:
    state["others"][tuple(square)]["height"] -= 2
  # Either way, reduce strength of the player
  state["player"]["strength"] -= 1
  return 1


def jump(state):
  # Copy player square into lists
  square = list(state["playerSquare"])
  farSquare = list(state["playerSquare"])
  # Change col or row of squares based on orientation to get adjacent and landing square
  if state["player"]["orientation"] == "up":
    square[1] -= 1
    farSquare[1] -= 2
  elif state["player"]["orientation"] == "down":
    square[1] += 1
    farSquare[1] += 2
  elif state["player"]["orientation"] == "left":
    square[0] -= 1
    farSquare[0] -= 2
  else:
    square[0] += 1
    farSquare[0] += 2
  # Get entity at adjacent and landing square
  facing = getEntityAt(state, square[0], square[1])
  landing = getEntityAt(state, farSquare[0], farSquare[1])
  # If there isn't an entity at the adjacent square
  if not facing:
    return -1
  # If there is an entity at the landing square
  if landing:
    return -2
  # If adjacent square is a block that is too high
  if facing["type"] == "block" and facing["height"] > 5:
    return -3
  # Otherwise, set player square to landing square and reduce agility
  state["playerSquare"] = tuple(farSquare)
  state["player"]["agility"] - 1
  return 1


def readState(file):
  state = {}
  with open(file) as f:
    for line in f.readlines():
      # Break each line into a list of values
      entity = line.strip().split(" ")
      # Call the appropriate function based on the entity type
      if entity[0] == "player":
        state = initialiseState(int(entity[1]), int(entity[2]), entity[5],
                                int(entity[3]), int(entity[4]))
      elif entity[0] == "herb":
        addHerb(state, int(entity[1]), int(entity[2]), int(entity[3]))
      elif entity[0] == "bread":
        addBread(state, int(entity[1]), int(entity[2]), int(entity[3]))
      elif entity[0] == "block":
        addBlock(state, int(entity[1]), int(entity[2]), int(entity[3]))
  return state


def playConsole(file):

  def playConsole(file):
    state = readState(file)
    while True:
      command = input("Next request> ")
      if command == "step":
        step(state)
      elif command[:4] == "turn":
        turn(state, command[5:])
      elif command == "show board":
        showBoard(state, 10, 3)
      elif command == "show player":
        showPlayer(state)
      elif command == "show facing":
        showFacing(state)
      elif command == "quit":
        exit()
      elif command == "jump":
        jump(state)
      elif command == "eat":
        eat(state)
      elif command == "batter":
        batter(state)


playConsole("state.txt")

if __name__ == "__main__":
  playConsole('example.txt')
