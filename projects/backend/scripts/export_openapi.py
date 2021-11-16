from io import StringIO
from typing import Any, Dict

import yaml
from app.main import app
from fastapi.openapi.utils import get_openapi


def get_open_api_json() -> Dict[str, Any]:
    return get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )


def get_open_api_yaml() -> yaml:
    openapi_json = get_open_api_json()
    yaml_s = StringIO()
    yaml.dump(openapi_json, yaml_s)
    return yaml_s


if __name__ == "__main__":
    openapi_yaml = get_open_api_json()
    with open("openapi.yaml", "w") as outfile:
        yaml.dump(openapi_yaml, outfile, default_flow_style=False, allow_unicode=True)
