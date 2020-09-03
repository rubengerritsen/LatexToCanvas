#!/usr/bin/env python3
"""
Created on Wed Sep  2 13:22:12 2020

@author: ruben
"""

from __future__ import print_function
import sys
import pandocfilters as pf

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def eprint(*args, **kwargs):
  """ Equivalent to print(), but prints to stderr.

  Needed (for debuggin)since we can't print to stdout, since 
  that disrupts the pipeline.
  """
  print(*args, file=sys.stderr, **kwargs)

def get_default_style():
    """ CSS specification of the code block style.
    
    might interfere with the formatting done by Canvas, so 
    keep it basic.
    """
    return ''

def highlightCode(code, language='python', style='default'):
    """ Highlights plain text string as code.
    
    @params: 
        code: a string containing the basic code to format
        language: programming language to base highlighting on
        style: choose color scheme options: ['default', 'emacs', 'friendly', 
               'colorful', 'autumn', 'murphy', 'manni', 'monokai', 'perldoc', 
               'pastie', 'borland', 'trac', 'native', 'fruity', 'bw', 'vim', 
               'vs', 'tango', 'rrt', 'xcode', 'igor', 'paraiso-light', 
               'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 
               'rainbow_dash', 'abap']
    """
    lexer = language
    style = style
    formatter = HtmlFormatter(style=style,
                              linenos=False,
                              noclasses=True,
                              cssclass='',
                              cssstyles= get_default_style(),
                              nobackground=True
                              )
    html = highlight(code, get_lexer_by_name(lexer), formatter)
    return html
    

def formatCode(key, value, format, meta):
  style = 'default'
  if key == 'CodeBlock':
    if value[0][1]:
      return pf.Plain([pf.RawInline("html", highlightCode(value[1],style=style, language=value[0][1][0]))])
    else:
      return pf.Plain([pf.RawInline("html", highlightCode(value[1],style=style, language='text'))])

if __name__ == "__main__":
  pf.toJSONFilter(formatCode)