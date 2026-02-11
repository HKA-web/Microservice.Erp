import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.relpath(os.path.join(cwd)))
sys.path.append(os.path.relpath(os.path.join(cwd, 'lib')))

from pythonnet import load

load('coreclr', )
import clr

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cwd + '/lib/win.x64/', )
clr.AddReference('ERPro.NET')
try:
    from ERPro.NET import (
        Spreadsheet as SpreadsheetClass,
        Document as DocumentClass,
        PdfViewer as PdfViewerClass,
    )
except:
    SpreadsheetClass, DocumentClass, PdfViewerClass = None, None, None

Spreadsheet = SpreadsheetClass()
Document = DocumentClass()
PdfViewer = PdfViewerClass()

__all__ = [
    Spreadsheet,
    Document,
    PdfViewer,
]
