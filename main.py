#!.venv/bin/python

import argparse
import sys
from PIL import ImageGrab, Image
import pyocr
import pyocr.builders
from deep_translator import GoogleTranslator
import pyocr.libtesseract
import pyocr.tesseract
import pyperclip

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Extract text from an image in the clipboard and translate it. You can control the source/target languages and actions."
)
parser.add_argument(
    "-s", "--source", type=str, default="eng", help="Source language code in 3-letter format"
)
parser.add_argument(
    "-t", "--target", type=str, default="ja", help="Target language code in 2-letter format"
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="both",
    choices=["none", "original", "translated", "both"],
    help="Output original text, translated text, or both",
)
parser.add_argument(
    "-c",
    "--copy",
    type=str,
    default="none",
    choices=["none", "original", "translated"],
    help="Copy original text or translated text to clipboard",
)
args = parser.parse_args()

# Check if there is anything to do
do_ocr = args.output not in ["none"] or args.copy not in ["none"]
do_translate = args.output in ["translated", "both"] or args.copy in ["translated"]
if not do_ocr:
    print("Nothing to do", file=sys.stderr)
    exit(1)

# Grab clipboard image
image = ImageGrab.grabclipboard()
if not isinstance(image, Image.Image):
    print("No image found in clipboard", file=sys.stderr)
    exit(1)

# Get OCR tool
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found. Try installing Tesseract.", file=sys.stderr)
    exit(1)
tool = tools[0]

# Extract text from image
builder = pyocr.builders.TextBuilder(tesseract_layout=3)
text = tool.image_to_string(
    image,
    lang=args.source,
    builder=builder,
)

# Translate text using Google Translate
if do_translate:
    translator = GoogleTranslator(source="auto", target=args.target)
    translated_text = translator.translate(text)

# Output results
if args.output == "original":
    print(text)
elif args.output == "translated":
    print(translated_text)
elif args.output == "both":
    print("# Original text")
    print(text)
    print()
    print("# Translated text")
    print(translated_text)

# Copy results to clipboard
if args.copy == "original":
    pyperclip.copy(text)
elif args.copy == "translated":
    pyperclip.copy(translated_text)
