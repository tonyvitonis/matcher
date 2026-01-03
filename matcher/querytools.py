from collections import defaultdict
import re

from matcher.regexer import Regexer

def normalized(incoming_value):

   work_value = _normalize_spaces(incoming_value)
   work_value = _normalize_parens(work_value)

   return work_value.strip()

def _normalize_spaces(incoming_value):

   work_value = incoming_value.strip()
   work_value = re.sub(r"\s+", " ", work_value)
   work_value = work_value.replace("( ", "(")
   work_value = work_value.replace(" )", ")")

   return work_value

def _normalize_parens(incoming_value):

   if not _parens_are_balanced(incoming_value):
      raise Exception("unbalanced parentheses")

   if re.search(r"\)\s*\(", incoming_value):
      raise Exception("consecutive groups")

   work_value = _expand_before_open_paren(incoming_value)
   work_value = _expand_after_close_paren(work_value)
   work_value = _remove_doubled_parens(work_value)
   work_value = _remove_parens_not_containing_spaces(work_value)
   work_value = _remove_outermost_parens(work_value)

   return work_value

def _parens_are_balanced(incoming_value):

   if "(" not in incoming_value:
      return ")" not in incoming_value

   open, close = leftmost_paren_group(incoming_value)
   if open < 0: return False

   inside_leftmost_group = incoming_value[open+1:close]
   right_of_leftmost_group = incoming_value[close+1:]

   return (
      _parens_are_balanced(inside_leftmost_group) and
      _parens_are_balanced(right_of_leftmost_group)
   )

def _expand_before_open_paren(incoming_value):

   regex = r"([^() ])\("  # not-space-or-paren(
   to_pattern = "{} ("    # not-space-or-paren (

   return Regexer(regex, to_pattern).apply_once_to(incoming_value)

def _expand_after_close_paren(incoming_value):

   regex = r"\)([^() ])"  # )not-space-or-paren
   to_pattern = ") {}"    # ) not-space-or-paren

   return Regexer(regex, to_pattern).apply_once_to(incoming_value)

def _remove_doubled_parens(incoming_value):

   regex = r"\(\(([^()]+)\)\)"  # ((not-paren))
   to_pattern = "({})"          # (not-paren)

   return Regexer(regex, to_pattern).apply_to(incoming_value)

def _remove_parens_not_containing_spaces(incoming_value):

   regex = r"\(([^() ]*)\)"  # (not-paren-or-space)
   to_pattern = "{}"         # not-paren-or-space

   return Regexer(regex, to_pattern).apply_to(incoming_value)

def _remove_outermost_parens(incoming_value):

   work_value = incoming_value

   while _outermost_parens_are_paired(work_value):
      work_value = work_value[1:-1]

   return work_value

def _outermost_parens_are_paired(incoming_value):

   OUTERMOST = (0, len(incoming_value) - 1)
   return leftmost_paren_group(incoming_value) == OUTERMOST

def leftmost_paren_group(incoming_value):

   NOT_GROUPED = (-1, -1)
   if not "(" in incoming_value: return NOT_GROUPED

   open = incoming_value.index("(")
   running_paren_count = 1

   increment_for = defaultdict(int)
   increment_for["("] = 1
   increment_for[")"] = -1

   for close in range(open + 1, len(incoming_value)):
      running_paren_count += increment_for[incoming_value[close]]
      if running_paren_count == 0:
         return (open, close)

   return NOT_GROUPED
