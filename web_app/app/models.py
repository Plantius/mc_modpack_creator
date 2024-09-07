from . import db

class Mod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    changelog = db.Column(db.Text, nullable=True)
    version_number = db.Column(db.String(20), nullable=False)
    dependencies = db.Column(db.JSON, nullable=True)
    mc_versions = db.Column(db.JSON, nullable=True)
    version_type = db.Column(db.String(20), nullable=True)
    mod_loaders = db.Column(db.JSON, nullable=True)
    mod_id = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.String(100), nullable=False)
    date_published = db.Column(db.String(50), nullable=True)
    files = db.Column(db.JSON, nullable=True)

    modpack_id = db.Column(db.Integer, db.ForeignKey('modpack.id'), nullable=False)
    modpack = db.relationship('Modpack', backref=db.backref('mods', lazy=True))

    def __repr__(self):
        return f'<Mod {self.title}>'

class Modpack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    build_date = db.Column(db.String(20), nullable=False)
    build_version = db.Column(db.String(20), nullable=False)
    mc_version = db.Column(db.String(10), nullable=False)
    mod_loader = db.Column(db.String(20), nullable=False)
    client_side = db.Column(db.String(20), nullable=False)
    server_side = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Modpack {self.title}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)