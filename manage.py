from os import getenv
import unittest
from flask_migrate import Migrate
from app import create_app, db

app = create_app(getenv("FLASK_ENV"))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return globals()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
