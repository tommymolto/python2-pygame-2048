import random, copy, pygame, sys
from enum import Enum

# Implementação de 2048 em pygame 3



###################### Variaveis globais ########################



tamanhoQuadrado = 100 # tamanho do quadrado em pixels
linhasNoJogo = 7  # area de x por x quadrados
class Movimentos(Enum):
    """Enumerator com os movimentos possiveis"""
    cima = 0
    baixo = 1
    esquerda = 2
    direita = 3

moveDict = {
    pygame.K_UP: Movimentos.cima,
    pygame.K_DOWN: Movimentos.baixo,
    pygame.K_LEFT: Movimentos.esquerda,
    pygame.K_RIGHT: Movimentos.direita
    }  # map key events to moves





######################## Classes ###############################



class JogoEstado(object):
    """2d array of all values in current game's state."""

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.data = [[None for x in range(tamanho)] for y in range(tamanho)]  # 2d array, estado do jogo
        

    def desenhaNaTela(self, tela):
        """Desenha o estado atual do jogo na tela."""
        tela.fill((119,110,101))  # colore
        fonte = pygame.font.Font(None, 60)  # textos terao esta fonte desse tamanho
        for y in range(self.tamanho):
            for x in range(self.tamanho):
                
                # draw square of particular item to screen w/ 1 thick border
                quadradinho = pygame.Rect(x*tamanhoQuadrado+1, y*tamanhoQuadrado+1, tamanhoQuadrado-2, tamanhoQuadrado-2)
                pygame.draw.rect(tela, self.pegaCorQuadrado(self.pegaItem(x, y)), quadradinho)
                if self.pegaItem(x, y) == None: continue # se nao existe item, desenha vazio
                texto = fonte.render(str(self.pegaItem(x, y)), 1, (249, 246, 242) if self.pegaItem(x, y) >= 8 else (119, 110, 101))
                # Center text onto tile
                textoQuadradinho = texto.get_rect()
                textoQuadradinho.centerx = quadradinho.centerx
                textoQuadradinho.centery = quadradinho.centery
                screen.blit(texto, textoQuadradinho)  # blit number to respective square

    def __eq__(self, other):
        """Verifica iguadade entre 2 jogos."""
        if self.tamanho != other.tamanho:
            return False  # São diferentes em tamanho
        for y in range(self.tamanho): 
            for x in range(self.tamanho):
                if self.pegaItem(x, y) != other.pegaItem(x, y): return False  # se algum item mudou de lugar, falso
        return True  # Se passou nas verificacoes acima, verdadeiro

    def pegaItem(self, x, y):
        assert (x in range(0, self.tamanho) and y in range(0, self.tamanho))
        return self.data[y][x]

    def setaItem(self, x, y, newVal):
        assert (x in range(0, self.tamanho) and y in range(0, self.tamanho))
        self.data[y][x] = newVal
    def pegaCorQuadrado(self,numero):
        # Puro design para cores dos quadrados
        # Adaptado de https://github.com/gabrielecirulli/2048/blob/master/style/main.css
        # retorna o RBG do jogo original para cada valor
        dicCorQuadrado = {2: 'eee4da', 4: 'ede0c8', 8: 'f2b179', 16: 'f59563', 32: 'f59563', 64: 'f65e3b', 128: 'edcf72', 256: 'edcc61', 512: 'edc850', 1024: 'edc53f', 2048: 'edc22e', 'super': '3c3a32'}
        hexString = dicCorQuadrado[numero] if numero in dicCorQuadrado else dicCorQuadrado['super']
        return (int(hexString[0:2], 16), int(hexString[2:4], 16), int(hexString[4:6], 16))



