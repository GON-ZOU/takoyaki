import bs4
import requests
import os
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory
# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, make_response, jsonify, send_file
import base64
# fromでstatistics.pyというモジュール(ファイル)を読み込む、importでstatistics.py内のmean()という関数を読み込む
import statistics
from statistics import mean
import datetime  # datetimeというモジュール(ファイル)を読み込む
XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__, static_folder=None)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'takoyaki'

UPLOAD_FOLDER = './static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def takoyaki():
    return render_template('takoyaki.html')


# GET  /register => 登録画面を表示
# POST /register => 登録処理をする


@app.route('/profile', methods=["GET", "POST"])
def profile():
    #  登録ページを表示させる
    if request.method == "GET":
        return render_template("profile.html")
    # ここからPOSTの処理
    else:
        session['username'] = request.form.get("username")
        session['gu'] = request.form.get("gu")
        session['topping'] = request.form.get("topping")
        session['source'] = request.form.get("source")
        # password = request.form.get("password")
# item = { "id":id, "comment":comment }
        # item = {"id": id, "comment": comment, "postdate": postdate}
        # 画像
        img_file = request.files['img_file']
        # 付け加えたよ
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imgdata = '/static/img/' + filename
            session['imgdata'] = filename
            print(filename)
            # conn = sqlite3.connect('service.db')
            # c = conn.cursor()
            # c.execute("insert into user values(null,?,?,?)",(name,password,imgdata))
            # conn.commit()
            # conn.close()
            # return redirect('/login')
            return redirect('/meishi')
        else:
            return ''' <p>許可されていない拡張子です</p> '''


@app.route('/static/img/<filename>')
def uploaded_file(filename):
    print(session['imgdata'])
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# @app.route('/static/img/<filename>')
# def send_file(filename):
#     return render_template('meishi.html', filename=filename)
# /add ではPOSTを使ったので /edit ではあえてGETを使う


@app.route("/meishi", methods=["GET"])
def meishi():
    print("fuck you!")
    print(session['imgdata'])
    # ブラウザから送られてきたデータを取得
    if "username" in session:
        user_id_py = session["username"]
    if "gu" in session:
        gu_id_py = session["gu"]
    if "topping" in session:
        topping_id_py = session["topping"]
    if "source" in session:
        source_id_py = session["source"]
    if "imgdata" in session:
        file_id_py = session["filename"]
    else:
        print(" <p>許可されていない拡張子です</p> ")
    #     return 'ユーザー名；' + str(session['username'])
    # if "gu" in session:
    #     return '具；' + str(session['gu'])
    # if "topping" in session:
    #     return 'トッピング；' + str(session['topping'])
    # if "source" in session:
    #     return 'ソース；' + str(session['source'])
    # item_id = request.args.get("name")
    # item_png = request.args.get("img_file")  # id
    # print("name")
    print(file_id_py)
    return render_template("meishi.html", username=user_id_py, gu=gu_id_py, topping=topping_id_py, source=source_id_py, img_file=file_id_py)


@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound404(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=True)
