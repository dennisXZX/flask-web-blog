import uuid

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User():
    @staticmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {'email': email})

        if data is not None:
            return cls(**data)

    @staticmethod
    def get_by_id(cls, id):
        data = Database.find_one('users', {'_id': id})

        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # check whether a user's email matches the password
        user = User.get_by_email(email)

        # if the email is a valid user account, check its password
        if user is not None:
            return user.password == password
        else:
            return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)

        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            # store the email address in session
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    '''
    # User object methods
    '''
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    # save the post to posts collection in MongoDB
    def save_to_mongo(self):
        Database.insert(collection='users',
                        data=self.json())

    # convert the Post object into a JSON
    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
