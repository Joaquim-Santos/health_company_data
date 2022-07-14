import os

from health_company_data_api import application


if __name__ == "__main__":
    debug = application.config.get('DEBUG')
    host = os.getenv("HOST", 'localhost')
    port = os.getenv("PORT", 5000)

    application.run(host=host, port=port, debug=debug, use_reloader=False)
