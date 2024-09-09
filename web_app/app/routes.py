from flask import Blueprint, render_template, request, redirect, url_for, flash, g

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    project = g.get('project', None)
    if project is None:
        return render_template('index.html')
    return render_template('index.html', project=project)

@bp.route('/load_project', methods=['GET', 'POST'])
async def load_project():
    project = g.get('project', None)
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            # Run async function in event loop
            success = await project.load_project(filename)
            if success:
                print('Project loaded successfully!', 'success')
                return redirect(url_for('main.index'))
            else:
                print('Failed to load the project!', 'error')
        else:
            print('No project file selected!', 'error')
        return redirect(url_for('main.load_project'))
    project_files = await project.get_project_files()
    # List all project files
    return render_template('load_project.html', project_files=project_files)

@bp.route('/save_project', methods=['POST'])
async def save_project():
    return redirect(url_for('main.index'))

@bp.route('/create_project', methods=['GET', 'POST'])
async def create_project():
    project = g.get('project', None)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        build_version = request.form.get('build_version')
        mc_version = request.form.get('mc_version')
        mod_loader = request.form.get('mod_loader')
        client_side = request.form.get('client_side')
        server_side = request.form.get('server_side')

        if title and description:
            # Run async function in event loop if needed
            success = project.create_project(title=title, description=description,
                                             build_version=build_version, mc_version=mc_version,
                                             mod_loader=mod_loader, client_side=client_side, server_side=server_side)
            if success:
                flash('Modpack created successfully!', 'success')
                return redirect(url_for('main.index'))
            else:
                print('Failed to create the modpack!', 'error')
        else:
            print('All fields are required!', 'error')
        return redirect(url_for('main.create_project'))

    # Render the create project form
    return render_template('create_project.html')

@bp.route('/list_mods')
async def list_mods():
    project = g.project
    return render_template('list_mods.html', mods=project.mod_data)

@bp.route('/error')
def error_page():
    return render_template('error.html')
