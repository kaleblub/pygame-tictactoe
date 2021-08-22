import pygame
# ----------- Game Initialization -------------------
pygame.init()

displayWidth, displayHeight = 685, 780

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Tic-Tac-Toe')

# ----------- Constants -------------------
font = pygame.font.SysFont(None, 100)

gameOverMessage = """
Game Over, 
press C to 
play again 
or Q to quit."""

tileSize = 225

# Initiate the board
board = []

for y in (100, 101 + tileSize, 102 + (tileSize*2)): 
	for x in (4, 5 + tileSize, 6 + (tileSize*2)):
		box = pygame.Rect(x, y, tileSize, tileSize)
		board.append(box) # place each box in the board

def blitMultiLineText(surface, text, position, font , color=pygame.Color("black")):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    maxWidth, maxHeight = surface.get_size()
    x, y = position
    for line in words:
        for word in line:
            wordSurface = font.render(word, 0, color)
            wordWidth, wordHeight = wordSurface.get_size()
            if x + wordWidth >= maxWidth:
                x = position[0]  # Reset the x.
                y += wordHeight  # Start on new row.
            surface.blit(wordSurface, (x, y))
            x += wordWidth + space
        x = position[0]  # Reset the x.
        y += wordHeight  # Start on new row.

def isGameOver(board):
	# Check Horizontals
	if board[0] == board[1] and board[1] == board[2] and board[2] != None:
		scores.scoreUpdate(board[0])
		return True
	elif board[3] == board[4] and board[4] == board[5] and board[5] != None:
		scores.scoreUpdate(board[3])
		return True
	elif board[6] == board[7] and board[7] == board[8] and board[8] != None:
		scores.scoreUpdate(board[6])
		return True
	# Check Verticals
	elif board[0] == board[3] and board[3] == board[6] and board[6] != None:
		scores.scoreUpdate(board[0])
		return True
	elif board[1] == board[4] and board[4] == board[7] and board[7] != None:
		scores.scoreUpdate(board[1])
		return True
	elif board[2] == board[5] and board[5] == board[8] and board[8] != None:
		scores.scoreUpdate(board[2])
		return True
	# Check Diagonals
	elif board[0] == board[4] and board[4] == board[8] and board[8] != None:
		scores.scoreUpdate(board[0])
		return True
	elif board[2] == board[4] and board[4] == board[6] and board[6] != None:
		scores.scoreUpdate(board[2])
		return True
	else:
		return False

# Checks If Given Box Is Available or Not
def spaceIsAvailable(box, trackBoard):
	if trackBoard[board.index(box)] == None:
		return True
	else:
		return False

# Switches The Current Player
def switchTurn(currentPlayer):
	if currentPlayer == 'x':
		return 'o'
	else:
		return 'x'

class Scores:
	def __init__(self):
		self.xScore = 0
		self.oScore = 0
		self.xScoreMessage = font.render(f'X: {self.xScore}', True, "red")
		self.oScoreMessage = font.render(f'O: {self.oScore}', True, "blue")
	
	def scoreUpdate(self, currentPlayer):
		if currentPlayer == 'x':
			self.xScore += 1
			self.xScoreMessage = font.render(f'X: {self.xScore}', True, "red")
		else:
			self.oScore += 1
			self.oScoreMessage = font.render(f'O: {self.oScore}', True, "blue")

# Initiate Scores Class Outside Of Main Loop 
# So That The Scores Are Saved
scores = Scores()

# ----------- Main Game Function ---------------
def runGame():
	# Game Variables
	gameRunning = True
	gameOver = False

	letter = font.render('X', True, "white")

	currentPlayer = 'x' # The Turn of the Current Player
	turnMessage = font.render(f'{currentPlayer.upper()} Turn', True, "black")

	trackBoard = [None for i in range(0, 9)] # Board to keep track of X's and O's

# ------------- Start Of Game Loop ----------------
	while gameRunning:

# ----------- Game Over Menu -------------
		while gameOver == True:
			gameDisplay.fill("white")
			blitMultiLineText(gameDisplay, gameOverMessage, (20, 20), font, color="red")
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameRunning = False
				if event.type == pygame.KEYDOWN:
					if event.key == ord('q'):
						gameRunning = False
						gameOver = False
						pygame.quit()
					if event.key == pygame.K_c:
						runGame()

# ------------- Gameplay Handling ----------------
		for event in pygame.event.get(): # If the exit button was clicked, exit the game
			if event.type == pygame.QUIT:
				gameRunning = False
			if event.type == pygame.MOUSEBUTTONUP:
				for box in board: 								 # If the mouse was clicked
					if box.collidepoint(pygame.mouse.get_pos()) and spaceIsAvailable(box, trackBoard): # Check if it was in a box on the board and if the box is available or not
						trackBoard[board.index(box)] = currentPlayer 	 # Make the board reflect the current player's choice
						currentPlayer = switchTurn(currentPlayer)
						turnMessage = font.render(f'{currentPlayer.upper()} Turn', True, "black") # Re-render the turnMessage
						gameOver = isGameOver(trackBoard)

#  ----------- Game Code -------------------
		# Refresh the screen with white
		gameDisplay.fill("white")

		# Display the scores of each player
		gameDisplay.blit(scores.xScoreMessage, (0, 10))
		gameDisplay.blit(scores.oScoreMessage, (500, 10))

		# Display whose turn it is
		gameDisplay.blit(turnMessage, (230, 10))

		# Draw The Current Gameboard
		for box in board:
			if trackBoard[board.index(box)] == 'x': # if x has previously selected a box, display red
				pygame.draw.rect(gameDisplay, "red", box)
			elif trackBoard[board.index(box)] == 'o': # if o has previously selected a box, display blue
				pygame.draw.rect(gameDisplay, "blue", box)
			elif box.collidepoint(pygame.mouse.get_pos()): # if the box is being hovered over, display green
				pygame.draw.rect(gameDisplay, "green", box)
			else: 										  # if nothing is/has happened to the box, display black
				pygame.draw.rect(gameDisplay, "black", box)

		pygame.display.update()

	pygame.quit()
	quit()

if __name__ == "__main__":
	runGame()