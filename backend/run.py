from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

# for sqlite run these command on terminal
#
# python
# from flaskblog import db
# db.create_all()
# from flaskblog.models import Patient, order, shippingData, registrationData, marketing, jobs, teamUser
# User.query.all()
# region = Region(name='Over Yonder Thar')
# db.session.add(region)
# db.session.commit()