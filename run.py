import os

from app import create_app

# config_name = os.getenv('APP_SETTINGS')
config_name = "development"

app = create_app(config_name)


if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True, host='0.0.0.0', port='6001')