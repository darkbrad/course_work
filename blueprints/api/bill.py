from flask import Blueprint, jsonify, redirect, request, session
from flask_login import login_required

from blueprints import deps
from core.db import get_connection
from crud import bill_crud, user_crud

bill_blueprint = Blueprint('bill_blueprint', __name__, url_prefix="/bill")


@login_required
@bill_blueprint.route("/", methods=["POST"])
def create_bill():
    with get_connection() as conn:
        user = deps.get_user_by_id(session.get('_user_id'))
        bill_crud.create(conn, user[0])
        user_crud.new_bill(conn, user[1])
    return redirect("/success/")


@login_required
@bill_blueprint.route("/<string:bill_id>", methods=["DELETE"])
def unact(bill_id):
    with get_connection() as conn:
        bill_crud.get_unactive(conn, bill_id)
    return jsonify({"info": f"bill {bill_id} has become unactive"})


@login_required
@bill_blueprint.route("/add/<string:bill_id>/<int:money>")
def add(bill_id, money):
    with get_connection() as conn:
        user = bill_crud.get(conn, bill_id)
        login = user_crud.get_login_by_id(conn, user.owner)
        bill_crud.add_money(conn, money, user.balance, bill_id)

        print(user.owner, user.balance, login, " - added")
        return redirect("/success/")


@login_required
@bill_blueprint.route("/add", methods=["POST"])
def redir_add():
    sender_id = request.form.get("sender_bill_id")
    money = request.form.get("money")
    return redirect(f"/bill/add/{sender_id}/{int(money)}")


