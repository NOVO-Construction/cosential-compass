import json
from flexmock import flexmock


def mocked_response(content=None, status_code=200, headers=None):
    if isinstance(content, dict):
        content = json.dumps(content)

    return flexmock(ok=status_code < 400, status_code=status_code, json=lambda: json.loads(content), raw=content, text=content, headers=headers)
