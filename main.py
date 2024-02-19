import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get('https://books.toscrape.com/')


def conexao():
    if response.status_code == 200:
        print('\nConexão Estabelecida')
    else:
        print('ERRO')


conexao()


def coleta_de_categorias():
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    categorias = site.find('div', class_='side_categories').find_all('ul')[1].find_all('a')

    print('Categorias Disponíveis:')
    for i, categoria in enumerate(categorias, start=1):
        print(f'{i}. {categoria.text.strip()}')

    escolha_categoria = int(input('\nEscolha o número da categoria desejada (ou digite 0 para todas): '))

    if 0 <= escolha_categoria <= len(categorias):
        if escolha_categoria == 0:
            categorias_escolhidas = categorias
        else:
            categorias_escolhidas = [categorias[escolha_categoria - 1]]

        livros_total = []

        for categoria_escolhida in categorias_escolhidas:
            url_categoria = categoria_escolhida['href']
            response_categoria = requests.get(f'https://books.toscrape.com/{url_categoria}')
            if response_categoria.status_code == 200:
                site_categoria = BeautifulSoup(response_categoria.content, 'html.parser')
                livros = site_categoria.find_all('article', class_='product_pod')

                if livros:
                    for livro in livros:
                        titulo_livro = livro.h3.a['title']
                        preco_livro = livro.find('p', class_='price_color').text.strip()
                        avaliacao_livro = livro.find('p', class_='star-rating')['class'][1]

                        livros_total.append({'Título': titulo_livro, 'Preço': preco_livro, 'Avaliação': avaliacao_livro})

        df = pd.DataFrame(livros_total)
        nome_arquivo = 'livros.xlsx'
        df.to_excel(nome_arquivo, index=False)
        print(f'\nOs dados foram exportados para o arquivo "{nome_arquivo}" com sucesso!')

    else:
        print('Escolha de categoria inválida.')


coleta_de_categorias()
