from flask import Blueprint, render_template, jsonify
from flask_login import LoginManager, login_required

pages_blueprint = Blueprint("pages_blueprint", __name__, url_prefix="/pages")


@pages_blueprint.route("/profile/<string:login>", methods=["GET"])
@login_required
def cabinet(login):
    return render_template("personal-cabinet.html", name=login)
