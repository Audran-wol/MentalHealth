from flask import Flask
import os
from ChatbotWebsite.config import Config
from ChatbotWebsite.extensions import db, bcrypt, mail, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_fallback_secret_key_here')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.static_folder = 'static'

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        try:
            from ChatbotWebsite.models import User, ChatMessage, Journal
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    from ChatbotWebsite.main.routes import main
    from ChatbotWebsite.chatbot.routes import chatbot
    from ChatbotWebsite.users.routes import users
    from ChatbotWebsite.errors.handlers import errors
    from ChatbotWebsite.journal.routes import journals

    app.register_blueprint(users)
    app.register_blueprint(chatbot)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(journals)

    return app