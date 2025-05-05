# Import dependencies

# and subpackages
from api import app
from core import get_settings

# Exposing Flask App for Azure Deployment
app


if __name__ == '__main__':
    # Serve up flask API
    app.run(debug = False, use_reloader = False)

# EOF