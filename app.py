from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agidb.db'

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Product = Base.classes.product
Customer = Base.classes.city


@app.route('/')
def index():
    # new_product = Product(name='Fire Stone', price=20)
    # db.session.add(new_product)
    # db.session.commit()

    # results = db.session.query(Product).all()
    # for r in results:
    #     print(r.name)

    city_count = db.session.query(Customer).filter(Product.id == 2).count()
    print(city_count)

    return ''