from flask import Blueprint, render_template, request, redirect, url_for

journal_bp = Blueprint("journal_bp", __name__, url_prefix="/journaling")

# Temporary storage for journal entries
journal_entries = []

@journal_bp.route("/", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        entry = request.form.get("entry")  # Get the journal text
        if entry:
            journal_entries.append(entry)  # Store the entry
        return redirect(url_for("journal_bp.journal"))  # Reload page after saving

    return render_template("journal.html", entries=journal_entries)
