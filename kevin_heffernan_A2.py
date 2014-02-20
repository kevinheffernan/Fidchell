# =============== #
# kevin heffernan #
# id: 11277955    #
# =============== #

import re,random,itertools

def getInitialBoard():
    boardState=[list(r) for r in ['* AAA *',' '*7,'A DDD A','A DKD A','A DDD A',' '*7,'* AAA *']]
    return (boardState)

def printBoard(boardState,p):
    boardGui='  '+' {:^3}'*7+'\n  '+'-'*29+'\n'+''.join((str(8-i)+' '+'|{:^3}'*7\
    +'| '+str(8-i)+'\n  ')+'-'*29+'\n' for i in range(1,8))+'  '+' {:^3}'*7
    cols=['a','b','c','d','e','f','g']
    print '\n'+boardGui.format(*cols+[e for r in boardState for e in r]+cols)
    print '\n'+' '*6+"player to move: %s\n" % (p)
    return (None)

def printBoards(board1,board2,move,player):
    print '\n'+' '*8+"board before move"+' '*16+' '*10+'board after move'
    mve=chr(move[0][1]+97)+str(move[0][0]*-1)+'-'+chr(move[1][1]+97)+str(move[1][0]*-1)
    boardGui='  '+' {:^3}'*7+' '*5+' '*9+' {:^3}'*7+'\n '+'-'*29+' '*14+'-'*29+'\n'+''.join((str(8-i)+\
    ' '+'|{:^3}'*7+'| '+str(8-i)+'  ---->  '+str(8-i)+' '+'|{:^3}'*7+'| '+str(8-i)+'\n  ')+'-'*    29+\
    ' '*13+'-'*29+'\n' for i in range(1,8))+'  '+' {:^3}'*7+' '*14+' {:^3}'*7
    cols=['a','b','c','d','e','f','g']
    jointBoard = [board1[i]+board2[i] for i in range(0,7)]
    print '\n'+boardGui.format(*cols+cols+[e for r in jointBoard for e in r]+cols+cols)+'\n'
    print " "*27 + "%s's move: (%s)" % (player,mve)
    return (None)

def getMoveHuman(comment):
    move=raw_input("%s" % comment).lower()
    # validate format of user input to suit board size
    while re.match('^[a-g][1-7]-[a-g][1-7]$',move)==None: 
        move=raw_input("invalid input, re-enter move: ").lower()
    return (((-1*int(move[1]),ord(move[0])-97),(-1*int(move[4]),ord(move[3])-97)))

def getAvailablePieces(board,p):
    if p=='light': return [(a,b) for a in range(-7,0) for b in range(0,7) if board[a][b]=='A']
    else: return [(a,b) for a in range(-7,0) for b in range(0,7) if board[a][b] in ['K','D']]

def getAttackerDefenderMoves(board,position):
    (a,b)=(position[0],position[1])
    # check all horizontal and vertical possibilities (stopping if encountering piece along path)
    posMov=list(breakLoop() if board[r][b]!=' ' else (r,b) for r in range((a-1 if a!=-7 else a),-8,-1))+\
           list(breakLoop() if board[r][b]!=' ' else (r,b) for r in range(a+1,0))+\
           list(breakLoop() if board[a][c]!=' ' else (a,c) for c in range((b-1 if b!=0 else b),-1,-1))+\
           list(breakLoop() if board[a][c]!=' ' else (a,c) for c in range(b+1,7))
    return (posMov)

