# μPrintGen

<div style="text-align: center;">
  <img 
      style="
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
      
            "src="https://user-images.githubusercontent.com/30818940/206975537-288bc7c3-2684-4326-ac96-060124aed69c.svg"
      alt="Thumbnail"
      />
</div>

Creates a microprint representation of text or a text file, with rules set by a configuration file. These rules highlight rows with different background and text colors depending on the rules added.

## Usage

### Console command
Installing the package through pip makes the command `generate_microprint` available through the terminal. It accepts three parameters.

 - `-i` The text file to generate as a microprint. Required
 - `-c` The configuration file pathname. Optional, default: `config.json`
 - `-o` The name of the file to be saved. Optional, default: `microprint.svg`
#### Example
```
 generate_microprint -i log.txt -o test2.svg -c config_2.json
```

### As a package
At the same time, the package can be imported from a Python program and used in two ways:
#### From text_file
```
from uPrintGen import SVGMicroprintGenerator

svg = SVGMicroprintGenerator.from_text_file(
    file_path="example.txt", config_file_path="config.json", output_filename="microprint.svg"
    )

svg.render_microprint()
```

Which will save the microprint with the defined name and configuration file.

#### From text

```
from uPrintGen import SVGMicroprintGenerator

example= "blablablabla..."

svg = SVGMicroprintGenerator(text=example, config_file_path="config.json", 
    output_filename="microprint.svg")

svg.render_microprint()
```

### Configuration file
The generator accepts a JSON configuration file with a set of settings that it can change, those settings and their default values are as follows
(comments added for explanation purposes, not valid JSON):

For a valid example [click here](https://github.com/AlphaSteam/uPrintGen/blob/0413461ea1bb4eac68f7cf75bbfbe93367372c64/config.json)

```
{
  # Changes the scale of the font in the generated microprint.
  # Default: 1
  "scale": 2,

  # Changes the vertical spacing between each row.
  # Default: 1
  "vertical_spacing": 1.4,

  # Changes the width of the microprint (or each column if there's more than one)
  # Default: 120
  "microprint_width": 140,

  # Changes the max height of the microprint
  # If "number_of_columns" is set, this parameter is not used.
  # The microprint will be divided in columns to fulfill the desired height.
  # Default: Total log height. No limit
  "max_microprint_height": 300,

  # Changes the number of columns to render.
  # If this parameter is set, "max_microprint_height" is not used.
  # The height of the microprint will be set automatically to fulfill the desired number of columns
  # Default: Total log height. No limit
  "number_of_columns": 4,

  # Changes the size of the gap between columns
  # Default: 0.2
  "column_gap_size": 0.3,

  # Changes the color of the gap between columns
  # Default: "white"
  "column_gap_color": "red",

  # These define the default colors that are used in case no color was defined for
  # a certain rule. If this section is not present, both colors will be the
  # default ones.
  "default_colors": {
    # Default background color in case no background color is set
    # Default: white
    "background_color": "rgb(30, 30, 30)",

    # Default text color in case no background color is set
    # Default: black
    "text_color": "white"
  },

  # This section contains all the rules for the colors of the microprint
  # Each key corresponds to the word it needs to have in a row to use those
  # colors.
  
  # For example, if the key is "error" and the row contains the
  # word "error", then the whole row will be colored with the rules inside the
  # object

  # If any of the two colors is not set (text or background), the default ones 
  # are used.
  "line_rules": {
    "error": {
      "text_color": "red",
      "background_color": "white"
    },
    "installing": {
      "text_color": "white",
      "background_color": "green"
    },
    "command": {
      "text_color": "purple"
    },
    "warning": {
      "text_color": "black",
      "background_color": "yellow"
    },
    "fetching": {
      "text_color": "black",
      "background_color": "orange"
    },
    "complete": {
      "text_color": "green",
      "background_color": "white"
    }
  },
  
  # This section contains fonts to be embedded to the svg. If the fonts work
  # natively in the place where you want to see the svg, there's no need to
  # do this. Monospace fonts recommended.

  "additional_fonts": {

    # This sub-section contains fonts to be loaded from google fonts.

    # "name" is the name to assign the embedded font. This name is the one that
    # needs to be used when setting the font-family of the microprint.

    # "google_font_url" is the url from where to load the google font.

    # Both are required.
    "google_fonts": [
      {
        "name": "Anton",
        "google_font_url": "https://fonts.googleapis.com/css?family=Anton"
      },
      {
        "name": "Acme",
        "google_font_url": "https://fonts.googleapis.com/css?family=Acme"
      }
    ],

    # This sub-section contains fonts to be loaded from the repo, as a truetype
    # font file.

    # "name" is the name to assign the embedded font. This name is the one that
    # needs to be used when setting the font-family of the microprint

    # "truetype_file" is the path to the truetype font file. Includes the name of
    # the file with the extension.

    # Both are required.
    "truetype_fonts": [
      {
        "name": "NotoSans",
        "truetype_file": "./fonts/NotoSans-Regular.ttf"
      }
    ]
  },

  # This sets the font-family of the svg. If the first font is not available 
  # or cannot be loaded in the system, the next one is going to be used. 

  # Default: monospace
  "font-family": "Acme, Anton, NotoSans, Sans, Cursive"
}
```