# disable debug when it is not needed
DEBUG = 0
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
    global lstNum, curNum, numCyc
    global thr
    row, col = get_location()
    if(team == Team.BLACK and row == 0): return
    if(team == Team.WHITE and row == boardSize - 1): return
    forward = 1
    if team == Team.BLACK: forward = -1
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
        for i in range(-2, 1):
            for j in range(-1, 2):
                if j != 0:
                    if(valid(row + i, col + j) == team): numBel += 1
    else:
        for i in range(0, 3):
            for j in range(-1, 2):
                if j != 0:
                    if(valid(row + i, col + j) == team): numBel += 1
    kms = False
    # try to use our row advantage by accumulating pawns by attacking less frequently
    thr = 0
    if(team == Team.BLACK):
        if(row <= 8): thr = 40
    else:
        if(row >= 7): thr = 40
    tr = 5
    if(team == Team.BLACK):
        if(row <= 7): tr = 6
        if(row >= 10): tr = 4
    else:
        if(row >= 8): tr = 6
        if(row <= 6): tr = 4
    if(valid(row - forward, col) == team and (valid(row, col - 1) == team and valid(row, col + 1) == team) and (curNum - lstNum) >= thr and numBel >= tr):
        kms = True
    if(((valid(row + 2 * forward, col + 1) != oppTeam) and (valid(row + 2 * forward, col - 1) != oppTeam)) or kms):
        if(valid(row + forward, col) == False):
            move_forward()
            lstNum = curNum

def tryInit():
    pos = [1, 4, 7, 10, 13, 15]
    spawn(spawnRow, pos[roundNum - 1])

def score(i):
    # calculates the score of the current column
    # use this to assign rows to values
    num = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 7, 8, 20, 30, 40, 50, 60, 0]
    forward = 1
    if team == Team.BLACK: forward = -1
    sc = 0
    if(i > 0):
        if(valid(spawnRow + forward, i - 1) == oppTeam):
            # very bad: we will be captured immeiately
            sc -= 1000
    if(i < (boardSize - 1)):
        if(valid(spawnRow + forward, i + 1) == oppTeam):
            # same as above but for another row
            sc -= 1000
    # take into account how many we already have (both in neighbouring rows and our row
    tot = 0
    for j in range(boardSize):
        if(board[j][i] == team): tot += 1
    # try to get more here if we have not a lot of teammates here
    need = [100, 70, 50, 30, 20, 15, 10, 7, 5, 2, 1, 1, 0, 0, 0, 0, 0]
    sc += 5 * need[tot]
    for j in range(boardSize):
        if(board[j][i] == oppTeam):
            sc += 0.2 * num[15 - abs(j - spawnRow)]
    if(i > 0):
        for j in range(boardSize):
            if(board[j][i - 1] == oppTeam):
                sc += 3 * num[15 - abs(j - spawnRow)]
    if(i < (boardSize - 1)):
        for j in range(boardSize):
            if(board[j][i + 1] == oppTeam):
                sc += 3 * num[15 - abs(j - spawnRow)]
    return sc
    

def trySpawn():
    mx = -10000
    bst = -1
    for i in range(boardSize):
        cur = score(i)
        if(cur > mx and valid(spawnRow, i) == False):
            mx = cur
            bst = i
    if(bst != -1): spawn(spawnRow, bst)


def run_overlord():
    global board
    global roundNum
    roundNum += 1
    board = get_board()
    if roundNum <= 6:
        tryInit()
    else: 
        trySpawn()

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
