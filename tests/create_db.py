"""
Script used to create an SQLite DB and test ERAlchemy in Homebrew.
"""
import argparse


def create_db(path):
    from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Department(Base):
        __tablename__ = 'department'
        id = Column(Integer, primary_key=True)
        name = Column(String)

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        # Use default=func.now() to set the default hiring time
        # of an Employee to be the current time when an
        # Employee record was created
        hired_on = Column(DateTime, default=func.now())
        department_id = Column(Integer, ForeignKey('department.id'))
        # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
        department = relationship(
            Department,
            backref=backref('employees',
                            uselist=True,
                            cascade='delete,all'))

    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///{}'.format(path))

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', nargs='?', help='Database URI to create.', default='orm_in_detail.sqlite')
    args = parser.parse_args()
    create_db(args.u)


if __name__ == '__main__':
    cli()
