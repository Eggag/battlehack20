import random

# disable debug when it is not needed
DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

# checks if it is a valid cell
def valid(r, c):
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None

def log_bytecode():
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

# declare variables here
boardSize = None
team = None
oppTeam = None
spawnRow = 0

# work on it later, will depend on what the strategy for the overlord is
def run_pawn():
    row, col = get_location()
    dlog('My location is: ' + str(row) + ' ' + str(col))
    
"""
Strategy for the overlord

"""
def run_overlord():
    row, col = get_location()
    dlog('My location is: ' + str(row) + ' ' + str(col))

def turn():
    # random stuff
    dlog('Starting Turn!')
    boardSize = get_board_size()

    team = get_team()
    oppTeam = Team.WHITE if team == Team.BLACK else team.BLACK
    if team == Team.WHITE:
        spawnRow = 16;

    dlog('Team: ' + str(team))

    robotType = get_type()
    dlog('Type: ' + str(robotType))

    if robottype == RobotType.PAWN:
        run_pawn()
    else:
        run_overlord()
    log_bytecode()
