from IAPT.gui.components import Label, CheckBox, ComboBox
from IAPT.core.data import get_classes


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
        for classname in get_classes():
            content.append(CheckBox(text=classname, layout=layout, default=classname in selected_classes))
            content[-1].stateChanged.connect(
                lambda checked, key="classname", value=classname: (
                    setMulti(state, key, value, bool(checked)),
                    on_change() if on_change else None,
                )
            )

    if "outstanding" in wanted or "non_outstanding" in wanted:
        content.append(Label(text="Outstanding", layout=layout, variant="subheading"))
        if "outstanding" in wanted:
            content.append(CheckBox(text="Outstanding", layout=layout, default=bool(state.get("outstanding", False))))
            content[-1].stateChanged.connect(
                lambda checked, key="outstanding": (setBool(state, key, checked), on_change() if on_change else None)
            )

        if "non_outstanding" in wanted:
            content.append(
                CheckBox(text="No Outstandings", layout=layout, default=bool(state.get("non_outstanding", False)))
            )
            content[-1].stateChanged.connect(
                lambda checked, key="non_outstanding": (
                    setBool(state, key, checked),
                    on_change() if on_change else None,
                )
            )

    if "late" in wanted or "non_late" in wanted:
        content.append(Label(text="Late", layout=layout, variant="subheading"))
        if "late" in wanted:
            content.append(CheckBox(text="Late", layout=layout, default=bool(state.get("late", False))))
            content[-1].stateChanged.connect(
                lambda checked, key="late": (setBool(state, key, checked), on_change() if on_change else None)
            )

        if "non_late" in wanted:
            content.append(CheckBox(text="No Lates", layout=layout, default=bool(state.get("non_late", False))))
            content[-1].stateChanged.connect(
                lambda checked, key="non_late": (setBool(state, key, checked), on_change() if on_change else None)
            )

    if "no_awards" in wanted or "bronze_awarded" in wanted or "silver_awarded" in wanted:
        content.append(Label(text="Awards", layout=layout, variant="subheading"))
        if "no_awards" in wanted:
            content.append(CheckBox(text="No Awards", layout=layout, default=bool(state.get("no_awards", False))))
            content[-1].stateChanged.connect(
                lambda checked, key="no_awards": (setBool(state, key, checked), on_change() if on_change else None)
            )

        if "bronze_awarded" in wanted:
            content.append(CheckBox(text="Bronze", layout=layout, default=bool(state.get("bronze_awarded", False))))
            content[-1].stateChanged.connect(
                lambda checked, key="bronze_awarded": (setBool(state, key, checked), on_change() if on_change else None)
            )

        if "silver_awarded" in wanted:
            content.append(CheckBox(text="Silver", layout=layout, default=bool(state.get("silver_awarded", False))))
            content[-1].stateChanged.connect(
                lambda checked, key="silver_awarded": (setBool(state, key, checked), on_change() if on_change else None)
            )

    if "no_account" in wanted:
        content.append(Label(text="Other", layout=layout, variant="subheading"))
        content.append(CheckBox(text="No Account", layout=layout, default=bool(state.get("no_account", False))))
        content[-1].stateChanged.connect(
            lambda checked, key="no_account": (setBool(state, key, checked), on_change() if on_change else None)
        )

    return content


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
        data.sort(key=lambda student: sortValue(student, primary))

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

    classes = state.get("classes", [])
    if classes:
        data = [o for o in data if o.classname in classes]

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

    if not filtered_lists:
        return data

    data = [o for o in data if any(o in l for l in filtered_lists)]

    return data
