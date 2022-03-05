import sqlite3 as sql
import datetime
import os


def connect_db():
    db = sql.connect('intensive_schedule.db')

