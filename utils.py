import datetime
import json
import os

from OpenNews.models import News, Category, User
from OpenNews import app, db
import hashlib, secrets


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_news(news=None):
    pass


def load_categories(cate=None):
    with app.app_context():
        if cate == None:
            return Category.query.all()
        return Category.query.filter(Category.id == cate).all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))


# def load_user():
#     with app.app_context():
#         return User.query.all()
#
# print(load_user())
# def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
#     # products = read_json(os.path.join(app.root_path, 'data/products.json'))
#     # if cate_id:
#     #     products = [p for p in products if p['category_id'] == int(cate_id)]
#     # if kw:
#     #     products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
#     # if from_price:
#     #     products = [p for p in products if p['price'] >= float(from_price)]
#     # if to_price:
#     #     products = [p for p in products if p['price'] <= float(to_price)]
#     # return products
#     products = Product.query.filter(Product.active.__eq__(True))
#     if cate_id:
#         products = products.filter(Product.category_id.__eq__(cate_id))
#     if kw:
#         products = products.filter(Product.name.contains(kw))
#     if from_price:
#         products = products.filter(Product.price.__ge__(from_price))
#     if to_price:
#         products = products.filter(Product.price.__le__(to_price))
#     return products.all()


# def get_product_by_id(product_id):
#     # products = read_json(os.path.join(app.root_path, 'data/products.json'))
#     # for p in products:
#     #     if p['id'] == product_id:
#     #         return p
#     product = Product.query.get(product_id)
def get_it_by_name_categories(cate=None):
    if cate != None:
        return Category.query.filter(Category.name == cate).one().id
    return None


def add_user(name, username, password, **kwargs):
    salt = secrets.token_hex(16)
    hash_object = hashlib.sha256((password + salt).encode())
    hash_16 = hash_object.hexdigest()
    user = User(name=name.strip(),
                username=username.strip(),
                password=hash_16,
                salt=salt,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    user = User.query.filter(User.username == username).first()
    hash_object = hashlib.sha256((password + user.salt).encode())
    hash_16 = hash_object.hexdigest()
    if hash_16 == user.password:
        return User.query.filter(User.username == username and
                                 User.password == password).first()
    # if username == username and password == password:
    #     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    #
    #     return User.query.filter(User.username == username and
    #                              User.password == password).first()


# add_user(name='Nam', username='Nam', password='abc', email='abcd', avatar='nam.png')
# print(check_login('Phuongnam0212','Phuongnam0212').name)
def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_news(cate=None, date = None):
    with app.app_context():
        if cate == None:
            return News.query.all()
        return News.query.filter(News.image_url.__ne__('NULL') and News.category_id == int(cate) and News.created.date() == date).all()
        # return News.query.all()

# print(load_news(5,7))
# print(load_news(1))
def load_news_id(ID=None):
    return News.query.filter(News.id == ID).first()


# for i in load_news():
#     print(i)
def load_news_categories(id=None):
    return News.query.filter(News.image_url.__ne__('NULL') and News.category_id == id).all()


# print(load_news_categories(get_it_by_name_categories('entertainment')))


def add_news(news=None, cate =None):

    try:
        db.session.add(News(title=news['title'],
                            content=news['content'][:10000],
                            description=news['description'] if news['description'] != None else news['title'],
                            url=news['url'],
                            image_url=news['urlToImage'] if news['urlToImage'] != None else "NULL",
                            author=news['author'] if news['author'] != None else "NULL",
                            created=datetime.datetime.strptime(news['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                            category_id=cate))

        db.session.commit()
    except:
        pass
