# --Bibliotecas necessárias para o funcionamento do Remy-----------------------------------------------------------------
from sklearn.model_selection import train_test_split # divide o dataset em treino e teste
from sklearn.ensemble import RandomForestClassifier # cria varias árvores de decisão para uma previsão mais potente
from sklearn.metrics import accuracy_score, classification_report # acurácia e relatorio do modelo
from imblearn.over_sampling import ADASYN # favorece dados em menor quantidade no dataset
import pandas as pd # manipulação do dataset
import pyttsx3 # dá voz pro Remy
import json # estetica do dicionário dos parâmetros do vinho na saída
import streamlit as st

# --O Remy---------------------------------------------------------------------------------------------------------------
class Remy:
    # --Inicializa o Remy----------------------------------------------
    def __init__(self):

        # Define o atributo remy
        self.__remy = RandomForestClassifier(class_weight= "balanced", max_depth= 7, n_estimators=600, random_state=42)
        # lista com os parâmetros que vai aparecer na saída
        self.__keys = ["acidez fixa","acidez volátil","ácido cítrico","açúcar residual","cloretos","dióxido de enxofre livre","dióxido de enxofre total","densidade","pH","sulfatos","álcool"]


    # --Classifica o tipo do vinho entre branco e tinto a partir do parâmetro "dados"-------------
    def __Tipo(self, dados: list):
        # caminho do dataset que contem todos os vinhos
        dataset = "IA/datasets/qualidade_vinho.csv"

        # ler o dataset e guarda em df_v
        df = pd.read_csv(dataset)
        df_v = df

        # variaveis que vão ser usadas para o 1º treino do Remy
        x = [] # dados de estudo
        y = [] # resposta
        parametros = df_v.drop(columns=["quality", "tipo"]) # retirando as colunas "quality" e "tipo" do dataset
        tipo = df_v["tipo"] # entregando apenas a coluna "tipo" do dataset

        # preenchendo as variaveis "x" e "y" com as variaveis "parametros" e "tipos" respectivamente
        for i in range(len(df_v["tipo"])):
            x.append(parametros.loc[i].values)
            y.append(tipo.loc[i])

        # faz o balanceamento dos dados do dataset
        adasyn = ADASYN(random_state=42)
        x_new, y_new = adasyn.fit_resample(x, y)

        # faz o treino do Remy
        x_treino, x_teste, y_treino, y_teste = train_test_split(x_new, y_new, test_size= 0.2, random_state=42)

        # aprendizado do remy a partir do treino
        self.__remy.fit(x_new, y_new)
        
        # previsão do Remy a partir dos dados do vinho inseridos no parâmetro "dados"
        classe = self.__remy.predict([dados])[0]
        return classe # retorno da previsão do Remy
    

    # --Classifica a qualidade do vinho a partir do parâmetro "tipo_vinho"-----------------------------
    def __Qualidade(self, tipo_vinho):
        # escolhe o dataset com base no tipo do vinho
        if tipo_vinho == "tinto":
        # caminho do dataset que contem os vinhos tintos
            dataset_red = "IA/datasets/qualidade_vinho_vermelho.csv"
        else:
        # caminho do dataset que contem os vinhos brancos
            dataset_red = "IA/datasets/qualidade_vinho_branco.csv"
        
        # ler o dataset e guarda em df_vinho
        df = pd.read_csv(dataset_red)
        df_vinho = df

        # variaveis que vão ser usadas para o 2º treino do Remy
        x = [] # dados de estudo
        y = [] # resposta
        parametros = df_vinho.drop(columns=["quality", "tipo"]) # retirando as colunas "quality" e "tipo" do dataset
        quality = df_vinho["quality"] # entregando apenas a coluna "quality" do dataset

        # preenchendo as variaveis "x" e "y" com as variaveis "parametros" e "quality" respectivamente
        for i in range(len(df_vinho["quality"])):
            x.append(parametros.loc[i].values)

            # divide a qualidade em "alta", "média" e "baixa" com base no número na coluna "quality"
            if quality.loc[i].is_integer():
                if quality.loc[i] >= 7:
                    y.append("alta") # se o número > ou = a 7

                elif quality.loc[i] > 5 <= 6:
                    y.append("média") # se o número = 6
                else:
                    y.append("baixa") # se o número < 6 

        # faz o treino do Remy
        x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size= 0.2, random_state=42)

        # aprendizado do remy a partir do treino
        self.__remy.fit(x_treino, y_treino)

        # faz uma previsão com base na variável "x_teste"
        y_previsao = self.__remy.predict(x_teste)        
        return y_teste, y_previsao # retorna a resposta de "x_teste" e a previsão

    
    def Analizar(self, dados: list):
        tipo_vinho = self.__Tipo(dados) # retorna o tipo do vinho
        y_teste, y_previsao = self.__Qualidade(tipo_vinho) # faz o treinamento para a qualidade

        # junta a lista do parâmetro dados com o atributo "__keys" e converte para um dicionário
        parametros = dict(zip(self.__keys, dados))

        # faz a previsão do vinho inserido pelo do parâmetro "dados"
        qualidade = self.__remy.predict([dados])[0]

        engine = pyttsx3.init() # cria um objeto de engine de voz
        voices = engine.getProperty('voices') # pega a lista de vozes disponíveis no sistema
        engine.setProperty('voice', voices[0].id) # define qual voz será usada
        
        # transforma todo o texto em voz
        engine.say(f"Vinho {tipo_vinho} Reconhecido. Parametros analisados: {parametros}. Qualidade prevista para o vinho: {qualidade}. Acurácia do modelo Remy: {accuracy_score(y_teste, y_previsao) * 100:.1f}%")
        
        # espera terminar
        engine.runAndWait()

        # para
        engine.stop()
        
        return f"Vinho {tipo_vinho} Reconhecido.", f"Parametros analisados: {json.dumps(parametros, indent=4, ensure_ascii=False)}.", f"Qualidade prevista para o vinho: {qualidade}", f"Acurácia do modelo Remy: {accuracy_score(y_teste, y_previsao) * 100:.1f}%"
    
    
    # --passa um relatorio do modelo Remy------------------------------
    def Relatorio(self, dados: list):
        tipo_vinho = self.__Tipo(dados) # retorna o tipo do vinho
        y_teste, y_previsao = self.__Qualidade(tipo_vinho) # faz o treinamento para a qualidade

        engine = pyttsx3.init() # cria um objeto de engine de voz
        voices = engine.getProperty('voices') # pega a lista de vozes disponíveis no sistema
        engine.setProperty('voice', voices[0].id) # define qual voz será usada
        
        print(" Modelo Remy ")
        print(f"Relatório de classificação do modelo Remy:\n{classification_report(y_teste, y_previsao)}") # mostra o relatorio

        # transforma todo o relatorio em voz
        engine.say(f"Relatório de classificação do modelo Remy:\n{classification_report(y_teste, y_previsao)}")
        
        # espera terminar
        engine.runAndWait()

        # para
        engine.stop()

