"""

"""

from backend.app import db, create_app
from backend.app.models.user  import User
from backend.app.models.app  import BibboxApp

from backend.app.bibbox.instance_controler import InstanceControler

if __name__ == '__main__':

    ic = InstanceControler()

    app = create_app ('developmentlocal')    
    print ("Now in main",  app.config['SQLALCHEMY_DATABASE_URI'] )

    iIds = ic.getInstanceIds ()
    print (iIds)

    print (dir(InstanceControler))

    for id in iIds:
        iDescr = ic.getInstanceDescription (id)
        print (iDescr)

