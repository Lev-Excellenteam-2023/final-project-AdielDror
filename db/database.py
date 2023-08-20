from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.orm import Base


engine = create_engine('sqlite:///C:/Users/Adiel/Desktop/Excellent/final-project-AdielDror/db/database.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
