# store information on our apps settings in config.py
import os

DATABASE_URL = os.getenv('DATABASE_URL')

class Config:
  DEBUG = True
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_DATABASE_URI = DATABASE_URL
  SQLALCHEMY_TRACK_MODIFICATIONS = False