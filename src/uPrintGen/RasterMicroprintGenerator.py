from MicroprintGenerator import MicroprintGenerator
from PIL import Image, ImageDraw, ImageFont
import logging


class RasterMicroprintGenerator(MicroprintGenerator):

    def __init__(self, output_filename="microprint.png", text=""):
        super().__init__(output_filename, text)
        default_background_color = self.default_colors["background_color"]

        self.img = Image.new('RGB', (int(self.microprint_width), int(self.microprint_height)),
                             color=default_background_color)

        self.drawing = ImageDraw.Draw(self.img)
        self.drawing.fontmode = "1"

    def render_microprint(self):
        logging.info('Generating raster microprint')

        font = ImageFont.truetype(
            "fonts/NotoSans-Regular.ttf", int(self.scale))

        y = 0

        for text_line in self.text_lines:
            background_color = self.check_color_line_rule(
                color_type="background_color", text_line=text_line)

            self.drawing.rectangle([(0, y - self.scale_with_spacing), (self.microprint_width, y)],
                                   fill=background_color, outline=None, width=1)

            text_color = self.check_color_line_rule(
                color_type="text_color", text_line=text_line)

            self.drawing.text((0, y), text=text_line, font=font,
                              fill=text_color, anchor="ls")

            y += self.scale_with_spacing

        self.img.save(self.output_filename)
