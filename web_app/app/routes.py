from flask import Blueprint, render_template, request, redirect, url_for, flash, g
import mc_mp.standard as std

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
                flash('Project loaded successfully!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Failed to load the project!', 'error')
        else:
            flash('No project file selected!', 'error')
        return redirect(url_for('main.load_project'))

    # List all project files
    return render_template('load_project.html', project_files=std.get_project_files())

@bp.route('/save_project', methods=['POST'])
async def save_project():
    # title = request.form.get('title')
    # description = request.form.get('description')
    # build_date = request.form.get('build_date')
    # build_version = request.form.get('build_version')
    # mc_version = request.form.get('mc_version')
    # mod_loader = request.form.get('mod_loader')
    # client_side = request.form.get('client_side')
    # server_side = request.form.get('server_side')

    # # Run async functions if needed
    # loop = asyncio.get_event_loop()
    # modpack = Modpack(title=title, description=description, build_date=build_date,
    #                   build_version=build_version, mc_version=mc_version,
    #                   mod_loader=mod_loader, client_side=client_side, server_side=server_side)
    # db.session.add(modpack)
    # db.session.commit()
    # flash('Modpack saved successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/create_project', methods=['GET', 'POST'])
async def create_project():
    project = g.get('project', None)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        build_date = request.form.get('build_date')
        build_version = request.form.get('build_version')
        mc_version = request.form.get('mc_version')
        mod_loader = request.form.get('mod_loader')
        client_side = request.form.get('client_side')
        server_side = request.form.get('server_side')

        if title and description:
            # Run async function in event loop if needed
            success = await project.create_project(title=title, description=description, build_date=build_date,
                                                   build_version=build_version, mc_version=mc_version,
                                                   mod_loader=mod_loader, client_side=client_side, server_side=server_side)
            if success:
                flash('Modpack created successfully!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Failed to create the modpack!', 'error')
        else:
            flash('All fields are required!', 'error')
        return redirect(url_for('main.create_project'))

    # Render the create project form
    return render_template('create_project.html')

@bp.route('/list_mods')
async def list_mods():
    # Run async function if needed
    # loop = asyncio.get_event_loop()
    # mods = await loop.run_in_executor(None, lambda: Mod.query.all())
    return render_template('list_mods.html')

@bp.route('/error')
def error_page():
    return render_template('error.html')
