#!/usr/bin/env python3
"""Module for filtering and logging personal data."""

import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Obfuscates specified fields in a log message."""
    return re.sub(
            f'({"|".join(fields)})=[^{separator}]*',
            f'\\1={redaction}', message
            )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format log records, redacting PII fields."""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.getMessage(),
                self.SEPARATOR
                )
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Creates and configures a logger for user data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the MySQL database."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main():
    """Main function to retrieve and display filtered user data."""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
