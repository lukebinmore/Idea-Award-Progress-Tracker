from PySide6.QtGui import QIcon
from IAPT.core.config import PACKAGE_ROOT

ICON_ROOT = PACKAGE_ROOT / "gui" / "icons" / ""

back_icon = QIcon()
back_icon.addFile(str(ICON_ROOT / "arrow_left.svg"), mode=QIcon.Normal)
back_icon.addFile(str(ICON_ROOT / "arrow_left_disabled.svg"), mode=QIcon.Disabled)

forward_icon = QIcon()
forward_icon.addFile(str(ICON_ROOT / "arrow_right.svg"), mode=QIcon.Normal)
forward_icon.addFile(str(ICON_ROOT / "arrow_right_disabled.svg"), mode=QIcon.Disabled)

navigation_icon = QIcon()
navigation_icon.addFile(str(ICON_ROOT / "navigation.svg"), mode=QIcon.Normal)

filters_icon = QIcon()
filters_icon.addFile(str(ICON_ROOT / "filters.svg"), mode=QIcon.Normal)

close_icon = QIcon()
close_icon.addFile(str(ICON_ROOT / "close.svg"), mode=QIcon.Normal)
