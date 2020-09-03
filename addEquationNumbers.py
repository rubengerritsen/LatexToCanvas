#!/usr/bin/env python3
"""
Created on Wed Sep  2 13:22:12 2020

@author: ruben
"""

import sys
import re
import functools
import json
import io

# pandoc imports
import pandocfilters as pf
from pandocfilters import elt as _elt

# GLOBAL VARIABLES
eqNumber = 0
labelMap = dict()

def eprint(*args, **kwargs):
  """ Equivalent to print(), but prints to stderr.

  Needed (for debuggin)since we can't print to stdout, since 
  that disrupts the pipeline.
  """
  print(*args, file=sys.stderr, **kwargs)

def elt(eltType, numargs):  # pylint: disable=invalid-name
    """Returns Element(*value) function to create pandoc AST elements.

    This should be used in place of pandocfilters.elt().  This version
    ensures that the content is stored in a list, not a tuple.
    """
    def Element(*value):  # pylint: disable=invalid-name
        """Creates an element."""
        el = _elt(eltType, numargs)(*value)
        if isinstance(el['c'], tuple):
            el['c'] = list(el['c'])  # The content should be a list, not tuple
        return el
    return Element

def add_eq_number_and_id(fmt, value, num, labelName):
  num = str(num)
  outer = pf.RawInline('html',
                    f'<span id="{labelName}" style="display: inline-block; position: relative; width: 100%;">')
  inner = pf.RawInline('html', '<span style="position: absolute; right: 0em; top: 50%; line-height: 0; ">')
  eqno = pf.Str('(%s)' % num)
  endtags = pf.RawInline('html', '</span></span>')
  return [outer, elt('Math', 2)(*value), inner, eqno, endtags]
    

def createLabelMapAndAddEqNum(key, value, format, meta):
  global eqNumber, labelMap
  if key == 'Math' and value[0]['t'] == 'DisplayMath':
    eqNumber = eqNumber + 1
    label = re.search(r'\\label\{(.*?)\}',value[1])
    labelName = " "
    if label != None: 
      labelName = label.group(1)
      labelMap[labelName] = eqNumber
    return add_eq_number_and_id(format, value, eqNumber, labelName)

def applyLabelMapToText(key, value, format, meta):
  global labelMap
  if key == 'Link':
    if value[0][2] != []:
      if value[0][2][1][1] in labelMap:
        value[1][0]['c'] = '(%s)' % labelMap[value[0][2][1][1]]



if __name__ == "__main__":
  """ Add equation numbers and process references to equations.

  The basic idea is very simple, we run through the document once,
  give every equation an equation number and if the equation has 
  a label, we add the label and eq number to a dictionary called 
  'labelMap'. Then we do a second pass through the document and 
  change all \ref{<something>} to the correct equation number,
  based on the labelMap.
  """
  STDIN = io.TextIOWrapper(sys.stdin.buffer, 'utf-8', 'strict')
  STDOUT = io.TextIOWrapper(sys.stdout.buffer, 'utf-8', 'strict')
  STDERR = io.TextIOWrapper(sys.stderr.buffer, 'utf-8', 'strict')

  fmt = "html"
  doc = json.loads(STDIN.read())
  meta = doc['meta'] 
  blocks = doc['blocks']

  # first pass
  altered = functools.reduce(lambda x, action: pf.walk(x, action, fmt, meta), [createLabelMapAndAddEqNum, ], blocks)

  # second pass
  altered = functools.reduce(lambda x, action: pf.walk(x, action, fmt, meta), [applyLabelMapToText, ], altered)

  # update the document
  doc['blocks'] = altered

  # put the result to stdout
  json.dump(doc, STDOUT)
  STDOUT.flush()
