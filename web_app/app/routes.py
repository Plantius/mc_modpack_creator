from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from .models import Mod, Modpack, db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    project = g.get('project', None)
    if project is None:
        return render_template('index.html')
    return render_template('index.html', project=project)

@bp.route('/load_project', methods=['POST'])
def load_project():
    title = request.form.get('title')
    modpack = Modpack.query.filter_by(title=title).first()
    if not modpack:
        flash('Modpack not found!', 'error')
        return redirect(url_for('main.home'))
    mods = Mod.query.filter_by(modpack_id=modpack.id).all()
    return render_template('project.html', modpack=modpack, mods=mods)

@bp.route('/save_project', methods=['POST'])
def save_project():
    title = request.form.get('title')
    description = request.form.get('description')
    build_date = request.form.get('build_date')
    build_version = request.form.get('build_version')
    mc_version = request.form.get('mc_version')
    mod_loader = request.form.get('mod_loader')
    client_side = request.form.get('client_side')
    server_side = request.form.get('server_side')

    modpack = Modpack(title=title, description=description, build_date=build_date,
                      build_version=build_version, mc_version=mc_version,
                      mod_loader=mod_loader, client_side=client_side, server_side=server_side)
    db.session.add(modpack)
    db.session.commit()
    flash('Modpack saved successfully!', 'success')
    return redirect(url_for('main.home'))

@bp.route('/create_project', methods=['POST'])
def create_project():
    title = request.form.get('title')
    description = request.form.get('description')
    build_date = request.form.get('build_date')
    build_version = request.form.get('build_version')
    mc_version = request.form.get('mc_version')
    mod_loader = request.form.get('mod_loader')
    client_side = request.form.get('client_side')
    server_side = request.form.get('server_side')

    modpack = Modpack(title=title, description=description, build_date=build_date,
                      build_version=build_version, mc_version=mc_version,
                      mod_loader=mod_loader, client_side=client_side, server_side=server_side)
    db.session.add(modpack)
    db.session.commit()
    flash('Modpack created successfully!', 'success')
    return redirect(url_for('main.home'))

@bp.route('/list_mods')
def list_mods():
    mods = Mod.query.all()
    return render_template('list_mods.html', mods=mods)

@bp.route('/error')
def error_page():
    return render_template('error.html')
