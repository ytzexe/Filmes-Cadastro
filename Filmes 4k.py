#PROJETO 21/05/2025
#Bibliotecas
import customtkinter as ctk
from tkinter import messagebox
from collections import Counter
import json
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

filmes_json = "filmes.json"

#Funçao para ler os filmes proporcionados
def ler_filmes():
    if not os.path.exists(filmes_json):
        return []
    with open(filmes_json, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []

#Funçao para salvar os filmes escolhidos e adicionar a uma lista 
def salvar_filmes(lista_filmes):
    with open(filmes_json, "w", encoding="utf-8") as arquivo:
        json.dump(lista_filmes, arquivo, ensure_ascii=False, indent=2)


principal = ctk.CTk()
principal.title("Projeto Filmes")
principal.geometry("300x300")

#funçao para cadastrar o filme
def janela_cadastro():
    janelacad = ctk.CTkInputDialog(text="Janela de Cadastro", title="Janela de Cadastro")
    janelacad.geometry("300x500")
#funçao para salvar as opçoes escolhidas,e notificar se oque esta preenchido esta correto, respeitando as validades  propostas
    def salvar():
        nome = campo_nome.get().upper()
        ano = campo_ano.get()
        if not ano.isdigit() or int(ano) < 1900:
            messagebox.showerror("Erro", "Ano inválido! Use um valor a partir de 1900")
            return

        gener = campo_gener.get().upper()
        try:
            nota = float(campo_nota.get())
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida! Digite um número.")
            return
        if nota < 0 or nota > 10:
            messagebox.showerror("Erro", "Nota inválida! Use uma nota entre 0 a 10")
            return
        #aqui nos adicionamos o nome do filme, ano,nota,genero 
        filmes = ler_filmes()
        filmes.append([nome, ano, gener, nota])
        salvar_filmes(filmes)
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

        campo_ano.delete(0, "end")
        campo_nome.delete(0, "end")
        campo_nota.delete(0, "end")
        campo_gener.delete(0, "end")
    #Aqui criamos algumas menssagens de texto e um botao para salvar
    label_nome = ctk.CTkLabel(janelacad, text="Nome do Filme:")
    label_nome.pack(pady=10)

    campo_nome = ctk.CTkEntry(janelacad, placeholder_text="Digite o nome do filme")
    campo_nome.pack(pady=10)

    label_ano = ctk.CTkLabel(janelacad, text="Ano de lançamento do Filme:")
    label_ano.pack(pady=10)

    campo_ano = ctk.CTkEntry(janelacad, placeholder_text="Digite o ano de lançamento do filme")
    campo_ano.pack(pady=10)

    label_gener = ctk.CTkLabel(janelacad, text="Gênero do Filme:")
    label_gener.pack(pady=10)

    campo_gener = ctk.CTkEntry(janelacad, placeholder_text="Digite o gênero do filme")
    campo_gener.pack(pady=10)

    label_nota = ctk.CTkLabel(janelacad, text="Nota do Filme:")
    label_nota.pack(pady=10)

    campo_nota = ctk.CTkEntry(janelacad, placeholder_text="Digite a nota do filme")
    campo_nota.pack(pady=10)

    botao_salvar = ctk.CTkButton(janelacad, text="Salvar", text_color="white", command=salvar)
    botao_salvar.pack(pady=10)

#Funçao para listar e exibir os filmes que estao salvos na lista 
def janela_listar():
    janelalist = ctk.CTkInputDialog(text="Listar Filmes", title="Listar Filmes")
    janelalist.geometry("300x400")

    label_exibicao = ctk.CTkLabel(janelalist, text=f"Lista dos Filmes: ")
    label_exibicao.pack(pady=10)

    frame_scroll = ctk.CTkScrollableFrame(janelalist, width=320, height=300)
    frame_scroll.pack(padx=10, pady=10, fill="both", expand=True)
#funçao para classificar o filme de acordo com a nota que ele merece se e bom,ruim,regulat e etc
    def classificar_filme(nota):
        if 0 <= nota <= 3.9:
            return "Ruim"
        elif 4 <= nota <= 6.9:
            return "Regular"
        elif 7 <= nota <= 8.9:
            return "Bom"
        elif 9 <= nota <= 10:
            return "Ótimo"
        else:
            return " "

    filmes = ler_filmes()
    if filmes:
        for dados in filmes:
            classificacao = classificar_filme(float(dados[3]))
            label_filme = ctk.CTkLabel(frame_scroll, text=f"Nome: {dados[0]} \nAno: {dados[1]} \nGênero: {dados[2]} \nNota: {dados[3]} \nClassificação: {classificacao}", )
            label_filme.pack(padx=10, pady=10)
    else:
        label_vazio = ctk.CTkLabel(frame_scroll, text="Lista de filmes vazia.")
        label_vazio.pack(padx=10, pady=10)

#funçao para buscar os filmes que ja foram salvos
def janela_buscar():
    janelabusca = ctk.CTkInputDialog(text="Buscar Filmes", title="Buscar Filmes")
    janelabusca.geometry("300x400")

    def buscar():
        buscar_nome = campo_bucar.get().upper()
        resultado = None
        filmes = ler_filmes()
        for dados in filmes:
            if dados[0] == buscar_nome:
                resultado = dados
                break
        if resultado:
            messagebox.showinfo("Resultado",f"Filme encontrado: \nNome: {resultado[0]} \nAno: {resultado[1]} \nGenêro: {resultado[2]} \nNota: {resultado[3]}",)
        else:
            messagebox.showerror("Erro", "Filme não encontrado!")
    #Apos a funçao de buscar, criamos menssagens para serem exibidas, que sao filmes selecionados anteriormente  apos a busca e um botao de "buscar"
    label_bucar = ctk.CTkLabel(janelabusca, text="Buscar filme pelo nome")
    label_bucar.pack(padx=10, pady=10)

    campo_bucar = ctk.CTkEntry(janelabusca, placeholder_text="Digite aqui o nome do filme.")
    campo_bucar.pack(padx=10, pady=10)

    botaobusca = ctk.CTkButton(janelabusca, text="Buscar", command=buscar)
    botaobusca.pack(padx=10, pady=10)

#Funçao para remover os filmes caso deseja trocar para outro filme desejado 
def janela_remover():
    janelaremover = ctk.CTkInputDialog(text="Remover Filmes", title="Remover Filmes")
    janelaremover.geometry("300x400")
#Funçao para remover os filmes que ja foram salvos 
    def remover():
        remover_filme = campo_remover.get().upper()
        filmes = ler_filmes()
        for dados in filmes:
            if dados[0] == remover_filme:
                filmes.remove(dados)
                salvar_filmes(filmes)
                messagebox.showinfo("Sucesso", f"O filme '{remover_filme}' foi removido!")
                campo_remover.delete(0, "end")
                return
        messagebox.showerror("Erro.", "Filme não encontrado!")
    #Apos a funçao de remover, criamos as menssagens de texto para ser exibidas durante o processo, e criamos um botao para remover 
    label_remover = ctk.CTkLabel(janelaremover, text="Remover filme pelo nome")
    label_remover.pack(padx=10, pady=10)

    campo_remover = ctk.CTkEntry(janelaremover, placeholder_text="Digite aqui o nome do filme.")
    campo_remover.pack(padx=10, pady=10)

    botaoremover = ctk.CTkButton(janelaremover, text="Remover", command=remover)
    botaoremover.pack(padx=10, pady=10)

#funçao de estatisticas, que ira nos mostar as notas, filmes escolhidos e genero
def janela_estisticas():
    janelaestatistica = ctk.CTkInputDialog(text="Estatisticas", title="Estatisticas")
    janelaestatistica.geometry("300x400")

    filmes = ler_filmes()
    qtdd_filmes = len(filmes)
    #Aqui definimos as nossas notas para os filmes 
    notas = [float(dados[3]) for dados in filmes] if filmes else []
    media_notas = sum(notas) / len(notas) if notas else 0
    #Aqui definimos os generos dos filmes 
    generos = [dados[2] for dados in filmes] if filmes else []
    genero_maior = Counter(generos).most_common(1)[0][0] if generos else "Nenhum"

    filmes_maior8 = [dados[0] for dados in filmes if float(dados[3]) > 8]
    #Aqui criamos as menssagens de texto para definir, as medias de notas, quantidade de filmes,generos mais cadastrados. 
    label_qtdd = ctk.CTkLabel(janelaestatistica, text=f"Quantidade de filmes salvos: {qtdd_filmes}")
    label_qtdd.pack(padx=10, pady=10)

    label_media = ctk.CTkLabel(janelaestatistica, text=f"Média das notas: {media_notas:.2f}")
    label_media.pack(padx=10, pady=10)

    label_genero = ctk.CTkLabel(janelaestatistica, text=f"Gênero mais cadastrado: {genero_maior}")
    label_genero.pack(padx=10, pady=10)

    label_filmes_maior8 = ctk.CTkLabel(janelaestatistica, text=f"Filmes com nota maior que 8: ")
    label_filmes_maior8.pack(padx=10, pady=10)
    if filmes_maior8:
        for filme in filmes_maior8:
            label_filme = ctk.CTkLabel(janelaestatistica, text=f"- {filme}")
            label_filme.pack(padx=10, pady=10)
    else:
        label_filmes_vazio = ctk.CTkLabel(janelaestatistica, text="Nenhum filme com nota maior que 8.")
        label_filmes_vazio.pack(padx=10, pady=10)

#Aqui nos criamos os botoes para, cadastrar, listar, remover filmes e exibir filmes
botao_cadastro = ctk.CTkButton(principal, text="Cadastrar Filmes", text_color="white", command=janela_cadastro)
botao_cadastro.pack(pady=10)

botao_listar = ctk.CTkButton(principal, text="Listar Filmes", text_color="white", command=janela_listar)
botao_listar.pack(pady=10)

botao_buscar = ctk.CTkButton(principal, text="Buscar Filmes", text_color="white", command=janela_buscar)
botao_buscar.pack(pady=10)

botao_remover = ctk.CTkButton(principal, text="Remover Filmes", text_color="white", command=janela_remover)
botao_remover.pack(pady=10)

botao_exibir = ctk.CTkButton(principal, text="Exibir Filmes", text_color="white", command=janela_estisticas)
botao_exibir.pack(pady=10)

principal.mainloop()
#Kauã Lucas
#Eduardo Henrique Fernandes Ferreira