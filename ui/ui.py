from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QPalette, QImage, QColor, QAction
from PyQt6.QtCore import (
    Qt, pyqtSlot, pyqtSignal, pyqtProperty,
    QSize, QRect, QPoint, QPropertyAnimation,
    QEasingCurve, 
)


class Py_Switcher(QCheckBox):
    ''' UI style switcher. '''
    def __init__(
        self,
        width = 60,
        bg_color = '#777',
        circle_color = '#DDD',
        circle_color_2 = '#5e5e5e',
        active_color = '#d1d1d1',
    ):
        QCheckBox.__init__(self)

        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Colors
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._circle_color_2 = circle_color_2
        self._active_color = active_color

        # Create Animation if needed
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b'circle_position', self)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.animation.setDuration(500)  # in miliseconds

        # self.stateChanged.connect(self.debug)
        self.stateChanged.connect(self.start_transition)

    # Create new set and get propety
    @pyqtProperty(float) # getter
    def circle_position(self):
        return self._circle_position

    @circle_position.setter  # setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    # def debug(self):
    #     ''' Debuging switcher widget.'''
    #     print(f'Status: {self.isChecked()}')

    def start_transition(self, value):
        ''' Debuging switcher widget.'''
        self.animation.stop() 
        if value:
            self.animation.setEndValue(self.width() - 26)  # if checked
        else:
            self.animation.setEndValue(3)  # def pos value if not checked

        self.animation.start()

    # Set new hitting area
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    # Drawing new items
    def paintEvent(self, e):
        # Set painter
        p = QStylePainter(self)
        p.setRenderHint(QStylePainter.RenderHint.Antialiasing)

        # Set no pen
        p.setPen(Qt.PenStyle.NoPen)

        # Draw rectangle
        rect = QRect(0, 0, self.width(), self.height())

        # Checking hits and drawing
        if not self.isChecked():
            # Draw bg
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(
                0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
            )

            # Draw circles
            p.setBrush(QColor(self._circle_color))
            # p.drawEllipse(3, 3, 22, 22) # without animation
            p.drawEllipse(self._circle_position, 3, 22, 22)
        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(
                0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
            )

            # Draw circles
            p.setBrush(QColor(self._circle_color_2))
            # p.drawEllipse(self.width() - 26, 3, 22, 22) # without animation
            p.drawEllipse(self._circle_position, 3, 22, 22)

        p.end()


class Settings_widget(QWidget):
    delete = pyqtSignal(int)
    text_emit = pyqtSignal(int, str)
    dir_emit = pyqtSignal(int, str)

    def __init__(self, id_widget: int, parent=None):
        super(Settings_widget, self).__init__(parent)
        self.id_widget = id_widget

        self.dynamic_widget_2 = QWidget(self)
        self.dynamic_widget_2.setLayout(QVBoxLayout())
        self.label_name = QLabel('Label name..')
        self.line_edit_label = QLineEdit()
        self.line_edit_label.setObjectName(str(id_widget))
        self.line_edit_label.textChanged[str].connect(self.on_text_change)
        self.line_edit_label.textChanged[str].connect(self.text_translator)
        self.dynamic_widget_2.layout().addWidget(self.label_name)
        self.dynamic_widget_2.layout().addWidget(self.line_edit_label)

        self.dynamic_widget = QWidget(self)
        self.dynamic_widget.setLayout(QHBoxLayout())
        self.line_edit_dir = QLineEdit()
        self.button_dir = QPushButton('Save to..', self)
        self.button_dir.setMinimumSize(QSize(75, 23))
        self.button_dir.clicked.connect(self.open_dir_1)
        self.button_delete = QPushButton('delete label', self)
        self.button_delete.clicked.connect(self.press_del)
        self.button_delete.setMinimumSize(QSize(75, 23))

        self.dynamic_widget.layout().addWidget(self.line_edit_dir)
        self.dynamic_widget.layout().addWidget(self.button_dir)
        self.dynamic_widget.layout().addWidget(self.button_delete)

        self.dynamic_widget_2.layout().addWidget(self.dynamic_widget)

        self.dynamic_widget_2.setWindowTitle(str(id_widget))

    @pyqtSlot()
    def press_del(self):
        self.delete.emit(self.id_widget)

    def open_dir_1(self):
        dir = QFileDialog.getExistingDirectory()
        self.line_edit_dir.setText(dir)
        self.dir_emit.emit(self.id_widget, dir)

    def on_text_change(self, text):
        self.label_name.setText(text)
        self.label_name.adjustSize()

    @pyqtSlot(str)
    def renaming_slot(self, text):
        child_line = self.dynamic_widget_2.findChild(QLineEdit, str(self.id_widget))
        child_line.setText(text)

    def text_translator(self, text):
        self.text_emit.emit(self.id_widget, text)


