from bs4 import BeautifulSoup
import requests
import pyodbc

class crawl:
    title = []
    news = []

    def source(self , link):
        self.title = []
        self.news = []

        for i in range(1,11):
          page = requests.get(link + f"{i}")
          soup = BeautifulSoup(page.content ,'html.parser')
          news = soup.find_all('article',{'class':'list-item'})
          for new in news:
            self.crawling(new)
            
        self.save()

    def crawling(self , source):
        try :
            self.title.append(source.find('h2',{'class':'title'}).text.replace('\u200c',' ').strip())
        except :
            self.title.append(None)
        try :
            self.news.append(source.find('article',{'class':'list-item'}).find('h4',{'class':'lead'}).text.replace('\u200c',' ').strip())
        except :
            self.news.append(None)
    
    def save(self):
        server = '.'
        driver = '{ODBC Driver 17 for SQL Server}'
        try:
            # Create News Database if not already exist
            connection = f'DRIVER={driver};SERVER={server};DATABASE=master;Trusted_Connection=yes;'
            conn = pyodbc.connect(connection, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sys.databases WHERE name = 'News' ;")
            if cursor.fetchone():
                print(f"Database '{'News'}' already exists.")
            else:
                cursor.execute("CREATE DATABASE 'News' ;")
                print(f"Database 'News' created successfully.")
            # Create News table if not already exist
            connection = f'DRIVER={driver};SERVER={server};DATABASE=News;Trusted_Connection=yes;'
            conn = pyodbc.connect(connection, autocommit=True)
            cursor = conn.cursor()
            cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'News';")
            if cursor.fetchone():
                print(f"Table 'News' already exists.")
            else:
                cursor.execute("CREATE TABLE News (ID INT IDENTITY(1, 1) PRIMARY KEY,Titles ntext,Text ntext);")
                print("Table 'News' created successfully.")
            for i in range(len(self.title)):
                try:
                    cursor.execute("INSERT INTO News (Titles, Text) VALUES (?, ?);", self.title[i], self.news[i])
                except pyodbc.Error as e:
                    print(f"An error occurred while inserting row {i}: {e}")
            print("All data inserted successfully.")
        except pyodbc.Error as e:
            print("An error occurred:", e)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
                
        
ob = crawl()
ob.source('https://www.tasnimnews.com/fa/top-stories?page=')