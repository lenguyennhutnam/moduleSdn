from flask import Flask, redirect, render_template, request, send_file, url_for
from . import export
import os

app = Flask(__name__)

app.add_url_rule('/', endpoint='export_script')


@app.route('/', methods=['GET', 'POST'])
def export_script():
    if request.method == 'POST':
        export.exportTopo(dir=__file__)
        # if download is False, script will just showing in the browser
        download = True
        return send_file("topo.py", as_attachment=download)

    return render_template("export_script.html")


if __name__ == '__main__':
    # at moduleSdn folder run this command to test
    # flask --app ModuleExport run --debug 
    app.run(debug=True)
