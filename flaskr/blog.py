from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flask_mongoengine.wtf import model_form

from werkzeug.exceptions import abort

from flask_login import login_required, current_user

import datetime

bp = Blueprint('blog', __name__)

from .models import Post
PostForm = model_form(Post, field_args={'title': {'textarea': True}, 'body': {'textarea': True}})

@bp.route('/')
def index():
    posts = Post.objects()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm(request.form)
    if request.method == 'POST':
        user=current_user.to_dbref()
        Post(title=form.title.data, body=form.body.data, author=user).save()
        return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<string:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = PostForm(request.form)
    post=None
    try:
        post = Post.find(id=id)
    finally:
        if post is None:
            abort(404, "Post id {0} doesn't exist.".format(id))
    
        if post.author.user_id != current_user.user_id:
            abort(403)

    if request.method == 'POST':
        post.update(title=form.title.data, body=form.body.data, created = datetime.datetime.utcnow() + datetime.timedelta(hours=9))

        return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    post=Post.find(id=id)
    post.delete()
    return redirect(url_for('blog.index'))