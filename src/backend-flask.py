from tinydb import TinyDB, Query
from flask import *
import re

db = TinyDB('CosmicaLinkDatabase')
User = Query()
app = Flask(__name__)

@app.route('/search/<path:subpath>', methods=['GET'])
def get(subpath):
    search = re.escape(subpath)
    results = db.search(User.link.matches(f'.*{search}.*', flags=re.IGNORECASE))
    return Response(str(results), status=200, mimetype="text/plain")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
