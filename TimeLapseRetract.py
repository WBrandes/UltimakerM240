# Created by Wayne Porter
# Retraction by William Brandes

from ..Script import Script

class TimeLapseRetract(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Time Lapse Retract",
            "key": "TimeLapseRetract",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "trigger_command":
                {
                    "label": "Trigger camera command",
                    "description": "Gcode command used to trigger camera.",
                    "type": "str",
                    "default_value": "M240"
                },
                "pause_length":
                {
                    "label": "Pause length",
                    "description": "How long to wait (in ms) after camera was triggered.",
                    "type": "int",
                    "default_value": 700,
                    "minimum_value": 0,
                    "unit": "ms"
                },
                "retraction_distance":
                {
                    "label": "Retraction Distance",
                    "description": "How much the printer should retract when taking a picture.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 4.5
                },
                "park_print_head":
                {
                    "label": "Park Print Head",
                    "description": "Park the print head out of the way. Assumes absolute positioning.",
                    "type": "bool",
                    "default_value": true
                },
                "head_park_x":
                {
                    "label": "Park Print Head X",
                    "description": "What X location does the head move to for photo.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0,
                    "enabled": "park_print_head"
                },
                "head_park_y":
                {
                    "label": "Park Print Head Y",
                    "description": "What Y location does the head move to for photo.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 190,
                    "enabled": "park_print_head"
                },
                "park_feed_rate":
                {
                    "label": "Park Feed Rate",
                    "description": "How fast does the head move to the park coordinates.",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 9000,
                    "enabled": "park_print_head"
                }
            }
        }"""

    def execute(self, data):
        feed_rate = self.getSettingValueByKey("park_feed_rate")
        park_print_head = self.getSettingValueByKey("park_print_head")
        x_park = self.getSettingValueByKey("head_park_x")
        y_park = self.getSettingValueByKey("head_park_y")
        trigger_command = self.getSettingValueByKey("trigger_command")
        pause_length = self.getSettingValueByKey("pause_length")
        retraction_distance = self.getSettingValueByKey("retraction_distance")
        gcode_to_append = ";TimeLapse Begin\n"
        if park_print_head:
            gcode_to_append += self.putValue(G = 1, F = feed_rate, X = x_park, Y = y_park) + ";Park print head\n"
        gcode_to_append += self.putValue(M = 400) + ";Wait for moves to finish\n"
        gcode_to_append += trigger_command + ";Snap Photo\n"
        gcode_to_append += self.putValue(G = 4, P = pause_length) + ";Wait for camera\n"
        gcode_to_append += ";TimeLapse End\n"
        current_e = 0.0
        for layer in data:
            # Check that a layer is being printed
            lines = layer.split("\n")
            for line in lines:
                if "G1" in line:
                    e_ind = line.find("e", 0, len(line))
                    if e_ind != -1:
                        current_e = float(line[e_ind+1:])

                if ";LAYER:" in line:
                    index = data.index(layer)
                    layer += self.putValue("G1 F" + feed_rate + " E" + str(current_e - retraction_distance)) + "\n"
                    layer += gcode_to_append
                    layer += self.putValue("G1 F" + feed_rate + " E" + str(current_e)) + "\n"
                    data[index] = layer
                    break
        return data
