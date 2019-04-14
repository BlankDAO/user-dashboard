import server


def register_blueprints(app):
    app.register_blueprint(server.bp, url_prefix='')
