import datetime
import uuid

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User():
    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {"email": email})

        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, id):
        data = Database.find_one('users', {"_id": id})

        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            # store the email address in session
            session['email'] = email
            return True
        else:
            # User exists :(
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    # create a new post
    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        # find the blog associated with the id
        blog = Blog.from_mongo(blog_id)

        blog.new_post(title=title,
                      content=content,
                      date=date)

    '''
    # User object methods
    '''
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    # return all the blogs associated with the user
    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    # create a new blog
    # TODO - add verification and sanitise the inputs
    def new_blog(self, title, description):
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()

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
