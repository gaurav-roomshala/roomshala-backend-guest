import sqlalchemy
from sqlalchemy import DateTime, Integer, Sequence, ARRAY, FLOAT

from src.constants.utilities import DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_URL, DB_USER
from src.utils.logger.logger import logger
import psycopg2


def creating_guest_table():
    logger.info("========= CREATING GUEST TABLE ==========")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('guest',))
        if bool(cur.rowcount):
            logger.info("====== TABLE ALREADY EXIST IN THE DATABASE PASSING IT ======")
            conn.close()
            return True
        else:
            logger.warning("======= ADMIN TABLE DOESN'T EXIST, CREATING IT ========")
            metadata = sqlalchemy.MetaData()
            guest = sqlalchemy.Table(
                "guest",
                metadata,
                sqlalchemy.Column("id", Integer, Sequence("guest_id_seq"), primary_key=True),
                sqlalchemy.Column("first_name", sqlalchemy.String()),
                sqlalchemy.Column("last_name", sqlalchemy.String()),
                sqlalchemy.Column("gender", sqlalchemy.String()),
                sqlalchemy.Column("email", sqlalchemy.String()),
                sqlalchemy.Column("password", sqlalchemy.String()),
                sqlalchemy.Column("phone_number", sqlalchemy.String()),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean()),
                sqlalchemy.Column("created_on", DateTime),
                sqlalchemy.Column("updated_on", DateTime)
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return guest
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING GUEST TABLE {} ########".format(e))
        raise Exception("SOMETHING WENT WRONG IN CREATING GUEST TABLE")


def creating_codes_table():
    try:
        logger.info(" ########## GOING FOR CODES TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('guest_code',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            logger.info("#### CODES TABLE DOESN'T EXIST #### ")
            metadata = sqlalchemy.MetaData()
            code = sqlalchemy.Table(
                "guest_code",
                metadata,
                sqlalchemy.Column("id", Integer, Sequence("guest_code_id_seq"), primary_key=True),
                sqlalchemy.Column("email", sqlalchemy.String(100)),
                sqlalchemy.Column("reset_code", sqlalchemy.String(60)),
                sqlalchemy.Column("expired_in", DateTime),
                sqlalchemy.Column("status", sqlalchemy.String(1))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return code
    except Exception as e:
        logger.error("{}".format(e))


def creating_blacklist_table():
    try:
        logger.info(" ########## GOING FOR BLACKLIST TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('guest_blacklists',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            blacklists = sqlalchemy.Table(
                "guest_blacklists", metadata,
                sqlalchemy.Column("token", sqlalchemy.String(700), unique=True),
                sqlalchemy.Column("email", sqlalchemy.String(100))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return blacklists
    except Exception as e:
        logger.error("{}".format(e))


def guest_fav_property():
    try:
        logger.info(" ########## GOING FOR GUEST FAVOURITE PROPERTY TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('guest_property_fav',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            guest_fav = sqlalchemy.Table(
                "guest_property_fav", metadata,
                sqlalchemy.Column("id", Integer, Sequence("guest_property_fav_id_seq"), primary_key=True),
                sqlalchemy.Column("property_id", sqlalchemy.Integer),
                sqlalchemy.Column("user_id", sqlalchemy.Integer),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean()),
                sqlalchemy.Column("created_on", DateTime),
                sqlalchemy.Column("updated_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return guest_fav
    except Exception as e:
        logger.error("{}".format(e))