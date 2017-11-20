from flask import Blueprint

mod_blog=Blueprint('mod_blog',__name__)

from . import views