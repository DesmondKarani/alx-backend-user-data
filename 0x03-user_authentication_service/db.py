#!/usr/bin/env python3
"""DB module
This module provides a database interface for user management operations.
It defines a DB class that handles database connections and
user-related operations.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class for handling database operations.

    This class provides methods to interact with the database,
    including adding new users and managing database sessions.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.

        This method sets up the database engine, creates all necessary tables,
        and prepares the session maker.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.

        This property creates a database session if one doesn't exist,
        or returns the existing session.

        Returns:
            Session: The database session.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        This method creates a new user with the given email and hashed
        password,adds it to the database, and returns the new User object.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on input arguments.

        This method searches for a user in the database using the provided
        keyword arguments as filters. It returns the first matching user.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the search.

        Returns:
            User: The first user matching the search criteria.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
