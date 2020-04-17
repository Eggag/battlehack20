import random

# disable debug when it is not needed
DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

# checks if it is a valid cell
def valid(r, c):
    global boardSize
    if r < 0 or c < 0 or c >= boardSize or r >= boardSize:
        return False
    try:
        return check_space(r, c)
    except:
        return None

def log_bytecode():
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

# declare variables here
row = None
col = None
board = None
boardSize = None
team = None
oppTeam = None
spawnRow = 0

# work on it later, will depend on what the strategy for the overlord is
def run_pawn():
    global row, col
    row, col = get_location()
    dlog('My location is: ' + str(row) + ' ' + str(col))
    if(team == Team.BLACK and row == 0): return
    if(team == Team.WHITE and row == boardSize - 1): return
    forward = 1
    if team == Team.BLACK: forward = -1
    # check if we can attack someone
    # if we can't, try to move, but check if we will get attacked there
    # this is very simple
    # in reality, we need to do some sort of check
    # which side we should go to, but that is for later...
    if valid(row + forward, col + 1) == oppTeam:
        capture(row + forward, col + 1)
        return
    if valid(row + forward, col - 1) == oppTeam:
        capture(row + forward, col - 1)
        return
    if((valid(row + 2 * forward, col + 1) != oppTeam) and (valid(row + 2 * forward, col - 1) != oppTeam)):
        if(valid(row + forward, col) == False): move_forward()

"""
Strategy for the overlord
- prioritize defence, but only monitor starting from row ~13 to avoid not attacking
- empty cols should have higher value
- empty cols near 'filled by us' cols are even better
- check before sending an attacker
- might be too defensive, but we'll see
"""

def tryDefend():
    bestX = -100
    bestY = -100
    if team == Team.WHITE:
        bestX = 100
        bestY = 100
    if team == Team.BLACK:
        for i in range(3, boardSize - 1):
            for j in range(boardSize):
                if board[i][j] == oppTeam:
                    if j > 0:
                        # this can be improved (I think)
                        f = True
                        for k in range(i + 1, boardSize):
                            if board[k][j - 1] == team:
                                f = False
                        if f:
                            if(((j == 1) or ((j - 1) > 0 and board[boardSize - 1][j - 2] != oppTeam)) and (board[boardSize - 1][j] != oppTeam)):
                                if(i > bestX):
                                    bestX = i
                                    bestY = j - 1
                    if j < (boardSize - 1):
                            f = True
                            for k in range(i + 1, boardSize):
                               if board[k][j + 1] == team:
                                    f = False
                            if f:
                                if((board[boardSize - 1][j] != oppTeam) and (((j + 2) < boardSize and board[boardSize - 1][j + 2] != oppTeam) or (j + 2 >= boardSize))):
                                    if(i > bestX):
                                        bestX = i
                                        bestY = j + 1
    else:
        for i in range(1, boardSize - 3):
            for j in range(boardSize):
                if board[i][j] == oppTeam:
                    if j > 0:
                        f = True
                        for k in range(i - 1, -1, -1):
                            if board[k][j - 1] == team:
                                f = False
                        if f:
                            if(((j - 1) > 0 and board[boardSize - 1][j - 2] != oppTeam) and (board[boardSize - 1][j] != oppTeam)):
                                if(i < bestX):
                                    bestX = i
                                    bestY = j - 1
                    if j < (boardSize - 1):
                            f = True
                            for k in range(i - 1, -1, -1):
                                if board[k][j + 1] == team:
                                    f = False
                            if f:
                                if((board[boardSize - 1][j] != oppTeam) and ((j + 2) < boardSize and board[boardSize - 1][j + 2] != oppTeam)):
                                    if(i < bestX):
                                        bestX = i
                                        bestY = j + 1
    if(bestX != 100 and bestX != -100):
        spawn(spawnRow, bestY)
        return True
    return False

def tryAttack():
    # time to do some attacking!
    attack = True

def run_overlord():
    global board
    board = get_board()
    if tryDefend(): return
    tryAttack()

def turn():
    # random stuff
    global boardSize, team, oppTeam, robotType, spawnRow
    dlog('Starting Turn!')
    boardSize = get_board_size()

    team = get_team()
    oppTeam = Team.WHITE if team == Team.BLACK else team.BLACK
    if team == Team.BLACK:
        spawnRow = boardSize - 1;

    dlog('Team: ' + str(team))

    robotType = get_type()
    dlog('Type: ' + str(robotType))

    if robotType == RobotType.PAWN:
        run_pawn()
    else:
        run_overlord()
    log_bytecode()
