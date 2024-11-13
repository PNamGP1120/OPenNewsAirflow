import json
import os

from OpenNews import utils
import news_data
# import mysql.connector
# from mysql.connector import Error

# def connect_to_database():
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="news_data"
#         )
#         return connection
#     except Error as e:
#         print(f"Error: {e}")
#         return None

# def insert_article(connection, article, category):
#     cursor = connection.cursor()
#
#     cursor.execute("""
#         INSERT INTO articles (source_name, author, title, description, url, urlToImage, publishedAt, content, category)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """, (
#         article["source"]["name"],
#         article.get("author"),
#         article.get("title"),
#         article.get("description"),
#         article.get("url"),
#         article.get("urlToImage"),
#         article.get("publishedAt"),
#         article.get("content"),
#         category
#     ))
#     connection.commit()

def load_articles(file_path, category):

    with open(file_path, encoding='utf-8') as f:
        articles_data = json.load(f)["articles"]
    # print(articles_data)


    for a in articles_data:
        utils.add_news(a,category)


def main():
    category_files = {
        "news_data\\news.json": 7,
        "news_data\\technology_news.json": 6,
        "news_data\\entertainment_news.json" : 2,
        "news_data\\business_news.json": 1,
        "news_data\\sports_news.json": 5,
        "news_data\\politic_news.json" : 4,
        "news_data\\health_news.json" : 3
    }
    from pathlib import Path
    current_directory = Path.cwd()
    for file_name, category in category_files.items():
        print(f"Processing {file_name} as {category}")
        load_articles(current_directory.parent / file_name, category)

if __name__ == "__main__":

    main()