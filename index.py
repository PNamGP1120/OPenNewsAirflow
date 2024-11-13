from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cloudinary.uploader
from OpenNews import app, utils, login, limiter
import requests
from plugins import news_database

@app.context_processor
def common_processor():
    return {
        'cates': utils.load_categories(),
    }


@app.route('/')
def home():
    # news_database.main()
    news = utils.load_news(7)

    return render_template('index.html', news=news)
    # cates = utils.load_categories()
    # cate_id = request.args.get('category_id')
    # kw = request.args.get('keyword')
    # products = utils.load_products(cate_id=cate_id, kw=kw)
    # return render_template('index.html', categories=cates, products=products)


@app.route('/<string:category>')
def news_cate(category):
    cates = utils.load_news_categories(utils.get_it_by_name_categories(category))
    return render_template('index.html', news=cates)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def register():
    error = ""
    if request.method == 'POST':
        name = request.form.get('name')

        username = request.form.get('username')
        password = request.form.get('password')
        if password.__len__() < 3:
            error = "Password must be at least 3 characters"
            return url_for('register')
        email = request.form.get('email')
        repassword = request.form.get('repassword')
        avatar_path = None
        try:
            if password.strip() == repassword.strip():
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('login'))
            else:
                error = "Passwords do not match"
        except Exception as e:
            error = 'He thong co lôi' + str(e)

    return render_template('register.html', error=error)

    # @app.route('/products')
    # def product_list():
    #     cate_id = request.args.get("category_id")
    #     kw = request.args.get("keyword")
    #     from_price = request.args.get("from_price")
    #     to_price = request.args.get("to_price")
    #
    #     products = utils.load_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)
    #     return render_template('products.html', products=products)
    #
    #
    # @app.route('/products/<int:product_id>')
    # def product_detail(product_id):
    #     product = utils.get_product_by_id(product_id)
    #     return render_template('product_detail.html', product=product)


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/login", methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    error = ""
    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        # Kiểm tra reCAPTCHA đã check
        if not recaptcha_response:
            return "Vui lòng xác nhận reCAPTCHA!", 400
        # Gửi yêu cầu kiểm tra reCAPTCHA tới Google
        payload = {
            'secret': '6Lc3qHwqAAAAACcr37fTTfTNeuginV5s91AxTpnE',  # mã recaptcha secret key
            'response': recaptcha_response
        }
        # Gửi POST request đến Google API để xác thực reCAPTCHA
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        result = response.json()

        if result.get("success"):
            username = request.form.get("username")
            password = request.form.get("password")
            print(username,password)
            user = utils.check_login(username, password)
            if user:
                login_user(user)
                return redirect(url_for('home'))
            else:
                error = "Invalid username or password"



        else:
            return "Xác thực reCAPTCHA không thành công. Vui lòng thử lại!", 400
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/news/<int:id>', methods=['GET', 'POST'])
def news(id):
    new = utils.load_news_id(id)
    new2 = utils.load_news_id(id + 1)
    return render_template('content-news.html', news=new, new2=new2)


@app.route('/dashboard')
# @login_required
def dashboard():
    return f'Chào mừng, {current_user.username}!'


if __name__ == '__main__':
    from OpenNews.admin import *

    app.run(debug=False)
