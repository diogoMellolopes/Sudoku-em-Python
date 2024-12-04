from tkinter import *
import random

class Sudoku():
    def __init__(self, casas):
        self.__casasReveladas = casas
        self.campoJogador = []
        self.campoCheio = []
        
    def getCasasReveladas(self):
        return self.__casasReveladas
    
    def criarCampoJogador(self):
        self.campoJogador = [[" " for i in range(0, 9)] for j in range(0, 9)]
        for i in range(self.__casasReveladas):
            while True:
                coluna = random.randint(0, 8)
                linha = random.randint(0, 8)
                quadrado = self.campoJogador[linha][coluna]
                if quadrado == " ":
                    self.campoJogador[linha][coluna] = self.campoCheio[linha][coluna]
                else:
                    continue
                break

    def criarCampoPreenchido(self):
        self.campoCheio = [["■" for _ in range(9)] for _ in range(9)]

        def verificarCampo(linha, coluna, num):
            if num in self.campoCheio[linha]:
                return False
            if num in [self.campoCheio[i][coluna] for i in range(9)]:
                return False
            inicioLinha = (linha // 3) * 3
            inicioColuna = (coluna // 3) * 3
            for i in range(3):
                for j in range(3):
                    if self.campoCheio[inicioLinha + i][inicioColuna + j] == num:
                        return False
            return True

        def preencher(linha = 0, coluna = 0):
            if linha == 9:
                return True
            proxLinha, proxColuna = (linha + 1, 0) if coluna == 8 else (linha, coluna + 1)
            if self.campoCheio[linha][coluna] != "■":
                return preencher(proxLinha, proxColuna)
            numeros = list(range(1, 10))
            random.shuffle(numeros)
            for num in numeros:
                if verificarCampo(linha, coluna, num):
                    self.campoCheio[linha][coluna] = num  
                    if preencher(proxLinha, proxColuna):  
                        return True
                    self.campoCheio[linha][coluna] = "■"  
            return False  
        preencher()

    def printarCampo(self):
        campo = ""
        temp = 1
        contLinha = 0
        contColuna = 0
        for i in range(0, 9):
            contColuna += 1
            for j in range(0, 9):
                quadrado = str(self.campoCheio[i][j])
                campo += "".join(quadrado)
                campo += "  "
                contLinha += 1
                if contLinha % 3 == 0 and contLinha != 9:
                    campo += "|  "
            if temp != i: campo += "\n"
            if contColuna % 3 == 0 and contColuna != 9:
                for j in range (0, 16):
                    campo += "- "
                campo += "\n"
            temp += 1
            contLinha = 0
        print(campo)

    def getCampoCheio(self):
        return self.campoCheio
    
    def getCampoJogador(self):
        return self.campoJogador

class Verificador(Sudoku):
    def __init__(self):
        pass

    def verificarCasa(self, coluna = 1, linha = 1, escolha = 7, campo = [], campoJogador = []):
        self.coordenada = campo
        self.campoJogador = campoJogador
        if self.campoJogador[linha][coluna] != " " or escolha == self.campoJogador[linha][coluna]:
            return "ENGANO"
        if escolha == self.coordenada[linha][coluna]:
            return True
        return False
    
class Condicionador(Sudoku):
    def __init__(self):
        pass

    def criarCondicaoVitoria(self, campo):
        campoJogador = campo
        cont = 0
        for i in range(9):
            for j in range(9):
                quadrado = str(campoJogador[i][j])
                if quadrado == " ":
                    pass
                else:
                    cont += 1
        if cont == 81:
            return True
        return False

class Pontuacao(Sudoku):
    def __init__(self, pontos = 0):
        self.__pontos = pontos
    
    def pontuar(self):
        self.__pontos += 100
    
    def getPontos(self):
        return self.__pontos
    
class Jogador(Sudoku):
    def __init__(self, nome):
        self.tentativas = 3
        self.nome = nome
    
    def printarCampo(self, campoJogador, pontos):
        campo = ""
        temp = 1
        contLinha = 0
        contColuna = 0
        for i in range(0, 9):
            contColuna += 1
            for j in range(0, 9):
                quadrado = str(campoJogador[i][j])
                campo += "".join(quadrado)
                campo += "  "
                contLinha += 1
                if contLinha % 3 == 0 and contLinha != 9:
                    campo += "|  "
            if temp != i: campo += "\n"
            if contColuna % 3 == 0 and contColuna != 9:
                for j in range (0, 16):
                    campo += "- "
                campo += "\n"
            temp += 1
            contLinha = 0
        print("Tentativas Restantes: ", self.tentativas)
        print("Pontos Totais: ", pontos, "\n")
        print(campo)

    def getTentativas(self):
        return self.tentativas

    def setTentativas(self, x):
        self.tentativas = x

    def getNome(self):
        return self.nome

class Interface():
    def __init__(self, master = None, mudarCenario = None):
        self.casasReveladas = 0
        self.mudarCenario = mudarCenario
        self.fontePadrao = ("Courier New", "12")

        self.primeiroContainer = Frame(master)
        self.primeiroContainer["padx"] = 20
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["pady"] = 20
        self.terceiroContainer.pack()

        Label(self.primeiroContainer, text = "Nome:", font = self.fontePadrao).pack(side = LEFT)

        self.nome = Entry(self.primeiroContainer, validate = "key", validatecommand = (master.register(lambda texto: len(texto) <= 20), "%P"))
        self.nome["width"] = 35
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side = LEFT)

        Label(self.segundoContainer, text = "Casas que gostaria de revelar:", font = self.fontePadrao).pack(side = LEFT)

        self.casas = Entry(self.segundoContainer, validate = "key", validatecommand = (master.register(lambda texto: len(texto) <= 2), "%P"))
        self.casas["width"] = 10
        self.casas["font"] = self.fontePadrao
        self.casas.pack(side = LEFT)

        self.avancar = Button(self.terceiroContainer)
        self.avancar["text"] = "Avançar"
        self.avancar["font"] = self.fontePadrao
        self.avancar["width"] = 12
        self.avancar["command"] = self.iniciarJogo
        self.avancar.pack()

    def iniciarJogo(self):
        try:
            self.casasReveladas = int(self.casas.get())
        except ValueError:
            self.casasReveladas = 15
        self.nomeJogador = str(self.nome.get())
        if self.casasReveladas < 0 or self.casasReveladas >= 81:
            self.casasReveladas = 15
        self.mudarCenario("jogo", self.casasReveladas, self.nomeJogador)

    def destruir(self):
        self.primeiroContainer.destroy()
        self.segundoContainer.destroy()
        self.terceiroContainer.destroy()

class Jogo():
    def __init__(self, master = None, casasReveladas = 0, nome = "a", mudarCenario = None):
        self.mudarCenario = mudarCenario
        self.casasReveladas = casasReveladas
        self.nomeJogador = nome
        fontePadrao = ("Courier New", "13")
        self.temp = ""
        self.tempCor = ""
        self.condicionador = Condicionador()
        self.pontuador = Pontuacao()
        self.jogador = Jogador(nome)
        self.jogo = Sudoku(self.casasReveladas)
        self.verificador = Verificador()
        self.jogo.criarCampoPreenchido()
        self.jogo.criarCampoJogador()

        self.containerDois = Frame(master)
        self.containerDois.pack()
        self.tentativas = Label(self.containerDois, text = "Tentativas restantes: " + str(self.jogador.getTentativas()), font = fontePadrao, height = 1)
        self.tentativas.pack(side = TOP)
        self.pontos = Label(self.containerDois, text = "Pontos totais: " + str(self.pontuador.getPontos()), font = fontePadrao, height = 1)
        self.pontos.pack(side = TOP)
        Label(self.containerDois, text = "Complete o Sudoku!", font = fontePadrao).pack(side = TOP)

        self.container = Frame(master)
        self.container.pack()
        self.botoes = []
        self.numeros = []  
        self.listaCheia = []
        contColuna = 0
        contLinha = 1
        for i in range(9):
            for j in range(9):
                coordenada = str(i) + str(j)
                botao = Button(self.container, text = str(self.jogo.campoJogador[i][j]), font = ("Courier New", "14"), width = 2, height = 1)
                botao.grid(row = i + contLinha, column = j + contColuna)
                botao.config(command = lambda b = botao, c = coordenada: self.atualizar(b, c))
                self.botoes.append(botao)
                self.botoes.append(coordenada)
                self.listaCheia.append(botao["text"])
                if j == 2 or j == 5:
                    Frame(self.container, width = 4.35, bg = "gray", height = 37).grid(row = i + contLinha, column = j + contColuna + 1)
                    contColuna += 1
            if i == 2 or i == 5:
                Frame(self.container, height = 4.35, bg = "gray", width = 296).grid(row = i + contLinha + 1, column = 0, columnspan = 20)
                contLinha += 1
            contColuna = 0
        contLinha = 0
        Frame(self.container, height = 4.35, bg = "gray", width = 296).grid(row = 25, column = 0, columnspan = 20)
        Frame(self.container, height = 5, bg = "gray", width = 296).grid(row = 0, column = 0, columnspan = 20)

        self.containerTres = Frame(master)
        self.containerTres.pack()
        self.atual = Label(self.containerTres, text = "Número selecionado: ", font = fontePadrao)
        self.atual.grid(row = 1, column = 0)

        self.containerQuatro = Frame(master)
        self.containerQuatro.pack()
        for i in range(1, 10):
            self.escolhaBotao = Button(self.containerQuatro, text = str(i), font = ("Courier New", "14"), width = 2, height = 1)
            self.escolhaBotao.grid(row = 0, column = i - 1)
            self.escolhaBotao.config(command = lambda i = i, opcao = self.escolhaBotao: self.escolha(i, opcao))
            self.numeros.append(self.escolhaBotao)
            contagem = self.listaCheia.count(str(i))
            if str(i) in self.listaCheia and contagem == 9:
                self.escolhaBotao.destroy()

    def escolha(self, valor, cor):
        try:
            self.tempCor["fg"] = "black"
        except TypeError:
            pass
        except TclError:
            pass
        cor["fg"] = "blue2"
        self.atual["text"] = "Número selecionado: " + str(valor)
        self.temp = str(valor)
        self.tempCor = cor
    
    def atualizar(self, botao, coordenada):
        tentativas = self.jogador.getTentativas()
        num = int(self.temp)
        linha = int(coordenada[0])
        coluna = int(coordenada[1])
        perdeu = 0
        verificacao = self.verificador.verificarCasa(coluna, linha, num, self.jogo.campoCheio, self.jogo.campoJogador)
        if verificacao == True:
            botao["text"] = self.temp
            self.listaCheia.append(self.temp)
            contagem = self.listaCheia.count(self.temp)
            if self.temp in self.listaCheia and contagem == 9:
                self.tempCor.destroy()
            botao["fg"] = "blue2"
            self.jogo.campoJogador[linha][coluna] = self.jogo.campoCheio[linha][coluna]
            self.pontuador.pontuar()
            self.pontos["text"] = "Pontos totais: " + str(self.pontuador.getPontos())
            if self.condicionador.criarCondicaoVitoria(self.jogo.campoJogador):
                perdeu = 0
                self.finalizarJogo(perdeu)
        elif verificacao == False:
            botao["text"] = self.temp
            botao["fg"] = "red"
            self.jogador.setTentativas(tentativas - 1)
            self.tentativas["text"] = "Tentativas restantes: " + str(self.jogador.getTentativas())
            if tentativas < 1:
                perdeu = 1
                self.finalizarJogo(perdeu)
        else:
            pass

    def finalizarJogo(self, perdeu):
        self.perdeu = perdeu
        self.nomeJogador = self.jogador.getNome()
        self.pontosFinais = self.pontuador.getPontos()
        self.mudarCenario("fim", 0, self.nomeJogador, self.pontosFinais, self.perdeu)

    def destruir(self):
        self.container.destroy()
        self.containerDois.destroy()
        self.containerTres.destroy()
        self.containerQuatro.destroy()

class Fim():
    def __init__(self, master = None, nome = "a", pontos = 0, perdeu = 0, mudarCenario = None):
        self.master = master
        self.mudarCenario = mudarCenario
        self.nomeJogador = nome
        self.pontosTotais = pontos
        self.perdeu = perdeu

        self.container = Frame(master)
        self.container.pack()
        if self.perdeu == 1:
            mensagem = "Você perdeu!"
        elif self.perdeu == 0:
            mensagem = "Parabéns, " + self.nomeJogador + " você venceu!"

        Label(self.container, text = mensagem, font = ("Courier New", "15")).pack(pady = 10)
        Label(self.container, text = "Pontos: " + str(self.pontosTotais), font = ("Courier New", "13")).pack(pady = 5)
        self.botaoMenu = Button(self.container, text = "Reiniciar Jogo!", font = ("Courier New", "13"), command = self.voltarMenu)
        self.botaoMenu.pack(pady=10)

    def voltarMenu(self):
        self.mudarCenario("menu")

    def destruir(self):
        self.container.destroy()

class Aplicacao():
    def __init__(self, master):
        self.master = master
        self.cenarioAtual = None
        self.carregarCenario("menu")

    def carregarCenario(self, cenario, casasReveladas = 0, nome = "a", pontosFinais = 0, perdeu = 0):
        if self.cenarioAtual:
            self.cenarioAtual.destruir()
        if cenario == "menu":
            self.cenarioAtual = Interface(self.master, self.carregarCenario)
        elif cenario == "jogo":
            self.cenarioAtual = Jogo(self.master, casasReveladas, nome, self.carregarCenario)
        elif cenario == "fim":
            self.cenarioAtual = Fim(self.master, nome, pontosFinais, perdeu, self.carregarCenario)

if __name__ == "__main__":
    root = Tk()
    root.title("Sudoku")
    app = Aplicacao(root)
    root.mainloop()