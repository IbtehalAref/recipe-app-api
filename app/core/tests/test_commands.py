"""
Test Custom Django management commands
"""


from unittest.mock import patch
from psycopg2 import OperationalError as psycopg2Error
