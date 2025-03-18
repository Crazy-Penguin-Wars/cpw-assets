import sys
import json
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QLayout, QLineEdit, QDialog, QListWidget
from PyQt6.QtGui import QPainter, QColor, QMouseEvent, QPolygonF, QPen, QPixmap, QCursor
from PyQt6.QtCore import QPointF, Qt, QEvent

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

        self.fixtures = {
            "BallSmallIce": "ball_small",
            "BallMediumIce": "ball_medium",
            "CubeSmallIce": "cube_small",
            "CubeMediumIce": "cube_medium",
            "CubeLargeIce": "cube_big",
            "TriangleSmallIce": "triangle_small",
            "TriangleMediumIce": "triangle_medium",
            "RectangleLargeIce": "rectangle_large",
            "RectangleMediumIce": "rectangle_medium",
            "PlankLargeIce": "plank_large",
            "PlankMediumIce": "plank_medium",
            "PlankSmallIce": "plank_small",
            "BallSmallMetal": "ball_small",
            "BallMediumMetal": "ball_medium",
            "CubeSmallMetal": "cube_small",
            "CubeMediumMetal": "cube_medium",
            "CubeLargeMetal": "cube_big",
            "TriangleSmallMetal": "triangle_small",
            "TriangleMediumMetal": "triangle_medium",
            "RectangleLargeMetal": "rectangle_large",
            "RectangleMediumMetal": "rectangle_medium",
            "PlankLargeMetal": "plank_large",
            "PlankMediumMetal": "plank_medium",
            "PlankSmallMetal": "plank_small",
            "BallSmallStone": "ball_small",
            "BallMediumStone": "ball_medium",
            "CubeSmallStone": "cube_small",
            "CubeMediumStone": "cube_medium",
            "CubeLargeStone": "cube_big",
            "TriangleSmallStone": "triangle_small",
            "TriangleMediumStone": "triangle_medium",
            "RectangleLargeStone": "rectangle_large",
            "RectangleMediumStone": "rectangle_medium",
            "PlankLargeStone": "plank_large",
            "PlankMediumStone": "plank_medium",
            "PlankSmallStone": "plank_small",
            "BallSmallWood": "ball_small",
            "BallMediumWood": "ball_medium",
            "CubeSmallWood": "cube_small",
            "CubeMediumWood": "cube_medium",
            "CubeLargeWood": "cube_big",
            "TriangleSmallWood": "triangle_small",
            "TriangleMediumWood": "triangle_medium",
            "RectangleLargeWood": "rectangle_large",
            "RectangleMediumWood": "rectangle_medium",
            "PlankLargeWood": "plank_large",
            "PlankMediumWood": "plank_medium",
            "PlankSmallWood": "plank_small"
        }

        self.names = {
            "BallSmallIce": "BallSmall",
            "BallMediumIce": "BallMedium",
            "CubeSmallIce": "CubeSmall",
            "CubeMediumIce": "CubeMedium",
            "CubeLargeIce": "CubeLarge",
            "TriangleSmallIce": "TriangleSmall",
            "TriangleMediumIce": "TriangleMedium",
            "RectangleLargeIce": "RectangleLarge",
            "RectangleMediumIce": "RectangleMedium",
            "PlankLargeIce": "PlankLarge",
            "PlankMediumIce": "PlankMedium",
            "PlankSmallIce": "PlankSmall",
            "BallSmallMetal": "BallSmall",
            "BallMediumMetal": "BallMedium",
            "CubeSmallMetal": "CubeSmall",
            "CubeMediumMetal": "CubeMedium",
            "CubeLargeMetal": "CubeLarge",
            "TriangleSmallMetal": "TriangleSmall",
            "TriangleMediumMetal": "TriangleMedium",
            "RectangleLargeMetal": "RectangleLarge",
            "RectangleMediumMetal": "RectangleMedium",
            "PlankLargeMetal": "PlankLarge",
            "PlankMediumMetal": "PlankMedium",
            "PlankSmallMetal": "PlankSmall",
            "BallSmallStone": "BallSmall",
            "BallMediumStone": "BallMedium",
            "CubeSmallStone": "CubeSmall",
            "CubeMediumStone": "CubeMedium",
            "CubeLargeStone": "CubeLarge",
            "TriangleSmallStone": "TriangleSmall",
            "TriangleMediumStone": "TriangleMedium",
            "RectangleLargeStone": "RectangleLarge",
            "RectangleMediumStone": "RectangleMedium",
            "PlankLargeStone": "PlankLarge",
            "PlankMediumStone": "PlankMedium",
            "PlankSmallStone": "PlankSmall",
            "BallSmallWood": "BallSmall",
            "BallMediumWood": "BallMedium",
            "CubeSmallWood": "CubeSmall",
            "CubeMediumWood": "CubeMedium",
            "CubeLargeWood": "CubeLarge",
            "TriangleSmallWood": "TriangleSmall",
            "TriangleMediumWood": "TriangleMedium",
            "RectangleLargeWood": "RectangleLarge",
            "RectangleMediumWood": "RectangleMedium",
            "PlankLargeWood": "PlankLarge",
            "PlankMediumWood": "PlankMedium",
            "PlankSmallWood": "PlankSmall"
        }

        self.materials = {
            "BallSmallIce": "Ice",
            "BallMediumIce": "Ice",
            "CubeSmallIce": "Ice",
            "CubeMediumIce": "Ice",
            "CubeLargeIce": "Ice",
            "TriangleSmallIce": "Ice",
            "TriangleMediumIce": "Ice",
            "RectangleLargeIce": "Ice",
            "RectangleMediumIce": "Ice",
            "PlankLargeIce": "Ice",
            "PlankMediumIce": "Ice",
            "PlankSmallIce": "Ice",
            "BallSmallMetal": "Metal",
            "BallMediumMetal": "Metal",
            "CubeSmallMetal": "Metal",
            "CubeMediumMetal": "Metal",
            "CubeLargeMetal": "Metal",
            "TriangleSmallMetal": "Metal",
            "TriangleMediumMetal": "Metal",
            "RectangleLargeMetal": "Metal",
            "RectangleMediumMetal": "Metal",
            "PlankLargeMetal": "Metal",
            "PlankMediumMetal": "Metal",
            "PlankSmallMetal": "Metal",
            "BallSmallStone": "Stone",
            "BallMediumStone": "Stone",
            "CubeSmallStone": "Stone",
            "CubeMediumStone": "Stone",
            "CubeLargeStone": "Stone",
            "TriangleSmallStone": "Stone",
            "TriangleMediumStone": "Stone",
            "RectangleLargeStone": "Stone",
            "RectangleMediumStone": "Stone",
            "PlankLargeStone": "Stone",
            "PlankMediumStone": "Stone",
            "PlankSmallStone": "Stone",
            "BallSmallWood": "Wood",
            "BallMediumWood": "Wood",
            "CubeSmallWood": "Wood",
            "CubeMediumWood": "Wood",
            "CubeLargeWood": "Wood",
            "TriangleSmallWood": "Wood",
            "TriangleMediumWood": "Wood",
            "RectangleLargeWood": "Wood",
            "RectangleMediumWood": "Wood",
            "PlankLargeWood": "Wood",
            "PlankMediumWood": "Wood",
            "PlankSmallWood": "Wood"
        }

        self.selected_material = "Wood"  # Default material
        self.selected_texture = self.TEXTURE_MAP[self.selected_material]
        self.grass_theme = "[Material]"  # Default grass theme
        self.pending_object = "no"
        self.timeSinceKeyPress = False
        self.level_settings = {"level_name": "", "theme": "Forest", "zoom_side": "width", "width": 760, "height": 668, "camera_bounds_width": 100, "camera_bounds_height": 100, "water_velocity_x": 0, "water_velocity_y": 0, "water_line": 477, "water_density": 32, "water_lineardrag": 15, "water_angulardrag": 15}  # Store level settings

        self.initUI()
        self.installEventFilter(self)

    def initUI(self):
        main_layout = QHBoxLayout()
        control_layout = QVBoxLayout()
        control_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.label = QLabel("Right-click on the corners of the terrain element you want to place. Left-click to finish.\nTo select an element: left-click near the first-placed corner of that element.\n\nPlace the corners clockwise, else the top border will be at the bottom.\n\nThe map scale factor is useful if the map is too 'zoomed in' (penguins/map textures too big).\nIt stretches all of the coördinates by the given factor (which means higher = smaller map textures).\n\nPress S to set a spawnpoint at your mouse location. There should be exactly 4 spawnpoints.\n\nPress M to edit level settings.")
        control_layout.addWidget(self.label)

        self.textbox_scale = QLineEdit()
        self.textbox_scale.setText("1.000")
        self.textbox_scale.setPlaceholderText("Map scale factor")
        self.textbox_scale.setFocus()
        control_layout.addWidget(self.textbox_scale)

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

        self.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_E:
            self.show_object_selection()
            return True
        elif event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_M:
            self.open_level_settings()
            return True
        elif event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_S and float(time.time()) - self.timeSinceKeyPress > 0.5:
            cursor_pos = self.canvas.mapFromGlobal(QCursor.pos())
            self.canvas.spawnpoints.append((cursor_pos.x(), cursor_pos.y()))
            self.canvas.update()
            self.timeSinceKeyPress = float(time.time())
            return True
        return super().eventFilter(obj, event)
    
    def open_level_settings(self):
        dialog = LevelSettingsDialog(self)
        if dialog.exec():
            self.level_settings = dialog.get_settings()
            print("Updated Level Settings:", self.level_settings)
    
    def show_object_selection(self):
        dialog = ObjectSelectionDialog(self)
        if dialog.exec():
            self.pending_object = dialog.selected_object

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
                "blue": 0,
                "red": 0,
                "texture_rotation": 0,
                "no_fixtures": False,
                "green": 0,
                "outline": True,
                "unbreakable": False,
                "dynamic": False,
                "shape": "edgeShape",
                "tint": 0
            }

            template_dynamic = {
                "id": "dynamic_1",
                "element_type": "DynamicObject",
                "unbreakable": False,
                "sleep": False,
                "angle": 0
            }

            scale = float(self.textbox_scale.text())
            bias_width = (3000 - self.level_settings["width"] * scale) / 2 # 3000 = width we want, 760*scale = actual width

            # ELEMENTS
            for elem in self.canvas.elements:
                if elem["element_type"] == "TerrainBlockEntity":
                    formatted_element = template.copy()
                    formatted_element["points"] = [{"x": p[0] * scale + bias_width, "y": p[1] * scale} for p in elem["shape"]]
                    formatted_element["theme"] = elem["theme"]
                    formatted_element["texture_swf"] = elem["texture_swf"]
                    formatted_element["grass_theme"] = elem["grass_theme"]
                    data["elements"].append(formatted_element)
                elif elem["element_type"] == "DynamicObject":
                    formatted_element = template_dynamic.copy()
                    formatted_element["x"] = elem["x"] * scale + bias_width
                    formatted_element["y"] = elem["y"] * scale
                    formatted_element["theme"] = self.materials[elem["name"]]
                    formatted_element["fixture"] = self.fixtures[elem["name"]]
                    formatted_element["name"] = self.names[elem["name"]]
                    data["elements"].append(formatted_element)

            # SPAWN POINTS
            data["spawn_points"] = []
            for i in range(len(self.canvas.spawnpoints)):
                data["spawn_points"].append({"name": "SpawnPoint" + str(i), "x": self.canvas.spawnpoints[i][0] * scale + bias_width, "y": self.canvas.spawnpoints[i][1] * scale})

            # SETTINGS
            for i in self.level_settings.keys():
                data[i] = self.level_settings[i]

            data["width"] = 3000
            data["height"] = self.level_settings["height"] * scale
            data["water_line"] = self.level_settings["water_line"] * scale

            # PARALLAX LAYERS
            data["parallax_layers"] = [{"element_type":"ParallaxLayer","camera_y_pan":0,"graphics_export":["parallax_1_1","parallax_1_2"],"graphics_swf":"level_graphics/level_bg_forest.swf","camera_z":0,"id":"parallax_4","gap":500,"y":550,"camera_x_pan":0,"tile_horizontally":True,"x":100},{"element_type":"ParallaxLayer","camera_y_pan":0,"graphics_export":["parallax_2_2","parallax_2_1"],"graphics_swf":"level_graphics/level_bg_forest.swf","camera_z":0,"id":"parallax_1","gap":800,"y":580,"camera_x_pan":0,"tile_horizontally":False,"x":200},{"element_type":"ParallaxLayer","camera_y_pan":0,"graphics_export":["parallax_3_1"],"graphics_swf":"level_graphics/level_bg_forest.swf","camera_z":0,"id":"parallax_2","gap":700,"y":380,"camera_x_pan":0,"tile_horizontally":True,"x":250},{"element_type":"ParallaxLayer","camera_y_pan":0,"graphics_export":["parallax_4_1"],"graphics_swf":"level_graphics/level_bg_forest.swf","camera_z":0,"id":"parallax_3","gap":1000,"y":450,"camera_x_pan":0,"tile_horizontally":True,"x":400},{"element_type":"ParallaxLayer","camera_y_pan":0,"graphics_export":["parallax_5_1","parallax_5_2"],"graphics_swf":"level_graphics/level_bg_forest.swf","camera_z":0,"id":"parallax_5","gap":500,"y":300,"camera_x_pan":0,"tile_horizontally":False,"x":200},{"element_type":"ParallaxLayer","camera_y_pan":0,"graphics_export":["parallax_6_1","parallax_6_2"],"graphics_swf":"level_graphics/level_bg_forest.swf","camera_z":0,"id":"parallax_6","gap":500,"y":160,"camera_x_pan":0,"tile_horizontally":True,"x":200}]


            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)

    def load_level(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Level", "", "JSON Files (*.lvl)")
        if file_name:
            with open(file_name, "r") as file:
                data = json.load(file)
                self.canvas.elements = []
                scale = data["width"] / 760
                self.textbox_scale.setText(str(round(scale, 3)))
                for elem in data.get("elements", []):
                    shape = [(p["x"] / scale, p["y"] / scale) for p in elem["points"]]
                    theme = elem.get("theme", "Wood")
                    texture_swf = elem.get("texture_swf", self.TEXTURE_MAP.get(theme, "level_graphics/level_assets_forest.swf"))
                    element_type = elem.get("element_type")
                    grass_theme = elem.get("grass_theme")
                    self.canvas.elements.append({"shape": shape, "theme": theme, "texture_swf": texture_swf, "element_type": element_type, "grass_theme": grass_theme})
                self.canvas.update()

    def delete_selected(self):
        self.canvas.delete_selected()

class ObjectSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Object")
        self.setGeometry(200, 200, 300, 400)
        
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        
        self.objects = [
            "BallSmallIce", "BallMediumIce", "CubeSmallIce", "CubeMediumIce", "CubeLargeIce", "TriangleSmallIce", "TriangleMediumIce", "RectangleLargeIce", "RectangleMediumIce", "PlankLargeIce", "PlankMediumIce", "PlankSmallIce",
            "BallSmallMetal", "BallMediumMetal", "CubeSmallMetal", "CubeMediumMetal", "CubeLargeMetal", "TriangleSmallMetal", "TriangleMediumMetal", "RectangleLargeMetal", "RectangleMediumMetal", "PlankLargeMetal", "PlankMediumMetal", "PlankSmallMetal",
            "BallSmallStone", "BallMediumStone", "CubeSmallStone", "CubeMediumStone", "CubeLargeStone", "TriangleSmallStone", "TriangleMediumStone", "RectangleLargeStone", "RectangleMediumStone", "PlankLargeStone", "PlankMediumStone", "PlankSmallStone",
            "BallSmallWood", "BallMediumWood", "CubeSmallWood", "CubeMediumWood", "CubeLargeWood", "TriangleSmallWood", "TriangleMediumWood", "RectangleLargeWood", "RectangleMediumWood", "PlankLargeWood", "PlankMediumWood", "PlankSmallWood"
        ]
        
        self.list_widget.addItems(self.objects)
        layout.addWidget(self.list_widget)
        
        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.select_object)
        layout.addWidget(self.select_button)
        
        self.setLayout(layout)
        
    def select_object(self):
        self.selected_object = self.list_widget.currentItem().text()
        self.accept()

