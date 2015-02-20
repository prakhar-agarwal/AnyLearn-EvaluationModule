from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func,Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import json
from pymongo import Connection 
import os
 
Base = declarative_base()

class Question(Base):
	__tablename__ = 'question'
	id=Column(Integer,primary_key=True)
	q_id=Column(String)
	storage_id=Column(String)

class UserDetails(Base):
	__tablename__='UserDetails'
	id=Column(Integer,primary_key=True)
	U_id=Column(String)
	js_storage_id=Column(String)
	ts=Column(DateTime,default=func.now())
	score=Column(Float)

fp = 'orm_in_detail.sqlite'
if os.path.exists(fp):
	os.remove(fp)

from sqlalchemy import create_engine
engine=create_engine('sqlite:///orm_in_detail.sqlite')
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)



connection=Connection('localhost',27017)
db=connection.test_database
collection=db.test_collection
post={    "gates": {        "1": "AND",        "2": "NOT"    },    "edges": [        {            "src":"1",            "dest": "2"        }    ],    "inputGate": {        "1" :["A","B"]    },    "outputGate": [        "2"    ],    "labels" : ["A", "B"]}
a= collection.insert(post)
a=str(a)
q=Question(q_id='DSFSFSFSF',storage_id=a)
s=session()
s.add(q)
s.commit()
str_id=s.query(Question).filter(Question.q_id='DSFSFSFSF').one().storage_id
print(str_id)
