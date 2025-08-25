from flask import Flask
from config import DevelopmentConfig
from presentation.blueprints.user_routes import bp as users_bp
from presentation.blueprints.note_routes import bp as notes_bp
from presentation.blueprints.group_routes import bp as groups_bp

def create_app(config_object=DevelopmentConfig):

    app = Flask(__name__, template_folder="presentation/templates",
        static_folder="presentation/static",   # 👈 importante
        static_url_path="/static" )
    app.config.from_object(config_object)
    
    @app.cli.command("init-db")
    def init_db():
        """Crea las tablas si no existen."""
        from infrastructure.db.session import _engine
        from infrastructure.db import models  # ⚠️ IMPORTA el módulo para registrar los modelos
        models.Base.metadata.create_all(bind=_engine)
        print("✅ Tablas creadas/actualizadas.")

    # Blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(groups_bp)

    # Seguridad básica
    app.secret_key = getattr(config_object, "SECRET_KEY", "dev-secret")
    return app

app = create_app()