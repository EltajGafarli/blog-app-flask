from flask import abort
from flask import render_template
from flask import request,redirect,url_for
from models import Tag
from .blueprints import posts
from models import Posts
from .forms import PostForm
from app import db

from flask_security import login_required

from devtools import debug

#url routing
@posts.route('/')
def blogs():
    q = request.args.get('q')
    if q:
        posts = Posts.query.filter(Posts.title.contains(q) | Posts.body.contains(q)).all()
        if not len(posts):
            abort(404)
    else:
        posts = Posts.query.order_by(Posts.created.desc())
        
    if type(posts) == list:
        return render_template('posts/posts.html',posts = posts,pages=None)
    page = request.args.get('page')
    
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page,per_page=2)
    return render_template('posts/posts.html',posts = posts,pages = pages)

@posts.route('/<slug>')
def blog_post_detail(slug):
    post = Posts.query.filter(Posts.slug == slug).first()
    return render_template('posts/post_detail.html',post = post)

@posts.route('tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html',tag = tag,slug = slug.upper())


#forms

@posts.route('create',methods=["GET","POST"])
@login_required
def create_post():
    form = PostForm()
    if request.method == "POST":
        title = form.data.get('title')
        body = form.data.get('body')
        post = Posts(title,body)
        db.session.add(post)
        db.session.commit()
        if "#" in title:
            title = title.replace("#","sharp")
        return redirect(url_for('posts.blog_post_detail',slug=title))
    return render_template('posts/forms.html',form = form)

#update post
@posts.route('/<slug>/edit',methods=["GET","POST"])
@login_required
def update_post(slug):
    post = Posts.query.filter(Posts.slug == slug).first()
    if request.method.lower() == "post":
        form = PostForm(formdata=request.form,obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.blog_post_detail',slug = post.slug))
    
    form = PostForm(obj = post)
    return render_template('posts/edit.html',form=form,post = post)


#error handler
@posts.errorhandler(404)
def not_found_on_db(err):
    return render_template('posts/error.html'),404

posts.register_error_handler(404,not_found_on_db)