def getKingMoves(z,position):
    (a,b,D)=(position[0],position[1],[' ','*'])
    # if king on left/right edge
    if b in [0,6]:
        posMov=list(breakLoop() if z[r][b] not in D else (r,b) for r in range((a-1 if a!=-7 else a),-8,-1))+\
        list(breakLoop() if z[r][b] not in D else (r,b) for r in range(a+1,0))+([(a,b)] if z[a][b+1 if b==0 else b-1] in D else [])+\
        ([(a+1 if a!=-1 else a,b+1 if b==0 else b-1)] if z[a+1 if a!=-1 else a][b+1 if b==0 else b-1] in D else [])+\
        ([(a-1 if a!=-7 else a,b+1 if b==0 else b-1)] if z[a-1 if a!=-7 else a][b+1 if b==0 else b-1] in D else [])
    # else if king is on top/bottom edge
    elif a in [-7,-1]:
        posMov=list(breakLoop() if z[a][c] not in D else (a,c) for c in range((b-1 if b!=0 else b),-1,-1))+\
        list(breakLoop() if z[a][c] not in D else (a,c) for c in range(b+1,7))+([(a,b)] if z[a+1 if a==-7 else a-1][b] in D else [])+\
        ([(a+1 if a==-7 else a-1,b+1 if b!=6 else b)] if z[a+1 if a==-7 else a-1][b+1 if b!=6 else b] in D else [])+\
        ([(a+1 if a==-7 else a-1,b-1 if b!=0 else b)] if z[a+1 if a==-7 else a-1][b-1 if b!=0 else b] in D else [])
    else:
        # else if king is not on edge
        posMov=([(a+1,b)] if z[a+1][b] in D else [])+([(a-1,b)] if z[a-1][b] in D else [])+([(a,b+1)] if z[a][b+1] in D else [])+\
        ([(a,b-1)] if z[a][b-1] in D else [])+([(a+1,b-1)] if z[a+1][b-1] in D else [])+([(a+1,b+1)] if z[a+1][b+1] in D else [])+\
        ([(a-1,b-1)] if z[a-1][b-1] in D else [])+([(a-1,b+1)] if z[a-1][b+1] in D else [])
    return (posMov)

def getPossibleMoves(board,position):
    (a,b)=(position[0],position[1])
    # first check if there was a suicide leaving a blank space
    if board[a][b]== ' ': 
        return ([])
    # if not suicide, get all possible moves for that position
    if board[a][b] in ['A','D']: 
        posMov=getAttackerDefenderMoves(board,position)
    elif board[a][b] == 'K': 
        posMov=getKingMoves(board,position)
    return ([move for move in posMov if move!=position])

def getMoveComputer(board,player,height,tpsnData,prnt):
    availablePieces,results=getAvailablePieces(board,player),[]
    # find all pieces for player and all moves of those pieces, select piece and move with highest value
    for (piece,move) in getAllPossibleMoves(board,player):
        # need to update board before sending to alpha beta
        (newBoard,gameOver,captures)=makeMove([list(e) for e in board],(piece,move))
        if prnt: print '='*50+'\nnew alpha-beta on position: %s, move: %s\n' % (str(piece),str(move)) + '='*50
        results.append((piece,move,alphaBeta(newBoard,height,float('-inf'),float('inf'),0,move,player,0,tpsnData,prnt,captures,0)))
    choice = sorted(results,key=lambda x: -x[2][1])[0]
    (move,numEvl,val,numNodes)=((choice[0],choice[1]),sum([r[2][0] for r in results]),choice[2][1],sum([r[2][2] for r in results]))
    return (move,numEvl,val,numNodes)

def legalMove(board,move,player):
    (a,b,c,d)=(move[0][0],move[0][1],move[1][0],move[1][1])
    # if player tried to make a 'null' move or move empty space
    if ((a,b)==(c,d) or board[a][b] in [' ','*']): return (False)
    # if not K and ending up on capture square (*)
    if board[c][d]=='*' and board[a][b]!='K': return (False)
    # if player tried to move opponent's piece
    if player=='light' and board[a][b] in ['K','D']: return (False)
    elif player=='dark' and board[a][b]=='A': return (False)
    # if moved in a diagonal and not 'K'
    if (c!=a and d!=b) and board[a][b]!='K': return (False)
    # if K moved more than one space and not on edge (or if on edge, doesn't end up on same edge)
    if max(c-a if a<c else 0 if a==c else a-c,d-b if b<d else 0 if d==b else b-d) > 1 and \
       board[a][b]=='K' and not ((a,c) in [(-1,-1),(-7,-7)] or (b,d) in [(0,0),(6,6)]): \
       return (False)
    # if player tried to skip another piece
    (x,y)=(a,b)
    while (x+y != c+d):
        (x,y) = x+1 if x < c else x if x==c else x-1,y+1 if y < d else y if y==d else y-1
        if (board[a][b]=='K' and board[x][y] not in ['*',' ']) or (board[a][b] != 'K' and board[x][y]!=' '): \
            return (False)
    return (True)

