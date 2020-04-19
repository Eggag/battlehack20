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

def run_pawn():
    global row, col
    row, col = get_location()
    dlog('My location is: ' + str(row) + ' ' + str(col))
    if(team == Team.BLACK and row == 0): return
    if(team == Team.WHITE and row == boardSize - 1): return
    forward = 1
    if team == Team.BLACK: forward = -1
    if valid(row + forward, col + 1) == oppTeam:
        capture(row + forward, col + 1)
        return
    if valid(row + forward, col - 1) == oppTeam:
        capture(row + forward, col - 1)
        return
    kms = False
    if(valid(row - (2 * forward), col) == team and valid(row - forward, col) == team and (valid(row, col - 1) == team or valid(row, col + 1) == team)):
        kms = True
    if(((valid(row + 2 * forward, col + 1) != oppTeam) and (valid(row + 2 * forward, col - 1) != oppTeam)) or kms):
        if(valid(row + forward, col) == False):
            move_forward()

def tryAttack():
    # try to put it into a row we 'have'
    op = 0
    if(team == Team.WHITE): op = boardSize - 1 
    for i in range(boardSize):
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
    for i in range(9):
        if(board[op][i] != team): # counter CC
            cur = 0
            for j in range(boardSize):
                if board[j][i] == team:
                    cur += 1
            if(cur < mn and valid(spawnRow, i) == False):
                mn = cur
                best = i
    if best != -1: spawn(spawnRow, best)

def run_overlord():
    global board
    board = get_board()
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
