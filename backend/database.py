from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///./dev.db"), conect_args= {"check_same_thread":False}
SBlocal = sessionmaker(bind = engine, autoflush= False, autocommit = False)
base = declarative_base()
