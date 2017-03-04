"""" config module for sql """
import os

rds_host = os.environ.get('RDS_HOST', '')
db_name = os.environ.get('RDS_DB', '')
db_username = os.environ.get('RDS_USER', '')
db_password = os.environ.get('RDS_PASS', '')
