from multiple_inheritance.person import Person
from multiple_inheritance.logger_mixin import LoggerMixin
from multiple_inheritance.timestamp_mixin import TimestampMixin

class User (Person, LoggerMixin, TimestampMixin):
    def __init__(self,name,email):
        super().__init__(name,email)
        self.set_timestamp()
        self.log(f"User {self.name} created at {self.created_at}")