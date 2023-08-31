#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.expense import Expense
# from models.user import User

@app_views.route("/expenses", methods=["GET"],
                 strict_slashes=False)
def get_expenses():
    """
    retrieves all expenses objects
    :return: json of all states
    """
    expenses_list = []
    expense = storage.all("Expense")

    for obj in expense.values():
        expenses_list.append(obj.to_dict())

    # expenses = [expense.to_dict() for expense in user.expenses]

    return jsonify(expenses_list)

@app_views.route("/expenses/<expense_id>",  methods=["GET"],
                 strict_slashes=False)
def expense_by_id(expense_id):
    """
    gets a specific expense object by ID
    :param expense_id: expense object id
    :return: expense obj with the specified id or error
    """

    fetched_obj = storage.get("Expense", str(expense_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/expenses", methods=["POST"],
                 strict_slashes=False)
def expense_create():
    """
    create expense route
    :return: newly created expense obj
    """
    expense_json = request.get_json(silent=True)
    if expense_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", str(expense_json["user_id"])):
        abort(404)
    if "user_id" not in expense_json:
        abort(400, 'Missing user_id')
    if "amount" not in expense_json:
        abort(400, 'Missing amount')
    if "catagory" not in expense_json:
        abort(400, 'Missing catagory')
    if "location" not in expense_json:
        abort(400, 'Missing location')

    new_expense = Expense(**expense_json)
    new_expense.save()
    resp = jsonify(new_expense.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/expenses/<expense_id>",  methods=["PUT"],
                 strict_slashes=False)
def expense_put(expense_id):
    """
    updates specific Expense object by ID
    :param expense_id: expense object ID
    :return: expense object and 200 on success, or 400 or
    404 on failure
    """
    expense_json = request.get_json(silent=True)
    if expense_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Expense", str(expense_id))

    if fetched_obj is None:
        abort(404)

    for key, val in expense_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())


@app_views.route("/expenses/<expense_id>", methods=["DELETE"],
                 strict_slashes=False)
def expense_delete_by_id(expense_id):
    """
    deletes Expense by id
    :param expense_id: expense object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("Expense", str(expense_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