class Label_buttons(QWidget):
    delete_label = pyqtSignal(int)
    label_translate = pyqtSignal(int)

    def __init__(self, id_widget: int, parent=None):
        super(Label_buttons, self).__init__(parent)
        self.id_widget = id_widget

        predef_label = 'cat'
        self.dynamic_widget_labels = QWidget(self)
        self.dynamic_widget_labels.setLayout(QVBoxLayout())
        self.dynamic_widget_labels.setObjectName(str(id_widget))
        self.button_1 = QPushButton(predef_label, self)
        self.button_1.setObjectName(str(id_widget))
        self.button_1.clicked.connect(lambda: self.conn(self.id_widget))
        self.dynamic_widget_labels.layout().addWidget(self.button_1)

        self.dynamic_widget_labels.setWindowTitle(str(id_widget))

    @pyqtSlot(int)
    def conn(self, destination: int):
        self.label_translate.emit(destination)

    @pyqtSlot()
    def press_del_2(self):
        self.delete_label.emit(self.id_widget)

    @pyqtSlot(int, str)
    def renaming_slot_button(self, wid, text):
        child_button = self.dynamic_widget_labels.findChild(QPushButton, str(self.id_widget))
        child_button.setText(text)
        self.dynamic_widget_labels.adjustSize()


class Main_thread_ui(QWidget):
    def create_main_ui(self):
        self.widget_central = QWidget()
        self.widget_central.setLayout(QHBoxLayout())

        # Label for represent image
        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.ColorRole.Base)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
        )
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        # Label for representing right image
        # Maybe usefull for img preprocession
        self.image_label_r = QLabel()
        self.image_label_r.setBackgroundRole(QPalette.ColorRole.Base)
        self.image_label_r.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
        )
        self.image_label_r.setScaledContents(True)

        # Scroll area 1
        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setVisible(False)

        # Scroll area 2             For right preprocessed image
        self.scroll_area_2 = QScrollArea()
        self.scroll_area_2.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scroll_area_2.setWidget(self.image_label_r)
        self.scroll_area_2.setVisible(False)

        self.widget_central.layout().addWidget(self.scroll_area)
        self.widget_central.layout().addWidget(self.scroll_area_2)
        self.setCentralWidget(self.widget_central)


        # Toolbar
        self.toolbar = QToolBar('Toolbar')
        self.addToolBar(self.toolbar)
        # Black/White qss switcher
        self.toggle = Py_Switcher()
        self.toggle.toggled.connect(self.white_dark_clicked)
        self.toolbar.addWidget(self.toggle)

        # Dock widgets
        # Labels
        self.dock_widget_2 = QDockWidget('Labels', self)

        self.docked_widget_2 = QWidget(self)
        self.docked_widget_2.setLayout(QHBoxLayout())

        self.dock_widget_2.setWidget(self.docked_widget_2)
        self.dock_widget_2.setMinimumSize(QSize(120, 100))
        self.dock_widget_2.setFloating(False)
        self.dock_widget_2.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_widget_2)
        self.dock_widget_2.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)

        # Label settings
        self.dock_widget = QDockWidget('Label settings', self)

        self.docked_widget = QWidget(self)
        self.docked_widget.setLayout(QVBoxLayout())

        # Add button to dynamicly add widgets with settings
        self.button_widget_add = QPushButton('Add label', self)
        self.button_widget_add.clicked.connect(self.add_new_button)
        self.docked_widget.layout().addWidget(self.button_widget_add)

        self.dock_widget.setWidget(self.docked_widget)
        self.dock_widget.setMinimumSize(QSize(350, 492))
        self.dock_widget.setFloating(False)
        self.dock_widget.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures |
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable 
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_widget)
        self.dock_widget.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )

        self.setWindowTitle('Grimgset')
        self.resize(1280, 720)
