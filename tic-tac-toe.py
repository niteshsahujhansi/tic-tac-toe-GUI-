import copy
import random
import pygame
import sys
import numpy as np

from constants import *

# --- pygame setup --- 

pygame.init()
screen = pygame.display.set_mode( (WIDTH+WIDTH, HEIGHT) ) 
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

pygame.mixer.init()
pygame.mixer.music.load("game.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# --- classes ---

class board:
    
    def __init__(self):

        self.squares = np.zeros( (ROWS, COLS) )     # create 2D list(array), for console representation
        # self.squares = [[0]*3, [0]*3, [0]*3]      # same as above line
        self.empty_sqrs = self.squares              # list of [squares]
        self.marked_sqrs = 0                        # initialize marked sqrs to 0, self.mark_sqr(1,1,3), print(self.squares), (value can varry from 0 to 9)

    def final_state(self, show=False):

        ''' return 0 if draw
            return 1 if player 1 wins
            return 2 if player 2 wins   '''
        
        # vertical wins 
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:       # same player in one vertical line     
                if show:
                    color = CIRC_COLOR if self.squares[0][col] ==2 else CROSS_COLOR
                    ipos = (col * SQSIZE + SQSIZE // 2, 20)
                    fpos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, ipos, fpos, LINE_WIDTH)                     # draw winning line                    
                
                return self.squares[0][col]

        # horizontal wins 
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] ==2 else CROSS_COLOR
                    ipos = (20, row * SQSIZE + SQSIZE // 2)
                    fpos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, ipos, fpos, CROSS_WIDTH)

                return self.squares[row][0]

        # desc diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] ==2 else CROSS_COLOR
                ipos = (20, 20)
                fpos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, ipos, fpos, CROSS_WIDTH)
                    
            return self.squares[1][1]

        # asc diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] ==2 else CROSS_COLOR
                ipos = (20, HEIGHT - 20)
                fpos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, ipos, fpos, CROSS_WIDTH)

            return self.squares[1][1]
        
        # draw
        
        return 0

    def mark_sqr(self, row, col, player):

        self.squares[row][col] = player         # assign player (1 or 2) to a perticular squares (row, col) 
        self.marked_sqrs += 1                   # increase marked sqrs by 1 on each mark sqr

    def empty_sqr(self, row, col):
        
        return self.squares[row] [col] == 0 # this function will return true if squares is empty

    def get_empty_sqrs(self):

        '''this method return a list of empty squares'''

        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        # print(empty_sqrs)
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):          # by defaut lever=1 mean unbeatable ai, 0 for ramdam ai, player=2 means ai has second turn, first has user
        self.level = level
        self.player = player 
    
    # --- random ---

    def rnd(self, board):
    
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col), return a random square out of empty squares

    def minmax(self, board, maximizing):

    # --- MINMAX ALGORITHM ---

        # terminal case 
        case = board.final_state() # (0-draw, 1-player1 wins, 2-player2 wins)

        # player 1 wins
        if case == 1:
            return 1, None #evel, move

        # player 2 win
        if case == 2:
            return -1, None
        
        # draw
        elif board.isfull():
            return 0, None

        if maximizing:                                       # by default user is the maximizing player
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minmax(temp_board, False)[0]
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    
            return max_eval, best_move

        elif not maximizing:                                 # by default AI is minimizing player
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minmax(temp_board, True)[0]     # recursive call,  this is minimizing and next step will be maximizing
                                                            # that is why we pass maximizing value TRUE
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move   
    
    def eval(self, main_board):

        if self.level == 0:                         # choose level 0 for random ai
            # random choise
            eval = 'random'
            move = self.rnd(main_board)
        else:                                       # by default game mode is 1 
            # minmax algo choise
            eval, move = self.minmax(main_board, False) # by default ai is minimizing player that is why we pass False value to maximizing variable

        # print('AI has choosen to mark the square in pos ', move, 'with an eval of ',eval )
        # print(self.player,'turn')

        return move # (row, colS)

