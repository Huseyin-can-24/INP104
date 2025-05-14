from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Veritabanını başlat
    db.init_app(app)
    
    # Migrations
    migrate = Migrate(app, db)

    # Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Lütfen önce giriş yapın.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint'leri kaydet
    from routes.auth import auth_bp
    from routes.patient import patient_bp
    from routes.doctor import doctor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
            elif current_user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
        return render_template('index.html')

    return app

# Uygulama oluştur
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        
        try:
            # Admin kullanıcısı oluştur
            admin_username = "admin"
            admin = User.query.filter_by(username=admin_username).first()
            if not admin:
                admin = User(
                    username=admin_username,
                    first_name="Admin",
                    last_name="User",
                    role="admin"
                )
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("Admin kullanıcısı oluşturuldu!")
        except Exception as e:
            print(f"Admin oluşturulurken hata: {e}")
    
    app.run(debug=True)