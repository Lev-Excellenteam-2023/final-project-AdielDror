import collections
import collections.abc
import pptx

class PowerPointProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all_slides = None

    def load_presentation(self):
        self.all_slides = pptx.Presentation(self.file_name + '.pptx')

    def extract_slide_text(self, slide):
        string_of_slide = ""
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                string_of_slide += shape.text
                string_of_slide += " "
        return string_of_slide

    def process_slides(self):
        string_of_slides = []
        for slide in self.all_slides.slides:
            string_of_slide = self.extract_slide_text(slide)
            string_of_slides.append(string_of_slide)
        return string_of_slides