class Game:

    def __init__(self):
        self.board = board()
        self.ai = AI()
        self.player = 1 # 1-cross, 2-circle
        
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)    # print(game.board.squares) # assign player (1) to perticular square 
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill( BG_COLOR )
        # vertical 
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),LINE_WIDTH)
        
        # horizontal
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),LINE_WIDTH)

    def draw_fig(self, row, col):

        if self.player == 1:
            # print('O turn')
            # draw cross
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # print('X turn')
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            # (x, y) (100, 100) (300, 100) (500, 100)
            # print(center)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
    
    def next_turn(self):
        self.player = self.player % 2 + 1 #try dry run

    def change_gamemode(self):
        # if self.gamemode == 'pvp':
        #     self.gamemode = 'ai'
        # else:
        #     self.gamemode = 'pvp'
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show = True) != 0 or self.board.isfull() # return true if condition true

    def reset(self):
        self.__init__()

class Board_2:

    def __init__(self):
        self.show_border()
        self.show_title()
        self.show_mode_Buttons()
        self.show_mode_text()
    
    def show_border(self):
        whole_window = (0, 0, WIDTH+WIDTH, HEIGHT)
        pygame.draw.rect(screen,LINE_COLOR, whole_window,3) # outline for whole window

        right_window = (WIDTH, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen,LINE_COLOR,right_window,3) # outline for control (Right) window
    
    def show_title(self):
        font1 = pygame.font.SysFont('freesanbold.ttf', 50)
        tictactoe = font1.render('TIC - TAC - TOE', True, TEXT_COLOR)
        tictactoeRect = tictactoe.get_rect()
        tictactoeRect.center = (WIDTH+(WIDTH/2), OFFSET)
        screen.blit(tictactoe, tictactoeRect) 

        font2 = pygame.font.SysFont('chalkduster.ttf', 30)
        game = font2.render('GAME', True, TEXT_COLOR)
        gameRect = game.get_rect()
        gameRect.center = (WIDTH+(WIDTH/2), OFFSET*2)
        screen.blit(game, gameRect)
    
    def show_mode_Buttons(self):      

        self.randomRact = pygame.Rect((WIDTH, OFFSET*4), (WIDTH/3, OFFSET))
        pygame.draw.rect(screen,LINE_COLOR,self.randomRact,3)

        self.aiRact = (WIDTH+WIDTH/3, OFFSET*4, WIDTH/3, OFFSET)
        pygame.draw.rect(screen,LINE_COLOR,self.aiRact,3)
        
        self.playerRact = (WIDTH+WIDTH/1.5, OFFSET*4, WIDTH/3, OFFSET)
        pygame.draw.rect(screen,LINE_COLOR,self.playerRact,3)

        self.restartRact = (WIDTH, OFFSET*6, WIDTH/2, OFFSET)
        pygame.draw.rect(screen,LINE_COLOR,self.restartRact,3)

        self.exitRact = (WIDTH+WIDTH/2, OFFSET*6, WIDTH/2, OFFSET)
        pygame.draw.rect(screen,LINE_COLOR,self.exitRact,3)

    def show_mode_text(self):

        font2 = pygame.font.SysFont('chalkduster.ttf', 30)
        mode = font2.render('Select Game Mode', True, TEXT_COLOR )
        modeRect = mode.get_rect()
        modeRect.center = (WIDTH+(WIDTH/2), OFFSET*3.5)
        screen.blit(mode, modeRect)

        random = font2.render('Random', True, TEXT_COLOR )
        randomRect = random.get_rect()
        randomRect.center = (WIDTH+((WIDTH/6)), OFFSET*4.5)
        screen.blit(random, randomRect)

        ai = font2.render('Unbeatable AI', True, TEXT_COLOR )
        aiRect = ai.get_rect()
        aiRect.center = (WIDTH+(WIDTH/2), OFFSET*4.5)
        screen.blit(ai, aiRect)

        player = font2.render('Player to Player', True, TEXT_COLOR )
        playerRect = player.get_rect()
        playerRect.center = (WIDTH+(WIDTH/1.2), OFFSET*4.5)
        screen.blit(player, playerRect)

        restart = font2.render('RESTART', True, TEXT_COLOR )
        restartRect = restart.get_rect()
        restartRect.center = (WIDTH+WIDTH/4, OFFSET*6.5)
        screen.blit(restart, restartRect)

        exit = font2.render('EXIT', True, TEXT_COLOR )
        exitRect = exit.get_rect()
        exitRect.center = (WIDTH+WIDTH/1.38, OFFSET*6.5)
        screen.blit(exit, exitRect)

    def random_clicked(self):
        pygame.draw.rect(screen,CLICKED_COLOR,self.randomRact,3)
        pygame.draw.rect(screen,LINE_COLOR,self.aiRact,3)
        pygame.draw.rect(screen,LINE_COLOR,self.playerRact,3)
    
    def ai_clicked(self):
        pygame.draw.rect(screen,LINE_COLOR,self.randomRact,3)
        pygame.draw.rect(screen,CLICKED_COLOR,self.aiRact,3)
        pygame.draw.rect(screen,LINE_COLOR,self.playerRact,3)
    
    def player_clicked(self):
        pygame.draw.rect(screen,LINE_COLOR,self.randomRact,3)
        pygame.draw.rect(screen,LINE_COLOR,self.aiRact,3)
        pygame.draw.rect(screen,CLICKED_COLOR,self.playerRact,3)

