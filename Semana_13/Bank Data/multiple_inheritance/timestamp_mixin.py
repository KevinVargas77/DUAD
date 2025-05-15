import datetime

class TimestampMixin:
    def set_timestamp(self):
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")