# models.py
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, TIMESTAMP, Text , UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(enum.Enum):
    admin = 'admin'
    member = 'member'

class ApprovalStatus(enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'

class VerificationStatus(enum.Enum):
    pending = 'pending'
    verified = 'verified'
    rejected = 'rejected'

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    city = Column(String(50))
    occupation = Column(String(50))
    role = Column(Enum(UserRole), nullable=False)
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.pending)
    is_active = Column(Boolean, default=True)
    
    social_links = relationship("UserSocialLink", back_populates="user")
    tweets = relationship("Tweet", back_populates="user")
    votes = relationship("Vote", back_populates="user")

class UserSocialLink(Base):
    __tablename__ = 'user_social_links'
    
    social_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    platform = Column(String(20), nullable=False)
    url = Column(String(200), nullable=False)
    
    user = relationship("User", back_populates="social_links")

class Tweet(Base):
    __tablename__ = 'tweets'
    
    tweet_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    tweet_text = Column(Text, nullable=False)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.pending)
    submit_date = Column(TIMESTAMP, server_default=func.now())
    
    user = relationship("User", back_populates="tweets")
    votes = relationship("Vote", back_populates="tweet")

class PlatformAccount(Base):
    __tablename__ = 'platform_accounts'
    
    account_id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    platform = Column(String(50), nullable=False)
    url = Column(String(200), nullable=False)
    admin_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

class Vote(Base):
    __tablename__ = 'votes'
    
    vote_id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey('tweets.tweet_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    vote = Column(Boolean, nullable=False)
    voted_at = Column(TIMESTAMP, server_default=func.now())
    
    
    
    # Prevents duplicate votes
    __table_args__ = (UniqueConstraint('tweet_id', 'user_id', name='_tweet_user_uc'),)
    
    user = relationship("User", back_populates="votes")
    tweet = relationship("Tweet", back_populates="votes")
    sources = relationship("VoteSource", back_populates="vote")

class VoteSource(Base):
    __tablename__ = 'vote_sources'
    
    source_id = Column(Integer, primary_key=True, index=True)
    vote_id = Column(Integer, ForeignKey('votes.vote_id', ondelete='CASCADE'), nullable=False)
    source_url = Column(String(200), nullable=False)
    
    vote = relationship("Vote", back_populates="sources")