def main():

    # object 
    game = Game()
    board = game.board # we'll use board instead of game.board to be the code readable and clear
    ai = game.ai 
    board_2 = Board_2()

    # main loop 
    while True:
        
        for event in pygame.event.get():            # itrate through all events
            
            if event.type == pygame.QUIT:           # to close the window
                pygame.quit()
                sys.exit()                          # termiate the python program
            
            if event.type == pygame.KEYDOWN:        # keyboard controls

                # g - gamemode 
                if event.key == pygame.K_g:
                    game.change_gamemode()
                
                # r - reset
                if event.key == pygame.K_r:
                    game.reset()
                    board_2.__init__()
                    board = game.board
                    ai = game.ai  

                # 0 random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 unbeatable ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:    

                pos = event.pos                     # pos has two value (x, y), print(event.pos)
                
                if pos[0] <= WIDTH :
                    
                    track1 = pygame.mixer.Sound("move.wav")
                    track1.play()                       # clicked sound on move

                    row = pos[1] // SQSIZE              # pos[1] represent y axis, print(row), thus we get the no. of row clicked
                    col = pos[0] // SQSIZE              # pos[0] represent x axis, print(col), thus we get the no. of col clicked
                                                        # print(row, col) # thus we get (cordinate) the squares clicked

                    if board.empty_sqr(row, col) and game.running : #true only if clicked square is empty
                        game.make_move(row, col)

                        if game.isover():
                            game.running = False 
                

                mouse = pygame.mouse.get_pos()  

                # random button clicked
                if WIDTH <= mouse[0] <= WIDTH+WIDTH/3 and OFFSET*4 <= mouse[1] <= OFFSET*5:
                    board_2.random_clicked()                                                           
                    ai.level = 0
                    track1 = pygame.mixer.Sound("mode.wav")
                    track1.play()

                # unbeatable ai button clicked
                elif WIDTH+WIDTH/4 <= mouse[0] <= WIDTH+WIDTH/1.5 and OFFSET*4 <= mouse[1] <= OFFSET*5:
                    board_2.ai_clicked()      
                    ai.level = 1
                    track1 = pygame.mixer.Sound("mode.wav")
                    track1.play()
                
                # Player to player button clicked 
                elif WIDTH+WIDTH/1.5 <= mouse[0] <= WIDTH+WIDTH and OFFSET*4 <= mouse[1] <= OFFSET*5:
                    board_2.player_clicked()
                    game.change_gamemode()
                    track1 = pygame.mixer.Sound("mode.wav")
                    track1.play()

                # restart button clicked 
                if WIDTH <= mouse[0] <= WIDTH+WIDTH/2 and OFFSET*6 <= mouse[1] <= OFFSET*7 :
                    game.reset()
                    board_2.__init__()
                    board = game.board
                    ai = game.ai
                    track1 = pygame.mixer.Sound("restart.wav")
                    track1.play()
                
                # exit button clicked 
                if WIDTH+WIDTH/2 <= mouse[0] <= WIDTH+WIDTH and OFFSET*6 <= mouse[1] <= OFFSET*7 :
                    track1 = pygame.mixer.Sound("exit.wav")
                    track1.play()
                    pygame.time.delay(500) # 1 second == 1000 milliseconds
                    pygame.quit()
                    sys.exit()
                    
            if game.gamemode =='ai' and game.player == ai.player and game.running :     # if we do not use game.running then after the square gets full the code will search for next move even it does not have empty square.
                # update the screen                                                     # and with this we will also use isover function below``
                pygame.display.update()

                # ai method 
                row, col = ai.eval(board)
                game.make_move(row, col)

                if game.isover():
                    game.running = False
    
        pygame.display.update()

main()
