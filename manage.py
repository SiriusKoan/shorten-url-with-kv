from os import getenv
import unittest
from flask_script import Manager
from app import create_app

app = create_app(getenv("ENV", "prod"))
manager = Manager(app)


@manager.shell
def shell():
    return globals()


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()