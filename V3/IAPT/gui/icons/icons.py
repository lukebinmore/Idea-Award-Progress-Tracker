from PySide6.QtGui import QIcon
from IAPT.core.config import PACKAGE_ROOT

back_icon = QIcon()
back_icon.addFile(str(PACKAGE_ROOT / "gui" / "icons" / "arrow_left.svg"), mode=QIcon.Normal)
back_icon.addFile(str(PACKAGE_ROOT / "gui" / "icons" / "arrow_left_disabled.svg"), mode=QIcon.Disabled)

forward_icon = QIcon()
forward_icon.addFile(str(PACKAGE_ROOT / "gui" / "icons" / "arrow_right.svg"), mode=QIcon.Normal)
forward_icon.addFile(str(PACKAGE_ROOT / "gui" / "icons" / "arrow_right_disabled.svg"), mode=QIcon.Disabled)
