# disable debug when it is not needed
DEBUG = 1
def dlog(str):
    if DEBUG == 1:
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
lstNum = 0
curNum = 0
roundNum = 0

def run_pawn():
    global row, col
    global lstNum, curNum
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
    curNum += 1
    if valid(row + forward, col + 1) == oppTeam:
        capture(row + forward, col + 1)
        return
    if valid(row + forward, col - 1) == oppTeam:
        capture(row + forward, col - 1)
        return
    numBel = 0
    # need to have more below for a successful attack
    if team == Team.WHITE:
        for i in range(-2, 2):
            for j in range(-1, 2):
                if(j != 0):
                    if(valid(row + i, col + j) == team): numBel += 1
    else:
        for i in range(-1, 3):
            for j in range(-1, 2):
                if(j != 0):
                    if(valid(row + i, col + j) == team): numBel += 1
    gd = True
    if(team == Team.WHITE):
        if(row >= 10): gd = False
    else:
        if(row <= 6): gd = False
    kms = False
    op = 0
    if(team == Team.WHITE): op = boardSize - 1
    thr = 6
    if(team == Team.WHITE):
        if(row >= 8): thr = 7
    else:
        if(row <= 7): thr = 7
    if(valid(row - forward, col) == team and (valid(row, col - 1) == team and valid(row, col + 1) == team) and numBel >= thr and gd):
        kms = True
    if(((valid(row + 2 * forward, col + 1) != oppTeam) and (valid(row + 2 * forward, col - 1) != oppTeam)) or kms):
        if(valid(row + forward, col) == False):
            move_forward()
            lstNum = curNum

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
                            if board[k][j - 1] == oppTeam:
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
                                if board[k][j + 1] == oppTeam:
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
                            if board[k][j - 1] == oppTeam:
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
                                if board[k][j + 1] == oppTeam:
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
    # endpoints are of higher priority
    # don't ask...
    # pos = [9, 1, 15, 3, 13, 5, 11, 7]
    pos = [9, 1, 15, 7, 11, 2, 13, 5, 0, 14, 2, 12, 4, 10, 6, 8]
    # pos = [1, 3, 2, 15, 4, 14, 5, 13, 6, 12, 7, 11, 8, 12, 16]
    # pos = [0, 2, 1, 15, 3, 14, 4, 13, 5, 12, 6, 11, 7, 10, 8, 14]
    # pos = [0, 2, 1, 15, 3, 5, 4, 14, 6, 8, 7, 13, 9, 11, 10, 12]
    for i in pos:
        f = True
        for j in range(boardSize):
            if(board[j][i] == team):
                f = False
                break
        if f:
            spawn(spawnRow, i)
            return
    op = 0
    if(team == Team.WHITE): op = boardSize - 1 
    for i in pos:
        if(board[op][i] == team):
            f1 = True
            for j in range(boardSize):
                if((j != op) and (board[j][i] == team or board[j][i] == oppTeam)):
                    f1 = False
                    break
            if f1:
                spawn(spawnRow, i)
                return
    best = -1
    mn = 1e9
    for i in range(boardSize):
        cur = 0
        for j in range(boardSize):
            if board[j][i] == team:
                cur += 1
        if(cur < mn and valid(spawnRow, i) == False and board[op][i] != team):
            mn = cur
            best = i
    if best != -1: spawn(spawnRow, best)

def run_overlord():
    global board
    global roundNum
    board = get_board()
    if roundNum >= 15 and tryDefend():
        return
    tryAttack()
    roundNum += 1

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
