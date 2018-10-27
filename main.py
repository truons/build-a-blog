from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blogg:root@localhost:3306/build-a-blogg'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()

    return render_template('blog.html', title="Build a Blog", blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    # blog_id = int(request.form['blog-id'])
    # blog = Blog.query.get(blog_id)
    # blog.completed = True
    # db.session.add(blog)
    # db.session.commit()

    # return redirect('/')

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        blog = Blog(title, body)

        title_error = ''
        body_error = ''

        if not title.strip():
            title_error = 'Enter in a title'

        if not body.strip():
            body_error = 'Please enter in the body'

        if not title_error and not body_error:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?id={0}'.format(new_blog.id))
        else:
            return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)
    if request.method == 'GET':
        return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blog_index():
    
    # blog_name = request.form['blog']
    # new_post = Blog(blog_name)
    # db.session.add(new_post)
    # db.session.commit()

    # blogs = Blog.query.filter_by(body=False).all()
    # completed_blogs = Blog.query.filter_by(body=True).all()
    # return render_template('newblog.html',title="Bluid A Blog", 
    # blogs=blogs, completed_blogs=completed_blogs)

    if request.args.get("id"):
        blog = Blog.query.filter_by(id = request.args.get("id")).first()
        return render_template('singpost.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
    
if __name__ == '__main__':
    app.run()