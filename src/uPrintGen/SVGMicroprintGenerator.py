from MicroprintGenerator import MicroprintGenerator
import svgwrite
import logging


class SVGMicroprintGenerator(MicroprintGenerator):

    def _load_svg_fonts(self):

        additional_fonts = self.rules.get("additional_fonts",
                                          {"google_fonts": [],
                                           "truetype_fonts": []})

        google_fonts = additional_fonts.get("google_fonts", [])

        truetype_fonts = additional_fonts.get("truetype_fonts", [])

        for count, google_font in enumerate(google_fonts):
            name = google_font["name"]
            url = google_font["google_font_url"]

            self.drawing.embed_google_web_font(name, url)

        for count, truetype_font in enumerate(truetype_fonts):
            name = truetype_font["name"]
            truetype_file = truetype_font["truetype_file"]

            self.drawing.embed_font(name, truetype_file)

    def __init__(self, output_filename="microprint.svg", text=""):
        super().__init__(output_filename, text)

        self.drawing = svgwrite.Drawing(
            output_filename, (self.microprint_width, self.microprint_height), debug=False)

        self.font_family = self.rules.get("font-family", "Sans")

        self._load_svg_fonts()

    def render_microprint_column(self, first_line, last_line, x_with_gap, y, current_line):

        backgrounds = self.drawing.add(self.drawing.g())

        default_text_color = self.default_colors["text_color"]

        texts = self.drawing.add(self.drawing.g(
            font_size=self.scale, fill=default_text_color))

        attributes = {'xml:space': 'preserve',
                      "font-family": self.font_family}

        texts.update(attributes)

        for text_line in self.text_lines[first_line:last_line]:
            background_color = self.check_color_line_rule(
                color_type="background_color", text_line=text_line)

            background_rect = self.drawing.rect(insert=(x_with_gap, y),
                                                size=(self.column_width,
                                                      self.scale + 0.3),
                                                rx=None, ry=None, fill=background_color)

            text_color = self.check_color_line_rule(
                color_type="text_color", text_line=text_line)

            text = self.drawing.text(text_line, insert=(x_with_gap, y),
                                     fill=text_color, dominant_baseline="hanging")

            text.update({"data-text-line": current_line})
            background_rect.update({"data-text-line": current_line})

            backgrounds.add(background_rect)
            texts.add(text)

            y += self.scale_with_spacing

            current_line += 1

    def render_microprint(self):
        logging.info('Generating svg microprint')

        default_background_color = self.default_colors["background_color"]

        self.drawing.add(self.drawing.rect(insert=(0, 0), size=('100%', '100%'),
                                           rx=None, ry=None, fill=default_background_color))

        current_line = 0

        for column in range(self.number_of_columns):
            x = math.ceil(column * self.column_width)
            x_with_gap = x if column == 0 else x + self.column_gap_size

            self.drawing.add(self.drawing.rect(insert=(x_with_gap, 0), size=(self.column_width, '100%'),
                                               rx=None, ry=None, fill=default_background_color))

            if column != 0:
                self.drawing.add(self.drawing.rect(insert=(x, 0), size=(self.column_gap_size, '100%'),
                                                   rx=None, ry=None, fill=self.column_gap_color))

            y = 0

            first_line = math.ceil(column * self.text_lines_per_column)

            last_line = min(
                math.ceil((column + 1) * self.text_lines_per_column), len(self.text_lines) - 1)

            if first_line >= len(self.text_lines):
                break

            self.render_microprint_column(
                first_line=first_line, last_line=last_line, x_with_gap=x_with_gap, y=y, current_line=current_line)

            current_line += self.text_lines_per_column

        self.drawing.save()