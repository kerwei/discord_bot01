from PIL import Image

class Manager:
    def __init__(self) -> None:
        self.board = [[ 0 , 0 , 0 ], 
                      [ 0 , 0 , 0 ], 
                      [ 0 , 0 , 0 ]]
        self.ttboard = Image.open('assets/ttboard.png')

    def first_player(self):
        pass

    def track_score(self):
        pass

    def paste_card(self, card, row, col):
        img = card.img
        position = (58+row*93, 27+col*120 , 58+(row+1)*93, 27+(col+1)*120)
        self.ttboard.paste(img, box=position)

    def valid_moves(self):
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    moves.append((row,col))
        return moves

    def compare(self, card):
        """After player place a card"""
        # test
        player_input = (1, 1)
        row, col = player_input
        self.board[row][col] = card

        # check top
        if row != 0 and type(self.board[row-1][col]) == Card:
            if card.north > (self.board[row-1][col]).south:
                # change owner
                pass
        
        # check bottom
        if row != 2 and type(self.board[row+1][col]) == Card:
            pass
        
        # check right
        if col != 0 and type(self.board[row][col-1]) == Card:
            pass
        
        # check left
        if col != 2 and type(self.board[row][col+1]) == Card:
            pass

    def update_board(self, card, position):
        """
        Update self.board at each turn
        """
        raise NotImplementedError

    def process_turn(self):
        """
        Manages the game flow
        """
        raise NotImplementedError


manager = Manager()

character = [
['edea', 10, 3, 10, 3],
['irvine', 2, 9, 6, 10],
['kiros', 6, 6, 7, 10],
['laguna', 5, 3, 10, 9],
['quistis', 9, 10, 6, 2],
['rinoa', 4, 2, 10, 10],
['seifer', 6, 10, 9, 4],
['selphie', 10, 6, 8, 4],
['squall', 10, 6, 4, 9],
['ward', 10, 2, 7, 8],
['zell', 8, 10, 5, 6]]

class Card:
    def __init__(self, north, south, east, west) -> None:
        self.img = None
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.color = None

edea = Card(10, 3, 10, 3)
irvine = Card(2, 9, 6, 10)
kiros = Card(6, 6, 7, 10)
laguna = Card(5, 3, 10, 9)
quistis = Card(9, 10, 6, 2)

manager.board[0][1] = edea
manager.board[1][0] = irvine
manager.board[1][2] = kiros
manager.board[2][1] = laguna

manager.compare(quistis)

"""
Player 1's turn

1. broadcast message to discord chat -> prompt player 1 to take action
    (server) --> (chatroom)
2. Player 1 response: card, board coordinate -> server endpoint
3. server endpoint -> (main:start game object/kill game object) -> manager function to process the next action (based on card and board coordinate from (2))

Discord init game -> server endpoint -> manager function to start new game (stateful)
"""