class Canvas(QFrame):
    def __init__(self, editor, material_colors):
        super().__init__(editor)
        self.editor = editor
        self.material_colors = material_colors  # Store reference to colors
        self.elements = []
        self.spawnpoints = []  # Array to store spawn points
        self.selected_element = None
        self.current_shape = []
        self.background_image = None
        self.spawn_icon = QPixmap("flag.png")  # Placeholder image

    def set_background(self, file_path):
        self.background_image = QPixmap(file_path)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        x, y = event.position().x(), event.position().y()

        if self.editor.pending_object != "no":
            new_element = {
                "x": event.position().x(),
                "y": event.position().y(),
                "element_type": "DynamicObject",
                "name": self.editor.pending_object,
                "shape": [[event.position().x(), event.position().y()]]
            }
            self.elements.append(new_element)
            self.update()
            self.editor.pending_object = "no"
            return

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
                "grass_theme": self.editor.grass_theme,
                "element_type": "TerrainBlockEntity"
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

            if "shape" in elem and len(elem["shape"]) > 1:
                polygon = QPolygonF([QPointF(p[0], p[1]) for p in elem["shape"]])
                painter.drawPolygon(polygon)
            else:
                # DynamicObject
                painter.drawRect(int(elem['shape'][0][0]), int(elem['shape'][0][1]), 20, 20)

        # Draw spawn points
        for x, y in self.spawnpoints:
            painter.drawPixmap(x - 10, y - 10, 20, 20, self.spawn_icon)

    def delete_selected(self):
        if self.selected_element in self.elements:
            self.elements.remove(self.selected_element)
            self.selected_element = None
            self.update()

class LevelSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Level Settings")
        self.setGeometry(300, 300, 300, 400)

        layout = QVBoxLayout()

        self.label = QLabel("If you're not sure, use the default values.")
        layout.addWidget(self.label)

        self.level_name = QLineEdit()
        self.level_name.setPlaceholderText("Level Name")
        layout.addWidget(QLabel("Level Name:"))
        layout.addWidget(self.level_name)

        self.theme = QComboBox()
        self.theme.addItems(["Forest", "Desert", "Winter", "Mountain", "OilRig"])
        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme)

        self.settings = {}
        fields = [
            "width", "height", "camera_bounds_width", "camera_bounds_height",
            "water_velocity_x", "water_velocity_y", "water_line", "water_density", "water_lineardrag", "water_angulardrag"
        ]
        
        for field in fields:
            self.settings[field] = QLineEdit()
            self.settings[field].setPlaceholderText(field.replace("_", " ").title())
            layout.addWidget(QLabel(field.replace("_", " ").title() + ":"))
            layout.addWidget(self.settings[field])

        self.zoomside = QComboBox()
        self.zoomside.addItems(["width", "height"])
        layout.addWidget(QLabel("Zoom Side:"))
        layout.addWidget(self.zoomside)

        # Set placeholders
        self.settings["width"].setText("760")
        self.settings["height"].setText("668")
        self.settings["camera_bounds_width"].setText("100")
        self.settings["camera_bounds_height"].setText("100")
        self.settings["water_velocity_x"].setText("0")
        self.settings["water_velocity_y"].setText("0")
        self.settings["water_line"].setText("477")
        self.settings["water_density"].setText("32")
        self.settings["water_lineardrag"].setText("15")
        self.settings["water_angulardrag"].setText("15")
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)

    def get_settings(self):
        return {
            "level_name": self.level_name.text(),
            "theme": self.theme.currentText(),
            "zoom_side": self.zoomside.currentText(),
            **{field: int(self.settings[field].text()) for field in self.settings if self.settings[field].text().isdigit()}
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = LevelEditor()
    editor.show()
    sys.exit(app.exec())
