import json
import re
from pathlib import Path
from IAPT.core.config import PACKAGE_ROOT

TOKEN_PATTERN = re.compile(r"\[\[(colours|classes):([^\]]+)\]\]")
CONFIG_PATH = PACKAGE_ROOT / "gui" / "styles" / "stylesheet.json"


def load_style_config(config_path):
    with Path(config_path).open("r", encoding="utf-8") as file:
        return json.load(file)


STYLE_CONFIG = load_style_config(CONFIG_PATH)
COLOURS = STYLE_CONFIG["colours"]


def build_stylesheet(stylesheet, config):
    def replace_token(match):
        category, name = match.groups()
        try:
            return config[category][name]
        except KeyError as error:
            raise KeyError(f"Unknown stylesheet token: {category}:{name}") from error

    previous = None
    while stylesheet != previous:
        previous = stylesheet
        stylesheet = TOKEN_PATTERN.sub(replace_token, stylesheet)

    if TOKEN_PATTERN.search(stylesheet):
        raise ValueError("Unresolved stylesheet token")

    return stylesheet