def checkForCaptures(z,move):
    # note: last check will be for suicide
    (D,A,a,b,piece)=(['K','D','*'],['A','*'],move[1][0],move[1][1],z[move[1][0]][move[1][1]])
    c1=[(r,l) for r in [-7,-1] for l in range(1,6) if (z[r][l]=='K' and z[r+1 if r==-7 else r-1][l] in A and \
       z[r][l-1] in A and z[r][l+1] in A) or (z[r+1 if r==-7 else r-1][l] in (D if z[r][l]=='A' else A) and z[r][l]!='K')\
       or (z[r][l+1] in (D if z[r][l]=='A' else A) and z[r][l-1] in (D if z[r][l]=='A' else A) and z[r][l]!='K')]
    # check for flanking on left-most and right-most columns
    c2=[(r,l) for l in [0,6] for r in range(-6,-1) if (z[r][l]=='K' and z[r][l+1 if l==0 else l-1] in A and z[r+1][l] in A \
       and z[r-1][l] in A) or (z[r][l+1 if l==0 else l-1] in (D if z[r][l]=='A' else A) and z[r][l]!='K')\
       or (z[r+1][l] in (D if z[r][l]=='A' else A) and z[r-1][l] in (D if z[r][l]=='A' else A) and z[r][l]!='K')]
    # check inner board for flanking
    c3=[(r,l) for r in range(-6,-1) for l in range(1,6) if (z[r][l]=='K' and z[r+1][l] in A and z[r-1][l] in A \
       and z[r][l+1] in A and z[r][l-1] in A) or (z[r+1][l] in (D if z[r][l]=='A' else A) and z[r-1][l] in (D if z[r][l]=='A' else A)\
       and z[r][l]!='K') or (z[r][l+1] in (D if z[r][l]=='A' else A) and z[r][l-1] in (D if z[r][l]=='A' else A) and z[r][l]!='K')]
    captures=[(x,z[x[0]][x[1]]) for x in c1+c2+c3 if z[x[0]][x[1]] not in [' ','*']]
    return (captures)

def makeMove(board,move):
    (a,b,c,d)=(move[0][0],move[0][1],move[1][0],move[1][1])
    # make move and update board (when king moves, '*' denotes high king square)
    (board[c][d],board[a][b])=(board[a][b],' ' if (a,b)!=(-4,3) else '*')
    # check for captured pieces
    captures=checkForCaptures(board,move)
    # if the king ends up on capture square (which isn't High King square) game is over
    if board[c][d]=='K' and (c,d) in [(-7,0),(-1,0),(-7,6),(-1,6)]: return (board,True,captures)
    for capture,piece in captures:
        # if king was captured game is over
        if piece=='K': return (board,True,captures)
        # else take captured pieces off the board
        else: board[capture[0]][capture[1]]=' '
    return (board,False,captures)

def takeMovesBack(history,tpsn):
    m,x=int(raw_input('# moves back? (%s max): '%str(len(history)/2))),1
    while m > len(history)/2: 
        print 'error: too many moves back'
        m=int(raw_input('# moves back? (%s max): '%str(len(history)/2)))
    for e in range(1,m): x+=2
    for i in range(0,x): history.pop()
    # return zobrist key at stage the board was saved at
    if tpsn: return ([list(e) for e in history[-1][0]],history[-1][1],history)
    else: return ([list(e) for e in history[-1][0]],history)    

def breakLoop(): raise StopIteration

def getDistKingFromCorner(board):
    # find where king is on board
    king=[(x,y) for x in range(-7,0) for y in range(0,7) if board[x][y]=='K'][0]
    dist=[]
    # check top left corner (first if statement checks if diagonal to corner)
    if king[0]+7==king[1]: dist.append(((-7,0),king[1]))
    else: dist.append(((-7,0),king[1]+king[0]+7))
    # check top right corner
    if king[0]-1-1==king[1]: dist.append(((-7,6),6-king[1]))
    else: dist.append(((-7,6),6-king[1]+king[0]+7))
    # check bottom left corner
    if king[0]-1-1==king[1]: dist.append(((-1,0),king[1]))
    else: dist.append(((-1,0),king[1]+-1-king[0]))
    # check bottom right corner
    if king[0]-1-1==king[1]: dist.append(((-1,6),6-king[1]))
    else: dist.append(((-1,6),6-king[1]-1-king[0]))
    # return minimum distance and closest corner
    return (king,sorted(dist,key=lambda x: x[1])[0])

