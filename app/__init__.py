from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import blueprints from routes
    from .routes import kv_bp
    from .routes import read_bp
    #from .routes import use_kv_bp
    from .routes import get_token_bp
    # Register blueprints
    app.register_blueprint(kv_bp, url_prefix="/encryption")
    app.register_blueprint(read_bp, url_prefix="/decryption")
    #app.register_blueprint(use_kv_bp, url_prefix="/use")
    app.register_blueprint(get_token_bp, url_prefix="/dev")
    return app
   