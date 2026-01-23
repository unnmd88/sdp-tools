import json

from pythonjsonlogger.json import JsonFormatter


class EnsureAsciiJsonFormatter(JsonFormatter):
    def __init__(self, *args, **kwargs):
        self.ensure_ascii = kwargs.pop('ensure_ascii', False)
        super().__init__(*args, **kwargs)

    def jsonify_log_record(self, log_record):
        return json.dumps(log_record, ensure_ascii=self.ensure_ascii)


formatter_class = f'{__name__}.EnsureAsciiJsonFormatter'