import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer
from itertools import islice

class Suguru():
  def __init__(self, groups, given, width, heigth):
    self.groups = groups
    self.given = given
    self.width = width
    self.height = height


if __name__ == "__main__":
  
  fd = open("SUG.pdf", "rb")
  viewer = SimplePDFViewer(fd)
  viewer.render()
  print(viewer.canvas.text_content)
