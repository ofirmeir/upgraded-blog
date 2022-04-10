from flask import Flask, render_template, request
import requests

BIN_URL = 'https://api.npoint.io/7b5be441e2670e15f75a'
all_posts = None

app = Flask(__name__)


def get_posts():
    global all_posts
    response = requests.get(BIN_URL)
    all_posts = response.json()


@app.route('/')
def hello():
    get_posts()
    return render_template("index.html", posts=all_posts)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", message_sent=False)
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phone-number"]
        message = request.form['message']
        print(f"{name}\n{email}\n{phone_number}\n{message}")
        return render_template("contact.html", message_sent=True)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<int:id>')
def show_post(id):
    for post in all_posts:
        if post["id"] == id:
            post_to_show = post
            return render_template('post.html', post_title=post_to_show['title'],
                                   post_subtitle=post_to_show['subtitle'], post_author=post_to_show['author'],
                                   post_date=post_to_show['date'], post_body=post_to_show['body'])


@app.route('/form_entry', methods=["POST"])
def receive_data():
    name = request.form["name"]
    email = request.form["email"]
    phone_number = request.form["phone-number"]
    message = request.form['message']
    print(f"{name}\n{email}\n{phone_number}\n{message}")
    return "<h1>Successfuly sent your message</h1>"


if __name__ == '__main__':
    app.run(debug=True)
