# this file will decide the game state valid moves and will also keep a move log
class GameState:
    def __init__(self):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "bp", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                      ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)    # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # changing turn

    '''
    Undo the Last Move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    Considering moves with checks in get_valid_moves()
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        
        return moves
    
    '''
    Lets get all the pawn moves for pawn located at (r,c) and add these moves to the list 
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # valid white pawn moves
            if self.board[r - 1][c] == '--':  # 1 Square advance available
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '--':
                    moves.append(Move((r, c), (r - 2, c), self.board))
                # print(c, r)
                if c - 1 >= 0:  # look for possible capture to left
                    if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if c + 1 <= 7:  # look for possible capture to right
                    print('insdie right', r, c)
                    if self.board[r-1][c + 1][0] == 'b':  # enemy piece to capture
                        print("appended to valid moves")
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
    '''
    Now Lets get all the Rook moves for Rook located at (r,c) and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        pass
class Move():

    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]   # it may or may  not be a captured piece
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol    #  kind of custom hash function
        # print(self.moveId)
    '''
    Overridding the equals method
    '''
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]

                   
