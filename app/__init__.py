from flask import Flask

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
app = Flask(
    __name__,
    static_folder=os.path.join(CUR_DIR, 'static'),
    template_folder=os.path.join(CUR_DIR, 'templates'))
app.config.update(
    DEBUG=True
)

app = Flask(__name__)

from app import views
