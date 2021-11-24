from flask import Flask, request, render_template, jsonify
from models.models import session, Menu, Category
import random


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adult')
def adult():
    return render_template('adult.html')


# Category for Member
@app.route('/api/category/<id>', methods=['GET'])
def get_category(id):
    return get_category_records(id=id)


@app.route('/api/category', methods=['GET'])
def get_categories():
    return get_category_records()


# Category for Adult
@app.route('/api/v1/category/<id>', methods=['GET'])
def get_category_v1(id):
    return get_category_records(id=id, adult=True)


@app.route('/api/v1/category', methods=['GET'])
def get_categories_v1():
    return get_category_records(adult=True)


# Menu for Member
@app.route('/api/menu/<id>', methods=['GET'])
def get_menu(id):
    return get_menu_records(id=id)


@app.route('/api/menu', methods=['GET'])
def get_menus():
    params = request.args
    return get_menu_records(params=params)


# Menu for Adult
@app.route('/api/v1/menu/<id>', methods=['GET'])
def get_menu_v1(id):
    return get_menu_records(id=id, adult=True)


@app.route('/api/v1/menu', methods=['GET'])
def get_menus_v1():
    params = request.args
    return get_menu_records(params=params, adult=True)


# Info
@app.route('/api/v1', methods=['GET'])
def get_api_list():
    body = [
        {
            "name": "Category API",
            "endpoint": "/api/v1/category"
        },
        {
            "name": "Menu API",
            "endpoint": "/api/v1/menu"
        }
    ]
    return send_response(data=body)


# Error Handler
@app.errorhandler(400)
def bad_request(e):
    error = '400 Bad Request'
    title = '無効なリクエストです'
    message = 'ブラウザのキャッシュが影響している可能性があります。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 400

@app.errorhandler(403)
def forbidden(e):
    error = '403 Forbidden'
    title = 'アクセス権がありません'
    message = '管理者にお問合せください。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 403

@app.errorhandler(404)
def not_found(e):
    error = '404 Not Found'
    title = 'お探しのページは<br class="sp">見つかりませんでした'
    message = 'URLが正しいことを確認してください。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 404

@app.errorhandler(408)
def not_found(e):
    error = '408 Request Timeout'
    title = 'リクエストが<br class="sp">タイムアウトしました'
    message = 'しばらくしてから再度お試しください。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 408

@app.errorhandler(500)
def internal_server_error(e):
    error = '500 Internal Server Error'
    title = 'サーバーで<br class="sp">エラーが発生しました'
    message = '管理者にお問合せください。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 500

@app.errorhandler(502)
def bad_gateway(e):
    error = '502 Bad Gateway'
    title = 'ゲートウェイで<br class="sp">エラーが発生しました'
    message = '管理者にお問合せください。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 502

@app.errorhandler(503)
def service_unavailable(e):
    error = '503 Service Unavailable'
    title = 'アクセスが<br class="sp">集中しています'
    message = 'しばらくしてから再度お試しください。'
    image = True if random.random() > 0.5 else False
    return render_template('page_error.html', error=error, title=title, message=message, image=image), 503


# functions
def get_category_records(id=None, adult=False):

    resp = None
    if id is not None:
        resp = [session.query(Category).get(id)]
    else:
        resp = session.query(Category).all()

    if not adult:
        resp = remove_alcohol(resp)

    def to_json(record):
        return {
            'id': record.id,
            'category_id': record.category_id,
            'category': record.category,
            'category_name': record.category_name
        }

    resp = list(map(to_json, resp))

    return send_response(data=resp, adult=adult)


def get_menu_records(id=None, params=None, adult=False):
    query = params.get('query') if params is not None else None
    name = params.get('name') if params is not None else None
    category_id = params.get('category_id') if params is not None else None
    price = params.get('price') if params is not None else None

    resp = None
    if id is not None:
        resp = [session.query(Menu).get(id)]
    elif query is not None:
        query_str = "select * from menus where {0} order by id asc"\
            .format(query)
        print(query_str)
        resp = session.execute(query_str)
    elif name is not None or category_id is not None or price is not None:
        q = ""
        if name is not None:
            s = "name like '%{0}%'".format(name)
            q = q + s if not q else q + " and " + s
        if category_id is not None:
            s = "category_id == {0}".format(category_id)
            q = q + s if not q else q + " and " + s
        if price is not None:
            s = "price == {0}".format(price)
            q = q + s if not q else q + " and " + s

        query_str = "select * from menus m, categories s where m.category_id = s.category_id and {0} order by id asc"\
            .format(q)
        resp = session.execute(query_str).all()
    else:
        resp = session.query(Menu).all()

    if not adult:
        resp = remove_alcohol(resp)

    def to_json(record):
        return {
            'id': record.id,
            'name': record.name,
            'category_id': record.category_id,
            'category_name': record.category,
            'price': record.price,
        }

    resp = list(map(to_json, resp))

    return send_response(data=resp, adult=adult)


def remove_alcohol(records):
    ALCOHOL = 'd-00'
    resp = []
    for r in records:
        if r.category_id != ALCOHOL:
            resp.append(r)

    return resp


def send_response(data=[], adult=False):
    body = {
        "result": data if len(data) != 1 else data[0],
        "response": True
    }
    if adult:
        body["adult"] = True
    if len(data) == 0:
        body["message"] = '条件にヒットするレコードはありませんでした。'

    return jsonify(body), 200


if __name__ == '__main__':
    app.run()
