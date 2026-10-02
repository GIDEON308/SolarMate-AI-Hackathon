from flask import Flask, render_template, request

from solarmate.analysis import FORM_FIELDS, analyze_case
from solarmate.analysis import SUPPORTED_SYMPTOMS
from solarmate.guidance import guidance_for_case


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    values = {field: "" for field in FORM_FIELDS}
    errors = {}
    result = None

    if request.method == "POST":
        values.update(request.form.to_dict())
        errors, result = analyze_case(values)
        if result:
            result.update(guidance_for_case(result))

    return render_template(
        "index.html",
        values=values,
        errors=errors,
        result=result,
        symptoms=SUPPORTED_SYMPTOMS,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