class SessaoJogo(object):
    def __init__(self, tamanho):
        self.JogoEstado = JogoEstado(tamanho)
        self.acabou = False

    def desenhaNaTela(self, tela):
        self.JogoEstado.desenhaNaTela(tela)

    def proximoMovimento(self, move):
        """Advance game to next move."""
        self.moveTodosQuadradosNaDirecao(move)
        self.verificaFimJogo()
        state = self.JogoEstado
        isFull = all([state.pegaItem(x,y)!=None for x in range(self.JogoEstado.tamanho) for y in range(self.JogoEstado.tamanho)])
        if not isFull: self.adicionaRandomicamenteValor(2)

    def moveTodosQuadradosNaDirecao(self, move):
        """Move all items in a particular direction."""
        ultimoEstado = JogoEstado(self.JogoEstado.tamanho)

        while not self.JogoEstado == ultimoEstado:  # Keep trying to move each item until none can be moved
            # Loop through each item in list
            ultimoEstado = copy.deepcopy(self.JogoEstado)
            for y in range(self.JogoEstado.tamanho):
                for x in range(self.JogoEstado.tamanho):
                    if self.JogoEstado.pegaItem(x, y) == None: continue
                    #Decide which direction to move each item depending on move
                    if move == Movimentos.cima and y>0:
                        self.mudaUmItemPara([x, y], [x, y-1])
                    elif move == Movimentos.baixo and y<self.JogoEstado.tamanho-1:
                        self.mudaUmItemPara([x, y], [x, y+1])
                    elif move == Movimentos.esquerda and x>0:
                        self.mudaUmItemPara([x, y], [x-1, y])
                    elif move == Movimentos.direita and x<self.JogoEstado.tamanho-1:
                        self.mudaUmItemPara([x, y], [x+1, y])

    def mudaUmItemPara(self, xyInicial, xyFinal): # shiftOneItemTo(self, startCoords, endCoords):
        """Shift a specific item at startCoords to endCoords.
        If endCoords has an item identical to at startCoords, add the two together. If none at endcoords, shift to there. Else, do nothing."""
        startVal = self.JogoEstado.pegaItem(xyInicial[0], xyInicial[1])
        endVal = self.JogoEstado.pegaItem(xyFinal[0], xyFinal[1])

        if endVal == None:
            self.JogoEstado.setaItem(xyFinal[0], xyFinal[1], startVal)
        elif startVal == endVal:
            self.JogoEstado.setaItem(xyFinal[0], xyFinal[1], startVal+endVal)
        else:
            return None
        self.JogoEstado.setaItem(xyInicial[0], xyInicial[1], None)

    def adicionaRandomicamenteValor(self, val):
        """Add new number with value 'val' to array in random location when move is done"""
        while True:  # Keep selecting random points until one with nothing in it is found
            x = random.randint(0, self.JogoEstado.tamanho-1)
            y = random.randint(0, self.JogoEstado.tamanho-1)
            if self.JogoEstado.pegaItem(x, y) == None:
                self.JogoEstado.setaItem(x, y, val)
                break
            else: continue

    def verificaFimJogo(self):
        """Use to update whether game is over or not."""
        self.acabou = True
        isEmpty = all([self.JogoEstado.pegaItem(x,y)==None for x in range(self.JogoEstado.tamanho) for y in range(self.JogoEstado.tamanho)])
        # check if any movements are possible, if not, game is over
        movLs = [Movimentos.cima, Movimentos.baixo, Movimentos.direita, Movimentos.esquerda]
        gameMoves = [copy.deepcopy(self) for i in range(len(movLs))]
        for i in range(len(movLs)): gameMoves[i].moveTodosQuadradosNaDirecao(movLs[i])
        if isEmpty or not all([self.JogoEstado == x.JogoEstado for x in gameMoves]):
            self.acabou = False



########################## Main module #############################




pygame.init()
screen = pygame.display.set_mode(
    (tamanhoQuadrado*linhasNoJogo, tamanhoQuadrado*linhasNoJogo)
    )
pygame.display.set_caption('2048')

gameSession = SessaoJogo(linhasNoJogo)

while not gameSession.acabou:
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(0, 0, tamanhoQuadrado*linhasNoJogo, tamanhoQuadrado*linhasNoJogo))  # clear the screen with black
    gameSession.desenhaNaTela(screen)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key in moveDict.keys():
            gameSession.proximoMovimento(moveDict[event.key])
        elif event.type == pygame.QUIT:
            pygame.display.quit()
    pygame.display.flip()