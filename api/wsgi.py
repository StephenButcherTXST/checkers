from main import app as application

if __name__ == '__main__':
    app.run()
else:
    gunicorn_app = application