def staticEvaluation(z,position,posMoves,player,captures):
    # check for game over by king being captured 
    if 'K' in [piece for (position,piece) in captures]: return 1000000 if player=='light' else -1000000
    # how far is king from each corner (ignoring skipping pieces, just distance)
    (king,(closestCorner,distKingFromCorner))=getDistKingFromCorner(z)
    # check for game over by king reaching a corner 
    if distKingFromCorner==0: return 1000000 if player=='dark' else -1000000
    # get mobility
    mobility=len(getAllPossibleMoves(board,player))
    # number of defenders/attackers on board
    numDef=len([(x,y) for x in range(-7,0) for y in range(0,7) if z[x][y]=='D'])
    numAtt=len([(x,y) for x in range(-7,0) for y in range(0,7) if z[x][y]=='A'])
    (numDefCapt,numAttCapt)=(0,0)
    # if king has no pieces in way to closest corner
    distanceClear=0
    (x,y),(c,d)=king,(closestCorner[0],closestCorner[1])
    while (x+y != c+d):
        (x,y) = x+1 if x < c else x if x==c else x-1,y+1 if y < d else y if y==d else y-1
        if board[x][y] not in ['*',' ']: distanceClear+=1
    # find number of captured attackers and defenders as result of move
    for (position,piece) in captures: 
        if piece=='A': numAttCapt+=1
        else: numDefCapt+=1
    attributes = [distKingFromCorner,distanceClear,mobility,numDef,numAtt,numDefCapt,numAttCapt]
    # weights used to multiply evaluation attributes
    if player=='light':
        weights=[-500,-1000,10,-1,1,200,-100]
    else:
        weights=[500,1000,10,1,-1,-100,200]
    value=0
    for i,w in enumerate(weights):
        if i < 2: value += (w / (1 if attributes[i]==0 else attributes[i]))
        else: value += w * attributes[i]
    return (value)

# show that pruning has taken place
def printPruned(l,p):
    if p==False: return (None)
    print ('\t'*l+"="*14+'\n'+"\t"*l+"*** PRUNED ***\n"+"\t"*l+"="*14)
    return (None)

# generate intial zobrist key and bitArray : will then initially XOR all numbers to get initial key
def initializeZobrist(board,pieces):
    # generate a 3D array (7 x 7 x 3) with random 16 bit numbers (don't need 64 bit, 16 is enough)
    bitTable = [[[random.getrandbits(16) for a in range(3)] for b in range(7)] for c in range(7)]
    zobristKey=0
    for (a,b,c) in itertools.product(*map(xrange,(7,7,3))):
        zobristKey ^= bitTable[a][b][c]
    return (bitTable,zobristKey)

def updateZobrist(board,move,zobristKey,bitTable,pieces,captures):
    (a,b,c,d)=(move[0][0],move[0][1],move[1][0],move[1][1])
    # random number to reflect whose viewpoint the board is viewed from
    fixedamountforchangeofplayer=3
    # get array values of squares moved to / from
    # note: board has already changed so working backwards
    posA=bitTable[a][b][pieces.index(board[a][b])]
    posB=bitTable[c][d][pieces.index(board[a][b])]
    # get values of captures (if any) else 0
    capt=0
    if captures !=[]:
        for c,p in captures:
            capt ^= bitTable[c[0]][c[1]][pieces.index(p)]
    zobristNew=(zobristKey ^ posA ^ posB ^ capt ^ fixedamountforchangeofplayer)
    return (zobristNew)

def getAllPossibleMoves(board,player):
    availablePieces=getAvailablePieces(board,player)
    possibleMoves=[]
    for piece in availablePieces:
        for move in getPossibleMoves(board,piece):
            possibleMoves.append((piece,move))
    return (possibleMoves)

