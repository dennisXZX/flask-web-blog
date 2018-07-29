import datetime
import uuid

from src.common.database import Database
from src.models.post import Post


class Blog():
    @classmethod
    def from_mongo(cls, id):
        # find the blog with the specified id
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})

        # create a Blog object, cls() represents the current class
        # so later when we change the class name our code is still intact
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        # find all the blogs with the specified author id
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})

        # return a list of Blog objects
        return [cls(**blog) for blog in blogs]

    '''
    # Blog object methods
    '''
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    # create a new post
    def new_post(self, title, content, created_date=datetime.datetime.utcnow()):

        # create a post object
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=created_date)

        # save the post to database
        post.save_to_mongo()

    # update the post specified by an id
    def update_post(self, post_id, new_title, new_content):
        Database.update(
            collection='posts',
            query={
                '_id': post_id
            },
            data={
                '$set': {
                    'title': new_title,
                    'content': new_content
                }
            }
        )

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

