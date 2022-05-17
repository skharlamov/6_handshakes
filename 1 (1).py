
# Библиотеки для работы 
import requests # Для get запроса 
from bs4 import BeautifulSoup # Библиотека для парсинга данных

# Вводим данные
start_url       = input("Введите страницу с которой надо начинать: ")
end_url         = input("Введите конечную страницу: ")
rate_limit      = int(input("Введите лимит: "))

def get_language_code(url: str):
    """ Функция для определения языка страницы """
    url = url.split("/")[2] # Разделяем от https
    if url.startswith("wiki"): # Если начинается с wikipedia, значит ставим en
        return "en"
    else: # Иначе то разделяем до точки
        return url.split(".")[0]

# Записываем языковой код
language_code = get_language_code(start_url)
URL = f"https://{language_code}.wikipedia.org"

def get_page_links(url: str) -> list:
    """ Функция для парсинга ссылок (DOM элементов a) с страницы"""
    request = None 
    try:
        request = requests.get(url)
    except:
        pass
    if not request:
        return None 
    soup    = BeautifulSoup(request.content, "lxml")
    links   = []
    for el in soup.find_all("a"):
        href = el.get('href')
        if not href:
            continue
        if href.find("HTTP_404") != -1:
            continue
        if href.startswith('/wiki/') or href.startswith(URL):
            links.append(href)

    return links

def parser(links: list, limit: int):
    """ Рекурсивная функция для парсинга ссылок """
    if limit > rate_limit: # Если превышаем лимит то возвращаем
        return "Не найдено" 

    print(f"Limit: {limit}")

    new_links = []
    # Проходимся по каждой полученной странице
    for el in links:
        url = URL + el
        page_links = get_page_links(url) # Парсим все ссылки с страницы 
        if not page_links: # Если не получилось, то пропускаем
            continue
        for link in page_links: # Пробегаемся по этим ссылкам, если нужная нам то возвращаем
            if link.startswith('/wiki/'):
                link = URL + link
            if link == end_url:
                return ("Найдено", limit, link)
        new_links = new_links + get_page_links(url) # Складываем все ссылки

    return parser(new_links, limit + 1)


print(parser(get_page_links(start_url), 1))