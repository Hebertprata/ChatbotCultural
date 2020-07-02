import json as js
import numpy as np
import nltk
from nltk.stem.rslp import RSLPStemmer
import tensorflow as tf
import tflearn as tfl
import random
import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from selenium import webdriver

driver =webdriver.Chrome('C:/Users/heber/OneDrive/Documentos/chromedriver.exe')

# Carregando Json
with open("intents.json", encoding='utf-8') as file:
  data = js.load(file)


def inserirItens(tagInsercao,item):
  for intent in data["intents"]:
    if intent["tag"] == tagInsercao:
      intent["responses"].append(item)

target_url = 'https://www.agendartecultura.com.br/noticias/dar-volta-museus/'
driver.get(target_url)

lista_museus=driver.find_elements_by_css_selector('p strong')
for museus in lista_museus:
    inserirItens("museu", museus.text)

target_url = 'https://www.awebic.com/livros-amazon/'
driver.get(target_url)

livros=driver.find_elements_by_tag_name('li')
for livro in livros:
    inserirItens("livros", livro.text)

target_url = 'https://www.maioresemelhores.com/melhores-filmes-atuais/'
driver.get(target_url)

lista_filmes=driver.find_elements_by_css_selector('h3 em')
for filmes in lista_filmes:
    inserirItens("filme", filmes.text)

target_url = 'https://maistocadas.mus.br/musicas-mais-tocadas/'
driver.get(target_url)

musicas=driver.find_elements_by_class_name('musicas')
for musica in musicas:
    inserirItens("musica", musica.text)

target_url = 'https://www.euamotheatro.com.br/pecasfamosas'
driver.get(target_url)

pecas=driver.find_elements_by_tag_name('strong')
for peca in pecas:
    inserirItens("teatro", peca.text)
    

#Preparando os dados  
nltk.download('rslp')
nltk.download('punkt')
palavras = []
intencoes = []
sentencas = []
saidas = []

def cria_audio(text):
  tts = gTTS(text,lang = 'pt')
  #Salva o arquivo de audio
  caminho = 'audios/001.mp3'
  tts.save(caminho)
  #print("Estou aprendendo o que você disse...")
  #Da play ao audio
  playsound(caminho) 
  os.remove(caminho)
  
def ouvir_microfone():
	#Habilita o microfone para ouvir o usuario
	microfone = sr.Recognizer()
	with sr.Microphone() as source:
		#Chama a funcao de reducao de ruido disponivel na speech_recognition
		microfone.adjust_for_ambient_noise(source)
		#Avisa ao usuario que esta pronto para ouvir
		#print("Diga alguma coisa: ")
		#Armazena a informacao de audio na variavel
		audio = microfone.listen(source)

	try:
		#Passa o audio para o reconhecedor de padroes do speech_recognition
		frase = microfone.recognize_google(audio,language='pt-BR')
		#Após alguns segundos, retorna a frase falada
		#print("Você disse: " + frase)
  
		

		#Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
	except sr.UnknownValueError:
		cria_audio("Não entendi")

	return frase


for intent in data["intents"]:
  
  tag = intent['tag'] 

  if tag not in intencoes:
     intencoes.append(tag)

  for pattern in intent["patterns"]:
    wrds = nltk.word_tokenize(pattern, language='portuguese')
    palavras.extend(wrds)
    sentencas.append(wrds)
    saidas.append(tag)
#Stemming
stemer = RSLPStemmer()

stemmed_words = [stemer.stem(w.lower()) for w in palavras]
stemmed_words = sorted(list(set(stemmed_words)))
#Bag of Words
training = []
output = []
outputEmpty = [0 for _ in range(len(intencoes))]

for x, frase in enumerate(sentencas):
  bag = []
  wds = [stemer.stem(k.lower()) for k in frase]
  for w in stemmed_words:
    if w in wds:
      bag.append(1)
    else:
      bag.append(0)

  outputRow = outputEmpty[:]
  outputRow[intencoes.index(saidas[x])] = 1

  training.append(bag)  
  output.append(outputRow)
#Rede Neural
training = np.array(training)
output = np.array(output)

tf.reset_default_graph()
net = tfl.input_data(shape=[None, len(training[0])])
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, len(output[0]), activation="softmax")
net = tfl.regression(net)
model = tfl.DNN(net)
#Treinamento
model.fit(training, output, n_epoch=300, batch_size=8, show_metric=True)
model.save("model.chatbot30G")
#Bot
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return np.array(bag)

def chat():
    #print("Bem vindo ao Bot Cultural")
    cria_audio('Bem vindo ao Bot Cultural, pode falar estou ouvindo')
    Online = True
    while Online:
        inp = ouvir_microfone()
        bag_usuario = bag_of_words(inp, stemmed_words)
        results = model.predict([bag_usuario])
        results_index = np.argmax(results)
        tag = intencoes[results_index]
        maximo=results.max()
        if maximo>0.15:
          

         for tg in data["intents"]:
             if tg['tag'] == tag:
                 responses = tg['responses']

         #print(random.choice(responses))
         cria_audio(random.choice(responses))

         if tag == "ate-mais":
             Online = False
        else:
          cria_audio('Não entendi, pode repetir?')
chat()

  