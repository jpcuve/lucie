from flask import Blueprint, render_template, request, current_app

from lucie.calcul import multiplication
from lucie.database import read_test_values

bp = Blueprint('api_web', __name__, url_prefix='/api/web')


@bp.route('/')
@bp.route('/home')
def api_index():
    # on va lire quelques valeurs de la db, changer init.sql pour voir l'effet
    values = read_test_values()
    current_app.logger.debug(f"Values: {values}")
    return render_template(
        'index.html',
        message='Bonjour',
        values=values
    )


@bp.route('/submit-multiplicateur', methods=['POST'])
def api_submit_multiplicateur():
    multiplicateur = request.form.get('multiplicateur', default=1.0, type=float)
    current_app.logger.info(f"Multiplicateur: {multiplicateur}")
    produit = multiplication(current_app.config['A'], multiplicateur)  # le A dans config.py
    current_app.logger.info(f"Produit: {produit}")
    return render_template('resultat.html', produit=str(produit))
