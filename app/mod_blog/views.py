from flask import render_template,request,session,g,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from app.main import main
from app.mod_user.models import User,Blog
from app import db
from . import mod_blog
from .forms import BlogForm


@mod_blog.route('/addblog',methods=['GET','POST'])
@login_required
def add_blog():
	""" 
		view for creating blog on post and rendered add blog template on get method 
	
	"""

	blogform = BlogForm()

	if blogform.validate_on_submit():
		
		if blogform.publication_date.data:
			blog = Blog(title=blogform.title.data,
						content=blogform.content.data,
						publication_date=blogform.publication_date.data,
						author=current_user)
		else:
			blog = Blog(title=blogform.title.data,
						content=blogform.content.data,
						author=current_user)


		db.session.add(blog)
		db.session.commit()
		flash('Added blog successfully')
		return redirect(url_for('main.index'))	
			
	return render_template('addblog.html',form=blogform) 

@mod_blog.route('/listblog')
@login_required
def list_blog():
	""" 
		view for listing blog 
	
	"""
	
	blogs = current_user.blogs.all()

	return render_template('listblog.html',blogs=blogs)

@mod_blog.route('/deleteblog/<int:id>')
@login_required	
def delete_blog(id):
	""" 
		view for deleting blog

	"""

	blog=Blog.query.filter_by(id=id).first()
	if blog:
		db.session.delete(blog)
		db.session.commit()
		flash('Blog Deleted Successfully')
		return redirect(url_for('.list_blog'))

@mod_blog.route('/editblog/<int:id>',methods=['GET','POST'])
@login_required
def edit_blog(id):
	"""
		view for editing blog

	"""
	blog= Blog.query.filter_by(id=id).first()
	blogform =BlogForm()
	if blogform.validate_on_submit():
		blog= Blog.query.filter_by(id=id).first()
		blog.title = blogform.title.data
		blog.content = blogform.content.data
		blog.publication_date = blogform.publication_date.data
		db.session.commit()
		flash('Blog Updated Successfully')
		return redirect(url_for('.list_blog'))

	else:			
		blogform.title.data=blog.title
		blogform.content.data = blog.content
		blogform.publication_date.data = blog.publication_date
	
	return render_template('editblog.html',form=blogform)
	
@mod_blog.route('/detailblog/<int:id>',methods=['GET'])
@login_required
def detail_blog(id):
	""" 
		view for getting blog detail
	
	"""

	blog= Blog.query.filter_by(id=id).first()
	if blog:
		return render_template('detailblog.html',blog=blog)	

@mod_blog.route('/allblog',methods=['GET'])
@login_required
def all_blog():
	""" 
		view for retriving all blog
	
	"""

	blogs = Blog.query.all()
	return render_template('allblog.html',blogs=blogs)