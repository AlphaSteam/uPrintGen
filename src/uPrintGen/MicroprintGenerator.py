import json
import logging
from abc import ABC, abstractmethod
import math
from sys import exit
import re


def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    return ansi_escape.sub('', text)


class MicroprintGenerator(ABC):
    def _load_config_file(self):
        config_file_path = self.config_file_path

        try:
            _file = open(config_file_path)
        except OSError as _:
            logging.error(f"Couldn't open config file '{config_file_path}'. Using default parameters.")
            self.rules = {}
        else:
            with _file:
                logging.info(f"Configuration file '{config_file_path} loaded successfully")
                rules = json.load(_file)

                self.rules = rules

    def _set_default_colors(self):
        fallback_colors = {"background_color": "white", "text_color": "black"}

        default_colors = self.rules.get("default_colors", fallback_colors)

        default_colors["background_color"] = default_colors.get(
            "background_color", fallback_colors["background_color"])

        default_colors["text_color"] = default_colors.get(
            "text_color", fallback_colors["text_color"])

        self.default_colors = default_colors

    def __init__(self, output_filename, config_file_path, text):

        logging.getLogger().setLevel(logging.INFO)

        self.output_filename = output_filename

        self.text_lines = remove_ansi_escape_sequences(text).split('\n')

        self.config_file_path = config_file_path

        self._load_config_file()

        self.scale = self.rules.get("scale", 2)
        self.vertical_spacing = self.rules.get("vertical_spacing", 1)

        self.scale_with_spacing = self.scale * self.vertical_spacing

        self.scaled_microprint_height = len(
            self.text_lines) * self.scale_with_spacing

        if "number_of_columns" not in self.rules:

            self.max_microprint_height = self.rules.get(
                "max_microprint_height", len(self.text_lines) * self.scale_with_spacing)

            self.number_of_columns = math.ceil(
                self.scaled_microprint_height / self.max_microprint_height)
        else:
            self.number_of_columns = self.rules["number_of_columns"]

            self.max_microprint_height = math.floor(
                self.scaled_microprint_height / self.number_of_columns)

        self.column_width = self.rules.get(
            "microprint_width", 120)

        self.column_gap_size = self.rules.get(
            "column_gap_size", 0.2) * self.scale

        self.column_gap_color = self.rules.get("column_gap_color", "white")

        self.microprint_width = (self.column_width + self.column_gap_size) * self.number_of_columns

        self.microprint_height = min(
            len(self.text_lines) * self.scale_with_spacing, self.max_microprint_height)

        self.text_lines_per_column = math.floor(
            self.microprint_height / self.scale_with_spacing)

        self._set_default_colors()

    @classmethod
    def from_text_file(cls, output_filename="microprint.svg", config_file_path="config.json", file_path=""):
        try:
            file = open(file_path)
        except OSError as _:
            exit(f"Couldn't open text file '{file_path}'. Aborting execution.")
        else:
            with file:
                text = file.read()

                return cls(output_filename=output_filename, config_file_path=config_file_path, text=text)

    def check_color_line_rule(self, color_type, text_line):
        text_line = text_line.lower()

        line_rules = self.rules.get("line_rules", {})

        default_color = self.default_colors[color_type]

        for rule in line_rules:
            try:
                pattern = re.compile(rule, re.IGNORECASE)
                if re.search(pattern, text_line):
                    return line_rules[rule].get(color_type, default_color)

            except re.error:
                if text_line.find(rule) != -1:
                    return line_rules[rule].get(color_type, default_color)

        return default_color

    @abstractmethod
    def render_microprint(self):
        pass