def alphaBeta(board,ht,achv,hope,l,position,player,evalCount,tpsnData,prnt,capt,nodes):
    global tpsnTbl
    if tpsnData: (pieces,bitTable,zobristKey)=tpsnData[0],tpsnData[1],tpsnData[2]
    posMoves=getPossibleMoves(board,position)
    temp=0.0
    if ht > 0 and posMoves!=[]:
        printABNode(ht,achv,hope,(float('-inf') if ht%2==0 else float('inf')),l,prnt,'search')
    # if no possible moves or have reached bottom of search, static evaluation
    if ht==0 or posMoves==[]:
        value = staticEvaluation(board,position,posMoves,player,capt)
        printABNode(ht,achv,hope,value,l,prnt,'static')
        return (evalCount+1,value,nodes)
    for move in posMoves:
        (boardNew,gameOver,captures)=makeMove([list(e) for e in board],(position,move))
        # if user selected the use of a transposition table generate new hash key
        if tpsnData:
            newKey=updateZobrist(board,(position,move),zobristKey,bitTable,pieces,captures)
            if newKey in tpsnTbl and 'depth' in tpsnTbl[newKey]:
                # if depth associated with key is greater than current, use stored value. else replace with alpha beta value
                if tpsnTbl[newKey]['depth'] >= ht:
                    (temp)=(tpsnTbl[newKey]['value'])
                    if prnt: print ('\t'*(l+1)+"="*38+'\n'+"\t"*(l+1)+"*** ALREADY IN TRANSPOSITION TABLE ***\n"+"\t"*(l+1)+"="*38)
                else:
                    (evalCount,temp,nodes)=alphaBeta(boardNew,ht-1,-hope,-achv,l+1,move,'light' if player=='dark' else 'dark',evalCount,tpsnData,prnt,captures,nodes+1)
                    (tpsnTbl[newKey]['depth'],tpsnTbl[newKey]['value'])=(ht,temp)
            else: 
                tpsnTbl[newKey]={}
                (evalCount,temp,nodes)=alphaBeta(boardNew,ht-1,-hope,-achv,l+1,move,'light' if player=='dark' else 'dark',evalCount,tpsnData,prnt,captures,nodes+1)
                (tpsnTbl[newKey]['depth'],tpsnTbl[newKey]['value'])=(ht,temp)
        else: (evalCount,temp,nodes)=alphaBeta(boardNew,ht-1,-hope,-achv,l+1,move,player,evalCount,tpsnData,prnt,captures,nodes+1)
        temp *= -1
        achv=max(temp,achv)
        printABNode(ht,achv,hope,achv,l,prnt,'search')
        if temp>=hope: printPruned(l,prnt); return (evalCount,temp,nodes)
    return (evalCount,achv,nodes)

# print alpha beta node
def printABNode(h,a,b,v,l,prnt,m):
    if prnt==False: return (None)
    (i,border)=("\t"*l,"-"*14)
    print "%s\n%sa: %s b: %s\n%svalue: %s\n%smethod: %s\n%s" % (i+border,i,a,b,i,v,i,m,i+border)
    return (None)

def getInitialParameters():
    print '\n'+' '*7+'game initial parameters'+'\n'+'='*37
    humanPlayer=raw_input('--> what side? (light/dark): ').lower()
    ht=int(raw_input('--> height to search alpha-beta: '))
    t=True if raw_input('--> transposition table? (y/n): ').lower()=='y' else False
    prnt=True if raw_input('--> enable alpha-beta printing? (y/n): ').lower()=='y' else False
    print '='*37
    return (humanPlayer,ht,t,prnt)

def printResult(count,result,nodes):
    print "----------------------------------------"
    print "total nodes visited: ",nodes
    print "total static evaluations performed: ",count
    print "----------------------------------------"
    return (None)

# initialize hash table for transpositions
(tpsnTbl,pieces)=({},['A','D','K'])
# get game parameters from user
(humanPlayer,height,tpsn,prnt)=getInitialParameters()
# set up initial board and initial parameters
(board,player,gameOver,history)=(getInitialBoard(),'light',False,[])
# if player requested transposition table, set it up
if tpsn: (bitTable,zobristKey)=initializeZobrist(board,pieces)
# set up history for allowing user to take back moves, storing board state and zobrist key (if applicable)
history.append(([list(e) for e in board],None if not tpsn else zobristKey))

while not gameOver:
    printBoard(board,player)
    if humanPlayer==player: move=getMoveHuman("--> enter move: ")
    else:
        (move,numEvl,val,nodes)=getMoveComputer(board,player,height,None if not tpsn else (pieces,bitTable,zobristKey),prnt)
        printResult(numEvl,val,nodes)
    while not legalMove(board,move,player): move=getMoveHuman("--> illegal move, re-enter move: ")
    (boardNew,gameOver,captures)=makeMove([list(e) for e in board],move)
    # if transposition table is used, update the zobrist key to reflect board state of 'real' moves
    if tpsn: zobristKey=updateZobrist(board,move,zobristKey,bitTable,pieces,captures)
    # update board
    board=boardNew
    # add to stack of board states for user move takeback
    history.append(([list(e) for e in board],None if not tpsn else zobristKey))
    printBoards(history[-2][0],history[-1][0],move,player)
    if humanPlayer==player:
        if raw_input('take back move? (y/n): ')=='y':
            if tpsn: (board,history,zobristKey)=takeMovesBack(history,tpsn)
            else: (board,history)=takeMovesBack(history,tpsn)
            # next line will call change of player
            player='dark' if player=='light' else 'light'
    player='dark' if player=='light' else 'light'
    if gameOver: print 'Game Over: %s wins' % ('dark' if player=='light' else 'light')
        
