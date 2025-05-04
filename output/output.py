from bs4 import BeautifulSoup

class Output:
    # テーブル要素を全て出力するメソッド
    def outputTable(self, soup:BeautifulSoup):
        # table要素を全て取得
        tables = soup.find_all('table')
        with open('output/tables.txt', 'w', encoding='utf-8') as f:
            for i, table in enumerate(tables, 1):
                f.write(f"Table {i}:\n")
                f.write(table.prettify())
                f.write('\n' + '-'*40 + '\n')

    # テーブル要素をクラス指定して全て出力するメソッド
    def outputTableForClass(self, soup:BeautifulSoup, class_name:str):
        # table要素を全て取得
        tables = soup.find_all('table', class_=class_name)
        with open('output/tables.txt', 'w', encoding='utf-8') as f:
            for i, table in enumerate(tables, 1):
                f.write(f"Table {i}:\n")
                f.write(table.prettify())
                f.write('\n' + '-'*40 + '\n')

    # テーブル要素をクラス指定して全て出力するメソッド
    def outputTableForId(self, soup:BeautifulSoup, id:str):
        # table要素を全て取得
        tables = soup.find_all('table', id=id)
        with open('output/tables.txt', 'w', encoding='utf-8') as f:
            for i, table in enumerate(tables, 1):
                f.write(f"Table {i}:\n")
                f.write(table.prettify())
                f.write('\n' + '-'*40 + '\n')

    # Div要素を全て出力するメソッド
    def outputDiv(self, soup:BeautifulSoup):
        # Div要素を全て取得
        divs = soup.find_all('div')
        with open('output/divs.txt', 'w', encoding='utf-8') as f:
            for i, div in enumerate(divs, 1):
                f.write(f"Div {i}:\n")
                f.write(div.prettify())
                f.write('\n' + '-'*40 + '\n')

    # Div要素をクラス名で指定して全て出力するメソッド
    def outputDivForClass(self, soup:BeautifulSoup, className:str):
        # Div要素を全て取得
        divs = soup.find_all('div', class_=className)
        with open('output/divs.txt', 'w', encoding='utf-8') as f:
            for i, div in enumerate(divs, 1):
                f.write(f"Div {i}:\n")
                f.write(div.prettify())
                f.write('\n' + '-'*40 + '\n')