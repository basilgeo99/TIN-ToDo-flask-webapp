from flask_script import Manager
from app import app,db

manager = Manager(app)


@manager.command
def checkScript():
    print ("The script runner is working")

@manager.command
def initializeDB():
    db.create_all()

if __name__ == "__main__":
    manager.run()