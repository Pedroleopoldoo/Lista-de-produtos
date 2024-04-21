import csv
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


# Exportação para CSV
def verifica_arquivo(lista_produtos, escolha):
    Local_Arquivo = '1_5_arquivo_produto.csv'

    try:
        if os.path.isfile(Local_Arquivo) and escolha == 2:
            with open(Local_Arquivo, mode='a', newline='') as arquivo_csv:
                Escreve_Informacoes = csv.writer(arquivo_csv)
                Escreve_Informacoes.writerows(lista_produtos)
        else:
            with open(Local_Arquivo, mode='w', newline='') as arquivo_csv:
                Escreve_Informacoes = csv.writer(arquivo_csv)
                Escreve_Informacoes.writerow(['Descrição do Produto', 'Valor do Produto', 'Tipo de Embalagem do Produto'])
                Escreve_Informacoes.writerows(lista_produtos)
    except IOError as e:
        messagebox.showerror("Erro", f"Erro ao manipular o arquivo: {e}")


# Botão de executar, coloca todas as informações coletadas em uma lista e joga para a verifica_arquivo
# Além disso, encerra o programa
def executor():
    class ErroDescricaoInvalida(Exception):
        def __str__(self):
            return "A descrição deve conter somente letras e não deve estar vazia"

    class ErroEmbalagemInvalida(Exception):
        def __str__(self):
            return "A embalagem deve conter somente letras e não deve estar vazia"

    def num_there(s):
        return any(i.isdigit() for i in s)

    try:
        lista_produtos = []
        for itens in range(len(frames_itens)):
            descricao = entry_descricao_respostas[itens].get()
            valor = entry_valor_respostas[itens].get()
            embalagem = entry_embalagem_respostas[itens].get()

            # Verifica se a descrição contém apenas letras
            try:
                if num_there(descricao) or descricao.strip() == "":
                    raise ErroDescricaoInvalida
            except ErroDescricaoInvalida as e:
                messagebox.showerror(f"Erro no item {itens + 1}", e)
                return

            try:
                valor = float(valor)  # Converte o valor para float
            except ValueError:
                messagebox.showerror(f"Erro no item {itens + 1}", "O valor do produto deve ser numérico.")
                return

            try:
                if num_there(embalagem) or embalagem.strip() == "":
                    raise ErroEmbalagemInvalida
            except ErroEmbalagemInvalida as e:
                messagebox.showerror(f"Erro no item {itens + 1}", e)
                return

            lista_produtos.append([descricao, valor, embalagem])

        escolha = var.get()
        verifica_arquivo(lista_produtos, escolha)
        janela.quit()

    except Exception as e:
        messagebox.showerror("Erro", "Erro ao rodar o programa.")


# Adiciona uma nova aba com todas as informações que o usuário deve colocar
def adicionar_aba():
    try:
        # Cada item
        frame_item = ttk.Frame(notebook)
        # Adiciona um novo item e coloca um título
        notebook.add(frame_item, text=f"Item {len(notebook.tabs()) + 1}")

        # Label de descrição para cada aba
        label_descricao_pergunta = Label(frame_item, text="Insira a descrição do produto")
        label_descricao_pergunta.place(x=50, y=40)
        entry_descricao_resposta = Entry(frame_item)
        entry_descricao_resposta.place(x=60, y=65)

        # Label de valor para cada aba
        label_valor_pergunta = Label(frame_item, text="Insira o valor do produto")
        label_valor_pergunta.place(x=250, y=40)
        entry_valor_resposta = Entry(frame_item)
        entry_valor_resposta.place(x=260, y=65)

        # Label de embalagem para cada aba
        label_embalagem_pergunta = Label(frame_item, text="Insira o tipo de embalagem")
        label_embalagem_pergunta.place(x=450, y=40)
        entry_embalagem_resposta = Entry(frame_item)
        entry_embalagem_resposta.place(x=460, y=65)


        # Adiciona informações nas listas, por conta disso essa função tem que rodar depois que as listas existam já
        frames_itens.append(frame_item)
        entry_descricao_respostas.append(entry_descricao_resposta)
        entry_valor_respostas.append(entry_valor_resposta)
        entry_embalagem_respostas.append(entry_embalagem_resposta)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao adicionar aba: {e}")
        return


# interface principal
janela = Tk()
janela.title("Cadastrador de produtos SGV")
janela.geometry("700x400")
janela.resizable(False, False)

# Adiciona a interface de abas dentro da interface principal, mas sem adicionar nenhuma aba ainda
notebook = ttk.Notebook(janela)
notebook.pack(fill='both', expand=True)

# Listas com número de abas adicionadas e as três informações adicionadas, uma em cada lista para uso posterior
frames_itens = []
entry_descricao_respostas = []
entry_valor_respostas = []
entry_embalagem_respostas = []

# adiciona as 5 abas obrigatórias ao programa
for i in range(1, 6):
    adicionar_aba()


Label(janela, text="Você deseja adicionar mais itens? ").place(x=230, y=180)

# Botão que faz adicionar uma nova aba para ter um novo item
botao_adicionar = Button(janela, text="Sim, é claro", command=adicionar_aba)
botao_adicionar.place(x=280, y=213)

# botão que executa o executor, fazendo o fim do programa e adiciona as novas informações, além de aplicar as exceções
botao = Button(janela, text="Exportar para CSV", command=executor)
botao.place(x=260, y=350)

# Opção de continuar ou não
Label(janela, text="Caso já exista um arquivo, você deseja sobrescreve-lo ou adicionar no atual? ").place(x=110, y=250)

# Variável de controle para armazenar a opção selecionada (pré-selecionada para 'sobescrever')
var = IntVar(value=1)

# Criando botões de opção para Sim e Não
Radiobutton(janela, text="sobrescrever", variable=var, value=1).place(x=260, y=270)
Radiobutton(janela, text="adicionar no atual", variable=var, value=2).place(x=260, y=290)

# Loop para programa sempre continuar rodando até ser encerrado
janela.mainloop()
