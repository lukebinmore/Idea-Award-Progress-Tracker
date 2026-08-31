COLOURS = {
    "background_primary": "#111111",
    "background_secondary": "#181818",
    "background_tertiary": "#202020",
    "accent": "#1F5F3F",
    "accent_highlight": "#2E8B57",
    "accent_pressed": "#16452E",
    "secondary": "#4B4A72",
    "secondary_highlight": "#65639A",
    "secondary_pressed": "#393852",
    "secondary_disabled": "#28283D",
    "text": "#F5F5F5",
    "text_disabled": "#777777",
    "border_primary": "#2A2A2A",
    "border_secondary": "#353535",
    "disabled": "#4A4A4A",
    "success": "#2E8B57",
    "success_highlight": "#3CB371",
    "success_pressed": "#246B45",
    "success_progress": "#66CDAA",
    "warning": "#B8860B",
    "warning_highlight": "#DAA520",
    "warning_pressed": "#966F09",
    "error": "#B22222",
    "error_highlight": "#DC3545",
    "error_pressed": "#8F1B18",
    "bronze": "#A8753A",
    "silver": "#8F9AA3",
    "outstanding": "#FF6B6B",
    "late": "#FFC857",
    "missing": "#9B59B6",
}

FONT_SIZES = {
    "standard": "13px",
    "table_header": "14px",
    "notification_label": "15px",
    "heading": "16px",
    "subheading": "15px",
    "program_title": "25px",
}

RADIUS = {
    "standard": "20px",
    "notification": "15px",
    "standard_lineedit": "12px",
}

BORDERS = {
    "standard": "2px solid",
}

GLOBAL = {
    "global": """
        font-family: "Comic Sans MS";
        font-size: 13px;
        color: #F5F5F5;
        background-color: transparent;
        gridline-color: transparent;
        border: 0;
    """,
}

CLASSES = {
    "heading": f"""
        font-size: {FONT_SIZES["heading"]};
        font-weight: bold;
        background-color: {COLOURS["accent"]};
        padding: 5px;
        border-bottom: {BORDERS["standard"]} {COLOURS["border_primary"]};
    """,
    "header_button": f"""
        border: {BORDERS["standard"]} {COLOURS["text"]};
        border-radius: 10px;
    """,
    "header_button_hover": f"""
        background-color: {COLOURS["accent_highlight"]};
    """,
    "header_button_pressed": f"""
        background-color: {COLOURS["accent_pressed"]};
    """,
    "header_button_disabled": f"""
        background-color: {COLOURS["accent_pressed"]};
        border-color: {COLOURS["text_disabled"]};
    """,
    "side_menu": f"""
        background-color: {COLOURS["background_secondary"]};
        margin: 10px 0;
        border: {BORDERS["standard"]} {COLOURS["border_primary"]};
    """,
    "nav_collapsed_btn": f"""
        background-color: {COLOURS["secondary"]};
        padding: 5px;
        margin: 10px 0;
    """,
    "nav_collapsed_btn_hover": f"""
        background-color: {COLOURS["secondary_highlight"]};
    """,
    "nav_collapsed_btn_pressed": f"""
        background-color: {COLOURS["secondary_pressed"]};
    """,
    "standard_btn": f"""
        background-color: {COLOURS["secondary"]};
        padding: 5px;
        color: {COLOURS["text"]};
    """,
    "standard_btn_hover": f"""
        background-color: {COLOURS["secondary_highlight"]};
    """,
    "standard_btn_pressed": f"""
        background-color: {COLOURS["secondary_pressed"]};
    """,
    "standard_btn_disabled": f"""
        background-color: {COLOURS["secondary_disabled"]};
        color: {COLOURS["text_disabled"]};
    """,
}


def build_stylesheet(stylesheet):
    tags = {
        "global": GLOBAL,
        "classes": CLASSES,
        "borders": BORDERS,
        "radius": RADIUS,
        "font_sizes": FONT_SIZES,
        "colours": COLOURS,
    }

    while "[[" in stylesheet:
        start = stylesheet.index("[[")
        end = stylesheet.index("]]", start)

        tag, name = stylesheet[start + 2 : end].split(":")

        stylesheet = stylesheet.replace(stylesheet[start : end + 2], tags[tag][name], 1)

    return stylesheet
