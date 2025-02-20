import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QLayout
from PyQt6.QtGui import QPainter, QColor, QMouseEvent, QPolygonF, QPen, QPixmap
from PyQt6.QtCore import QPointF, Qt

class LevelEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level Editor")
        self.setGeometry(100, 100, 800, 700)

        # Define available materials with colors
        self.MATERIAL_COLORS = {
            "Wood": QColor(139, 69, 19),       # Brown color
            "Desert": QColor(237, 201, 175),   # Sand-ish color
            "OilRig": QColor(10, 10, 80),      # Dark blue color
            "Ice": QColor(173, 216, 230),      # Ice blue color
            "Stone": QColor(128, 128, 128)     # Gray color
        }

        self.TEXTURE_MAP = {
            "Wood": "level_graphics/level_assets_forest.swf",
            "Desert": "level_graphics/level_assets_desert.swf",
            "Ice": "level_graphics/level_assets_winter.swf",
            "Stone": "level_graphics/level_assets_mountain.swf",
            "OilRig": "level_graphics/level_assets_forest.swf"
        }

        self.selected_material = "Wood"  # Default material
        self.selected_texture = self.TEXTURE_MAP[self.selected_material]
        self.grass_theme = "[Material]"  # Default grass theme

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        control_layout = QVBoxLayout()
        control_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.label = QLabel("Right-click on the corners of the terrain element you want to place. Left-click to finish.\nTo select an element: left-click near the first-placed corner of that element.\n\nPlace the corners clockwise, else the top border will be at the bottom.")
        control_layout.addWidget(self.label)

        save_button = QPushButton("Save Level")
        save_button.clicked.connect(self.save_level)
        control_layout.addWidget(save_button)

        load_button = QPushButton("Load Level")
        control_layout.addWidget(load_button)
        load_button.clicked.connect(self.load_level)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected)
        control_layout.addWidget(delete_button)

        load_bg_button = QPushButton("Load Screenshot (760x668px)")
        load_bg_button.clicked.connect(self.load_background)
        control_layout.addWidget(load_bg_button)

        self.material_selector = QComboBox()
        self.material_selector.addItems(self.MATERIAL_COLORS.keys())
        self.material_selector.currentTextChanged.connect(self.set_material)
        control_layout.addWidget(self.material_selector)

        self.grass_theme_checkbox = QCheckBox("Add top border")
        self.grass_theme_checkbox.setChecked(True)
        self.grass_theme_checkbox.stateChanged.connect(self.toggle_grass_theme)
        control_layout.addWidget(self.grass_theme_checkbox)

        self.label1 = QLabel("")
        control_layout.addWidget(self.label1)

        control_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum))

        self.canvas = Canvas(self, self.MATERIAL_COLORS)
        self.canvas.setFixedSize(760, 668)
        self.canvas.setFrameStyle(QFrame.Shape.Box)
        main_layout.addWidget(self.canvas)

        main_layout.addLayout(control_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_material(self, material):
        """Set the currently selected material and update its texture."""
        self.selected_material = material
        self.selected_texture = self.TEXTURE_MAP[material]

    def toggle_grass_theme(self):
        """Toggle grass theme between [Material] and [None]."""
        self.grass_theme = "[Material]" if self.grass_theme_checkbox.isChecked() else "[None]"

    def load_background(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Background Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.canvas.set_background(file_name)

    def save_level(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Level", "", "JSON Files (*.lvl)")
        if file_name:
            data = {"elements": []}
            template = {
                "shade": 99,
                "id": "terrain_2",
                "element_type": "TerrainBlockEntity",
                "texture_export": "landmass_bg_tile.png",
                "blue": 7,
                "red": 16,
                "texture_rotation": 0,
                "no_fixtures": False,
                "green": 0,
                "outline": True,
                "unbreakable": False,
                "dynamic": False,
                "shape": "edgeShape",
                "tint": 0
            }

            for elem in self.canvas.elements:
                formatted_element = template.copy()
                formatted_element["points"] = [{"x": p[0], "y": p[1]} for p in elem["shape"]]
                formatted_element["theme"] = elem["theme"]
                formatted_element["texture_swf"] = elem["texture_swf"]
                formatted_element["grass_theme"] = elem["grass_theme"]
                data["elements"].append(formatted_element)

            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)

    def load_level(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Level", "", "JSON Files (*.lvl)")
        if file_name:
            with open(file_name, "r") as file:
                data = json.load(file)
                self.canvas.elements = []
                for elem in data.get("elements", []):
                    shape = [(p["x"], p["y"]) for p in elem["points"]]
                    theme = elem.get("theme", "Wood")
                    texture_swf = elem.get("texture_swf", self.TEXTURE_MAP.get(theme, "level_graphics/level_assets_forest.swf"))
                    self.canvas.elements.append({"shape": shape, "theme": theme, "texture_swf": texture_swf})
                self.canvas.update()

    def delete_selected(self):
        self.canvas.delete_selected()

class Canvas(QFrame):
    def __init__(self, editor, material_colors):
        super().__init__(editor)
        self.editor = editor
        self.material_colors = material_colors  # Store reference to colors
        self.elements = []
        self.selected_element = None
        self.current_shape = []
        self.background_image = None

    def set_background(self, file_path):
        self.background_image = QPixmap(file_path)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        x, y = event.position().x(), event.position().y()

        if event.button().name == "RightButton":
            # Add points to define a shape
            self.current_shape.append([x, y])
        else:
            for elem in self.elements:
                if any(int(p[0]) <= x <= int(p[0]) + 10 and int(p[1]) <= y <= int(p[1]) + 10 for p in elem['shape']):
                    self.selected_element = elem
                    return

            if not self.current_shape:
                return

            new_element = {
                "shape": self.current_shape,
                "theme": self.editor.selected_material,
                "texture_swf": self.editor.selected_texture,
                "grass_theme": self.editor.grass_theme
            }
            self.elements.append(new_element)
            self.selected_element = None
            self.current_shape = []

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.background_image:
            painter.drawPixmap(0, 0, self.width(), self.height(), self.background_image)

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        for elem in self.elements:
            theme = elem.get("theme", "Wood")  # Default to "Wood" if missing
            color = self.material_colors.get(theme, QColor(100, 200, 100))
            painter.setBrush(color)

            if len(elem["shape"]) > 1:
                polygon = QPolygonF([QPointF(p[0], p[1]) for p in elem["shape"]])
                painter.drawPolygon(polygon)
            else:
                painter.drawRect(int(elem['shape'][0][0]), int(elem['shape'][0][1]), 20, 20)

    def delete_selected(self):
        if self.selected_element in self.elements:
            self.elements.remove(self.selected_element)
            self.selected_element = None
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = LevelEditor()
    editor.show()
    sys.exit(app.exec())
