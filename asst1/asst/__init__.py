from flask import Flask, render_template

APP = Flask(__name__, template_folder="views/templates", static_url_path='/static')
APP.secret_key = 'A^*4L#Cs8UjQaq!Hjmhz'

# Register all views after here
# =======================
from asst.views import grid


APP.register_blueprint(grid.page, url_prefix='/')