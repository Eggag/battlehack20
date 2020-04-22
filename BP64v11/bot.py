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

def sq(num):
    if(num < 0):
        return (-1 * num * num)
    return num * num

def run_pawn():
    global row, col
    global lstNum, curNum
    row, col = get_location()
    dlog('My location is: ' + str(row) + ' ' + str(col))
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
    if team == Team.WHITE:
        for i in range(-2, 2):
            for j in range(-1, 2):
                if(j != 0 and valid(row + i, col + j) == team): numBel += 1
    else:
        for i in range(-1, 3):
            for j in range(-1, 2):
                if(j != 0 and valid(row + i, col + j) == team): numBel += 1
    kms = False
    op = 0
    if(team == Team.WHITE): op = boardSize - 1 
    thr = 8
    if(row == (op - (2 * forward))): thr = 6
    if(row == (op - (forward))): thr = 6
    if((curNum - lstNum) > 40): thr = 6
    if(valid(row - forward, col) == team and (valid(row, col - 1) == team or valid(row, col + 1) == team) and numBel >= thr):
        kms = True
    if(((valid(row + 2 * forward, col + 1) != oppTeam) and (valid(row + 2 * forward, col - 1) != oppTeam)) or kms):
        if(valid(row + forward, col) == False):
            move_forward()
            lstNum = curNum

def tryPlace():
    score = [0 for i in range(boardSize)]
    if team == Team.WHITE:
        for i in range(boardSize):
            # we need the lowest black pawn
            pos = -1
            for j in range(boardSize):
                if(board[j][i] == oppTeam):
                    pos = j
                    break
            if(pos == -1):
                continue
            mi = 0
            th = 0
            if(i > 0):
                # find left
                for j in range(boardSize):
                    if(j >= pos):
                        if(board[i - 1][j] == oppTeam): th += 1
            if(i < (boardSize - 1)):
                # find right
                for j in range(boardSize):
                    if(j >= pos):
                        if(board[i + 1][j] == oppTeam): th += 1
            if(i > 0):
                for j in range(boardSize):
                    if(j <= pos):
                        if(board[i - 1][j] == team): mi += 1
            if(i < (boardSize - 1)):
                for j in range(boardSize):
                    if(j <= pos):
                        if(board[i + 1][j] == team): mi += 1
            dlog(str(pos))
            if(i > 0):
                num = (pos) ** 5
                num1 = (mi - th) ** 4
                score[i - 1] = 4 * (num + num1)
            num2 = (pos) ** 5
            num3 = (mi - th) ** 4
            score[i] = 3 * (num2 + num3)
            if(i < (boardSize - 1)):
                num = (pos) ** 5
                num1 = (mi - th) ** 4
                score[i + 1] = 4 * (num + num1)
    else:
        notyet = 1    
    mx = -1e9
    bst = -1
    for i in range(boardSize):
        dlog(str(score[i]))
        if(score[i] > mx and valid(spawnRow, i) == False):
            mx = score[i]
            bst = i
    dlog('Max score: ' + str(mx))
    if(bst != -1): spawn(spawnRow, bst)

def run_overlord():
    global board
    board = get_board()
    tryPlace()

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
