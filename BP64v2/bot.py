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
                if j != 0:
                    if(valid(row + i, col + j) == team): numBel += 1
    else:
        for i in range(-1, 3):
            for j in range(-1, 2):
                if j != 0:
                    if(valid(row + i, col + j) == team): numBel += 1
    kms = False
    op = 0
    if(team == Team.WHITE): op = boardSize - 1 
    thr = 7
    if(row == (op - (2 * forward))): thr = 6
    if(row == (op - (forward))): thr = 6
    if((curNum - lstNum) > 150): thr = 6
    if(valid(row - forward, col) == team and (valid(row, col - 1) == team and valid(row, col + 1) == team) and numBel >= thr):
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
        for i in range(boardSize - 1):
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
        for i in range(1, boardSize):
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
    else:
        mn1 = 1e9
        bst1 = -1
        nm1 = 1e9
        mx1 = -1e9
        bst2 = -1
        nm2 = 1e9
        for i in range(boardSize):
            mn = 1e9
            mx = -1e9
            nm = 0
            for j in range(boardSize):
                if(oppTeam == board[j][i]):
                    if(j < mn): mn = j
                    if(j > mx): mx = j
                if(team == board[j][i]):
                    nm += 1
            if(valid(spawnRow, i) == False and nm < 4):
                if(mn < mn1):
                    bst1 = i
                    mn1 = mn
                    nm1 = nm
                elif(mn == mn1):
                    if(nm < nm1):
                        bst1 = i
                        nm1 = nm
                if(mx > mx1):
                    bst2 = i
                    mx1 = mx
                    nm2 = nm
                elif(mx == mx1):
                    if(nm < nm2):
                        bst2 = i
                        nm2 = nm
        if team == Team.WHITE:
            if(bst1 != -1 and mn1 <= 6):
                spawn(spawnRow, bst1)
                return True
        else:
            if(bst2 != -1 and mx1 >= 9):
                spawn(spawnRow, bst2)
                return True
    return False

def tryAttack():
    # endpoints are of higher priority
    pos = []
    pos.append(0)
    pos.append(15)
    for i in range(1, 15): pos.append(i)
    # process them in the order of importance
    for i in pos:
        f = True
        for j in range(boardSize):
            if(board[j][i] == team or board[j][i] == oppTeam):
                f = False
                break
        if f:
            spawn(spawnRow, i)
            return
    # try to put it into a row we 'have'
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
    # just pick the one with the least of ours?
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
    board = get_board()
    if tryDefend():
        return
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
