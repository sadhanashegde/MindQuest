from flask import Blueprint, render_template, request

journal_bp = Blueprint("journal", __name__)
journal_entries = []

@journal_bp.route("/journal", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        entry = request.form["entry"]
        journal_entries.append(entry)
    return render_template("journal.html", entries=journal_entries)
