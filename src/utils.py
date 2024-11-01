from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# load the .env file variables
load_dotenv()


def db_connect():
    import os
    engine = create_engine(os.getenv('DATABASE_URL'))
    engine.connect()
    return engine

# This is a comment to test branching and merging from a codespace

# This is another test comment

# This is a comment to test the inverse: a student incorporating changes from main into their branch.
