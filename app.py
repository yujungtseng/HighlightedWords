import os
import imgToStr
import resizeImg
import crawler
from flask import Flask, request, redirect, url_for, render_template
import readJson

UPLOAD_FOLDER = '/static/upload'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

app = Flask(__name__, static_folder="static/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_SIZE'] = 5 * 1024 * 1024  # 5MB


@app.route('/history')
def history():
    word = readJson.select('data.json')
    return render_template('memorizeWord.html', words=word)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/intro")
def intro():
    return render_template('intro.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['POST', 'GET'])
def upload_picture():
    if request.method == "POST":
        picture = request.files['picture']
        if request.form['history'] == 'history':
            history = True
        else:
            history = False
        if picture.filename == '':
            return render_template('index.html', warning_msg="You didn't upload picture.")
        if allowed_file(picture.filename) == False:
            return render_template('index.html', warning_msg="Allowed filetype : jpg, png, jpeg")
        if picture and allowed_file(picture.filename):
            path = os.path.join('static', 'upload', picture.filename)
            picture.save(path)
            words = imgToStr.ImgToStr(path)
            if history == True:
                readJson.insertData(words, 'data.json')
            translate = crawler.Translate(words)
            resizeImg.resize(path)
            # print(translate[0][1]['translate'][0])
            # print(type(translate[0][1]['translate'][0]))
            return render_template('index.html', translation=translate, picture_path=picture.filename)


if __name__ == "__main__":
    app.run(debug=True)
