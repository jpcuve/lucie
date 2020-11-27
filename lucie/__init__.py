import logging
import os

from flask import Flask, redirect, url_for, current_app

LUCIE_CONFIGURATION_LOCATION = 'LUCIE_CONFIG'


def create_app() -> Flask:
    app = Flask(__name__)
    # lecture de la config à partir de config.py dans le répertoire racine... les defauts
    app.config.from_object('config')
    # lecture de la config à partir du fichier pointé par la variable d'environnement LUCIE_CONFIG, si elle existe
    # les paramètres redéfinis écrasent les existants. Ceci est pour permettre d'utiliser un fichier de config de prod.
    if LUCIE_CONFIGURATION_LOCATION is os.environ.keys():
        app.config.from_envvar(LUCIE_CONFIGURATION_LOCATION)
    # setup du niveau du debugging, avec son niveau suivant l'environnement de développement ou production
    app.development = app.config['ENV'] == 'development'  # variable interne de flask
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG if app.development else logging.INFO)
    # à partir d'ici, tout logger via app.logger (ou 'current_app.logger' si tu es dans le contexte d'une requete)
    app.logger.info(f"Configuration lue, par exemple A={app.config['A']}")
    # initialisation de la db (les variables de config vont être utilisées)
    from lucie.database import db
    db.init_app(app)
    # integration des blueprint (end-points http) dans l'application flask
    from lucie.api import api_web
    app.register_blueprint(api_web.bp)

    @app.before_first_request
    def init():
        # en phase de dévelopement, je crée une db manuellement et j'y injecte quelques données
        if app.development:
            connection = db.engine.connect()
            with current_app.open_resource('init.sql', 'rb') as resource:
                sql = str(resource.read(), 'utf8')
                for statement in sql.split(';'):
                    with connection.begin() as transaction:
                        try:
                            connection.execute(statement)
                            transaction.commit()
                        except Exception as e:
                            current_app.logger.error(e)
                            transaction.rollback()

    @app.route('/')
    def api_home():
        # redirection de l'url principal vers la page d'accueil
        return redirect('/api/web')

    @app.route('/favicon.ico')
    def api_favicon():
        return redirect(url_for('static', filename='favicon.ico'))

    return app
