from selenium import webdriver

driver =webdriver.Chrome('C:/Users/heber/OneDrive/Documentos/chromedriver.exe')

"""target_url = 'https://www.awebic.com/livros-amazon/'
driver.get(target_url)

livros=driver.find_elements_by_tag_name('li')
for livro in livros:
    print(livro.text)"""


"""target_url = 'https://www.maioresemelhores.com/melhores-filmes-atuais/'
driver.get(target_url)

lista_filmes=driver.find_elements_by_css_selector('h3 em')
for filmes in lista_filmes:
    print(filmes.text)"""


"""target_url = 'https://maistocadas.mus.br/musicas-mais-tocadas/'
driver.get(target_url)

musicas=driver.find_elements_by_class_name('musicas')
for musica in musicas:
    print(musica.text)"""

"""target_url = 'https://www.euamotheatro.com.br/pecasfamosas'
driver.get(target_url)

pecas=driver.find_elements_by_tag_name('strong')
for peca in pecas:
    print(peca.text)"""

target_url = 'https://www.agendartecultura.com.br/noticias/dar-volta-museus/'
driver.get(target_url)

lista_museus=driver.find_elements_by_css_selector('p strong')
for museus in lista_museus:
    print(museus.text)