"""
py_to_pdf.py
------------
Converts one or more Python files to a syntax-highlighted PDF.

Usage:
    python py_to_pdf.py file1.py file2.py ... -o output.pdf

Requirements:
    pip install pygments reportlab
"""

import argparse
from pathlib import Path

from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

# Pygments token to color mapping - Dark theme
TOKEN_COLORS = {
    Token.Comment: "6A9955",           # Green
    Token.Keyword: "569CD6",           # Blue
    Token.Name: "D4D4D4",              # Light gray
    Token.Name.Function: "DCDCAA",     # Yellow
    Token.Name.Class: "4EC9B0",        # Cyan
    Token.Name.Builtin: "569CD6",      # Blue
    Token.String: "CE9178",            # Orange
    Token.String.Double: "CE9178",     # Orange
    Token.String.Single: "CE9178",     # Orange
    Token.Number: "B5CEA8",            # Light green
    Token.Operator: "D4D4D4",          # Light gray
    Token.Punctuation: "D4D4D4",       # Light gray
    Token.Whitespace: "D4D4D4",        # Light gray
    Token.Text: "D4D4D4",              # Light gray
}

def get_color(token_type):
    """Get color for a token, checking parent types if exact match not found"""
    if token_type in TOKEN_COLORS:
        return TOKEN_COLORS[token_type]
    # Check parent token types
    for ttype in TOKEN_COLORS:
        if token_type in ttype:
            return TOKEN_COLORS[ttype]
    return "D4D4D4"

def convert(py_files: list, output_pdf: str):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    story = []
    
    code_style = ParagraphStyle(
        'Code',
        fontName='Courier',
        fontSize=8,
        leading=10,
        leftIndent=0.2*inch,
        backColor=colors.HexColor("#1E1E1E"),
        textColor=colors.HexColor("#D4D4D4"),
    )
    
    title_style = ParagraphStyle(
        'Title',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.black,
        spaceAfter=12,
    )

    for py_file in py_files:
        # Add filename as header
        story.append(Paragraph(f"File: {Path(py_file).name}", title_style))
        
        # Read and highlight code
        with open(py_file, "r", encoding="utf-8") as f:
            code = f.read()
        
        # Tokenize and build HTML with colors
        tokens = list(lex(code, PythonLexer()))
        html_lines = []
        current_line = ""
        
        for token_type, value in tokens:
            color = get_color(token_type)
            
            # Handle newlines
            if '\n' in value:
                parts = value.split('\n')
                for i, part in enumerate(parts):
                    if part:
                        escaped = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
                        current_line += f'<font color="#{color}">{escaped}</font>'
                    if i < len(parts) - 1:
                        html_lines.append(current_line)
                        current_line = ""
            else:
                escaped = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
                current_line += f'<font color="#{color}">{escaped}</font>'
        
        if current_line:
            html_lines.append(current_line)
        
        code_html = '<br/>'.join(html_lines)
        story.append(Paragraph(f"<font face='Courier' size='7'>{code_html}</font>", code_style))
        story.append(PageBreak())
        print(f"  Processed {py_file}")

    doc.build(story)
    print(f"\n✅ Saved to: {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Python files to a syntax-highlighted PDF.")
    parser.add_argument("py_files", nargs="+", help="One or more .py files to convert")
    parser.add_argument("-o", "--output", default="output.pdf", help="Output PDF path")
    args = parser.parse_args()

    convert(args.py_files, args.output)