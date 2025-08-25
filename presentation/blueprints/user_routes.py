from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError

from infrastructure.db.session import get_session
from infrastructure.db.user_repository_impl import SqlAlchemyUserRepository
from infrastructure.auth.password_hasher_impl import BcryptPasswordHasher

from application.use_cases.register_user import RegisterUser
from application.use_cases.login_user import LoginUser
from core.exceptions import DomainValidationError

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.get('/register')
def register_form():
    return render_template("user/register_form.html")

@bp.post('/register')
def register_post():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not username or not email or not password:
        flash("Completa todos los campos", "error")
        return redirect(url_for("users.register_form"))

    with get_session() as s:
        repo = SqlAlchemyUserRepository(s)
        hasher = BcryptPasswordHasher()
        uc = RegisterUser(user_repo=repo, password_hasher=hasher.hash)
        try:
            user = uc.execute(username=username, email=email, raw_password=password)
            flash("Usuario creado con éxito", "success")
            # opcional: iniciar sesión automática
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("users.login_form"))
        except IntegrityError:
            s.rollback()
            flash("Usuario o email ya existen", "error")
            return redirect(url_for("users.register_form"))
        except DomainValidationError as de:
            flash(str(de), "error")
            return redirect(url_for("users.register_form"))
    

@bp.get("/login")
def login_form():
    return render_template("user/login_form.html")

@bp.post("/login")
def login_post():
    username_or_email = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username_or_email or not password:
        flash("Completa todos los campos", "error")
        return redirect(url_for("users.login_form"))

    with get_session() as s:
        repo = SqlAlchemyUserRepository(s)
        hasher = BcryptPasswordHasher()
        uc = LoginUser(user_repo=repo, password_checker=hasher.verify)
        try:
            user = uc.execute(username_or_email, password)
            # Sesión sencilla (si luego usas Flask-Login, reemplaza esto)
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Sesión iniciada", "success")
            return redirect(url_for("home.index"))  # o a tu dashboard
        except DomainValidationError as de:
            flash(str(de), "error")
            return redirect(url_for("users.login_form"))

@bp.post("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("users.login_form"))
