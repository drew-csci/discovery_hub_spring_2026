import os
from flask import Flask, render_template
from config import config
from extensions import db, migrate, login_manager


def create_app(config_name=None):
    """Application factory function"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from accounts import accounts_bp
    from pages import pages_bp
    
    app.register_blueprint(accounts_bp)
    app.register_blueprint(pages_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from accounts.models import User
        return User.query.get(int(user_id))
    
    # Create tables and context
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
