from datetime import date
from PySide6.QtCore import QDate
from IAPT.gui.components import Label, CheckBox, ComboBox, NumberEdit, DateEdit
from IAPT.core.data import get_classnames, get_categories


def setBool(state, key, checked):
    state[key] = bool(checked)


def setMulti(state, key, value, checked):
    values = set(state.get(key, []))
    if checked:
        values.add(value)
    else:
        values.discard(value)
    state[key] = sorted(values)


def setCombo(state, key, value):
    state[key] = value


def drawFilters(columns, wanted, layout, state, on_change=None):
    content = []

    content.append(Label(text="Primary Sort", layout=layout, variant="subheading"))
    content.append(ComboBox(options=columns, layout=layout, default=state.get("primary_sort", None)))
    content[-1].currentIndexChanged.connect(
        lambda index, key="primary_sort", combo=content[-1]: (
            setCombo(state, key, combo.currentData()),
            on_change() if on_change else None,
        )
    )

    content.append(Label(text="Secondary Sort", layout=layout, variant="subheading"))
    content.append(ComboBox(options=columns, layout=layout, default=state.get("secondary_sort", None)))
    content[-1].currentIndexChanged.connect(
        lambda index, key="secondary_sort", combo=content[-1]: (
            setCombo(state, key, combo.currentData()),
            on_change() if on_change else None,
        )
    )

    if "classname" in wanted:
        content.append(Label(text="Class", layout=layout, variant="subheading"))
        selected_classes = set(state.get("classname", []))
        for classname in get_classnames():
            content.append(CheckBox(text=classname, layout=layout, default=classname in selected_classes))
            content[-1].stateChanged.connect(
                lambda checked, key="classname", value=classname: (
                    setMulti(state, key, value, bool(checked)),
                    on_change() if on_change else None,
                )
            )

    if "category" in wanted:
        content.append(Label(text="Category", layout=layout, variant="subheading"))
        selected_categories = set(state.get("category", []))
        for category in get_categories():
            content.append(CheckBox(text=category, layout=layout, default=category in selected_categories))
            content[-1].stateChanged.connect(
                lambda checked, key="category", value=category: (
                    setMulti(state, key, value, bool(checked)),
                    on_change() if on_change else None,
                )
            )

        content.append(CheckBox(text="No Category", layout=layout, default="" in selected_categories))
        content[-1].stateChanged.connect(
            lambda checked, key="category", value="": (
                setMulti(state, key, value, bool(checked)),
                on_change() if on_change else None,
            )
        )

    if "outstanding" in wanted:
        content.append(Label(text="Outstanding", layout=layout, variant="subheading"))
        content.append(CheckBox(text="Outstanding", layout=layout, default=bool(state.get("outstanding", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="outstanding": (setBool(state, key, checked), on_change() if on_change else None)
        )

        content.append(
            CheckBox(text="No Outstandings", layout=layout, default=bool(state.get("non_outstanding", False)))
        )
        content[-1].stateChanged.connect(
            lambda checked, key="non_outstanding": (setBool(state, key, checked), on_change() if on_change else None)
        )

    if "late" in wanted:
        content.append(Label(text="Late", layout=layout, variant="subheading"))
        content.append(CheckBox(text="Late", layout=layout, default=bool(state.get("late", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="late": (setBool(state, key, checked), on_change() if on_change else None)
        )

        content.append(CheckBox(text="No Lates", layout=layout, default=bool(state.get("non_late", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="non_late": (setBool(state, key, checked), on_change() if on_change else None)
        )

    if "awards" in wanted:
        content.append(Label(text="Awards", layout=layout, variant="subheading"))
        content.append(CheckBox(text="No Awards", layout=layout, default=bool(state.get("no_awards", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="no_awards": (setBool(state, key, checked), on_change() if on_change else None)
        )

        content.append(CheckBox(text="Bronze", layout=layout, default=bool(state.get("bronze_awarded", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="bronze_awarded": (setBool(state, key, checked), on_change() if on_change else None)
        )

        content.append(CheckBox(text="Silver", layout=layout, default=bool(state.get("silver_awarded", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="silver_awarded": (setBool(state, key, checked), on_change() if on_change else None)
        )

    if "on_roll" in wanted:
        content.append(Label(text="Active Students", layout=layout, variant="subheading"))
        content.append(CheckBox(text="On Roll", layout=layout, default=bool(state.get("on_roll", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="on_roll": (setBool(state, key, checked), on_change() if on_change else None)
        )

        content.append(CheckBox(text="Not On Roll", layout=layout, default=bool(state.get("not_on_roll", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="not_on_roll": (setBool(state, key, checked), on_change() if on_change else None)
        )

    if "disabled" in wanted:
        content.append(Label(text="Active Students", layout=layout, variant="subheading"))
        content.append(CheckBox(text="Disabled", layout=layout, default=bool(state.get("disabled", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="disabled": (setBool(state, key, checked), on_change() if on_change else None)
        )

        content.append(CheckBox(text="Not Disabled", layout=layout, default=bool(state.get("not_disabled", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="not_disabled": (setBool(state, key, checked), on_change() if on_change else None)
        )

    if "points" in wanted:
        content.append(Label(text="Points", layout=layout, variant="subheading"))
        for key, label in (("points_from", "From"), ("points_to", "To")):
            edit = NumberEdit(
                layout=layout,
                align="left",
                value=state.get(key),
                placeholder_text=f"{label} - Any",
            )
            content.append(edit)
            edit.textChanged.connect(lambda text, edit=edit, key=key: state.__setitem__(key, edit.value()))
            edit.valueCommitted.connect(lambda value: on_change() if on_change else None)

    if "due_date" in wanted:
        content.append(Label(text="Due Date", layout=layout, variant="subheading"))
        today = date.today()
        september = QDate(today.year if today.month >= 9 else today.year - 1, 9, 1)
        august = QDate(september.year() + 1, 8, 1)
        for key, label in (("due_date_from", "From"), ("due_date_to", "To")):
            default_date = september if key == "due_date_from" else august
            saved_date = state.get(key)
            if not saved_date:
                saved_date = default_date.toString("yyyy-MM-dd")
                state[key] = saved_date
            edit = DateEdit(minimum=september, value=QDate.fromString(saved_date, "yyyy-MM-dd"), layout=layout)
            content.append(edit)
            edit.dateChanged.connect(
                lambda value, key=key: (
                    state.__setitem__(key, value.toString("yyyy-MM-dd")),
                    on_change() if on_change else None,
                )
            )

    if "no_account" in wanted:
        content.append(Label(text="Other", layout=layout, variant="subheading"))
        content.append(CheckBox(text="No Account", layout=layout, default=bool(state.get("no_account", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="no_account": (setBool(state, key, checked), on_change() if on_change else None)
        )


def applySort(data, state):
    primary = state.get("primary_sort") or "id"
    secondary = state.get("secondary_sort") or None

    def sortValue(obj, field):
        value = getattr(obj, field, None)
        if isinstance(value, str):
            return value.lower()
        return value

    if secondary:
        data.sort(
            key=lambda obj: (
                sortValue(obj, primary),
                sortValue(obj, secondary),
            )
        )
    else:
        data.sort(key=lambda obj: sortValue(obj, primary))

    return data


def setDefaultSort(state, primary, secondary=None):
    if not state.get("primary_sort", None):
        state["primary_sort"] = primary[1]

    if secondary:
        if not state.get("secondary_sort", None):
            state["secondary_sort"] = secondary[1]

    return state


def applyFilters(data, state):
    filtered_lists = []

    classes = state.get("classname", [])
    if classes:
        data = [o for o in data if o.classname in classes]

    categories = state.get("category", [])
    if categories:
        data = [o for o in data if o.category in categories]

    points_from = state.get("points_from", None)
    points_to = state.get("points_to", None)
    if points_from:
        data = [o for o in data if o.points >= points_from]
    if points_to:
        data = [o for o in data if o.points <= points_to]

    due_date_from = state.get("due_date_from", None)
    due_date_to = state.get("due_date_to", None)
    if due_date_from:
        data = [o for o in data if o.due_date >= date.fromisoformat(due_date_from)]
    if due_date_to:
        data = [o for o in data if o.due_date <= date.fromisoformat(due_date_to)]

    if state.get("outstanding", False):
        filtered_lists.append([o for o in data if o.outstanding > 0])

    if state.get("non_outstanding", False):
        data = [o for o in data if o.outstanding == 0]

    if state.get("late", False):
        filtered_lists.append([o for o in data if o.late > 0])

    if state.get("non_late", False):
        data = [o for o in data if o.late == 0]

    if state.get("no_awards", False):
        data = [o for o in data if not o.bronze_awarded and not o.silver_awarded]

    if state.get("bronze_awarded", False):
        data = [o for o in data if o.bronze_awarded]

    if state.get("silver_awarded", False):
        data = [o for o in data if o.silver_awarded]

    if state.get("no_account", False):
        data = [o for o in data if not o.account_found]

    if state.get("not_on_roll", False):
        data = [o for o in data if not o.on_roll]

    if state.get("on_roll", False):
        data = [o for o in data if o.on_roll]

    if state.get("disabled", False):
        data = [o for o in data if o.disabled]

    if state.get("not_disabled", False):
        data = [o for o in data if not o.disabled]

    if not filtered_lists:
        return data

    data = [o for o in data if any(o in l for l in filtered_lists)]

    return data
