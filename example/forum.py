"""Forum like example.

Code credits go to NewsMeme (https://github.com/danjac/newsmeme)
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Unicode,
    UnicodeText,
)
from sqlalchemy.orm import Relationship, declarative_base

Base = declarative_base()


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column(
        "post_id",
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    # user roles
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(60), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    karma = Column(Integer, default=0)
    date_joined = Column(DateTime, default=datetime.utcnow)
    activation_key = Column(String(80), unique=True)
    role = Column(Integer, default=MEMBER)
    receive_email = Column(Boolean, default=False)
    email_alerts = Column(Boolean, default=False)
    followers = Column(Text)
    following = Column(Text)

    _password = Column("password", String(80))
    _openid = Column("openid", String(80), unique=True)


class Post(Base):
    __tablename__ = "posts"

    PUBLIC = 100
    FRIENDS = 200
    PRIVATE = 300

    PER_PAGE = 40

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)

    title = Column(Unicode(200))
    description = Column(UnicodeText)
    link = Column(String(250))
    date_created = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer, default=1)
    num_comments = Column(Integer, default=0)
    votes = Column(Text)
    access = Column(Integer, default=PUBLIC)

    _tags = Column("tags", UnicodeText)

    author = Relationship(User, innerjoin=True, lazy="joined")


class Comment(Base):
    __tablename__ = "comments"

    PER_PAGE = 20

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)

    post_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"), nullable=False)

    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))

    comment = Column(UnicodeText)
    date_created = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer, default=1)
    votes = Column(Text)

    author = Relationship(User, innerjoin=True, lazy="joined")

    post = Relationship(Post, innerjoin=True, lazy="joined")

    parent = Relationship("Comment", remote_side=[id])


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    slug = Column(Unicode(80), unique=True)

    _name = Column("name", Unicode(80), unique=True)


if __name__ == "__main__":
    from eralchemy import render_er

    render_er(Base, "forum.svg")
    render_er(Base, "forum.er")
    render_er(Base, "forum.puml")
