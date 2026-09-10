class DatabaseError(Exception):
    """
    Database error for now is for
    psycopg.OperationalError and sqlite3.Error
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message
