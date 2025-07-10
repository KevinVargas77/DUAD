from multiple_inheritance.person import Person
from multiple_inheritance.logger_mixin import LoggerMixin
from multiple_inheritance.timestamp_mixin import TimestampMixin
from datetime import datetime

class User(Person, LoggerMixin, TimestampMixin):
    def __init__(self, name, email,date_of_birth):
        super().__init__(name, email)
        self.set_timestamp()
        self.date_of_birth = date_of_birth


    @property
    def info(self):
        return f"{self.name} | {self.email} | {self.age} years old"


    @property
    def created_at_datetime(self):
        return datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S")


    @property
    def days_active(self):
        now = datetime.now()
        return (now - self.created_at_datetime).days


    @property  #exercise 3
    def age(self):
        today = datetime.today().date()
        dob = self.date_of_birth 
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))