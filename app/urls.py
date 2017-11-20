from . import app 
from .mod_user import mod_user as user_blueprint
from .main import main as main_blueprint
from .mod_blog import mod_blog as blog_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(blog_blueprint)