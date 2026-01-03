from matcher import querytools
import re

def tree_for(query):

   query = querytools.normalized(query)

   if not _is_valid(query):
      raise Exception("syntax error at '{}'".format(query))

   operators = ( ("or", _pair_around), ("and", _pair_around), ("not", _pair_after) )

   for operator, function in operators:
      pair = function(query, operator)
      if pair is not None: return (operator, pair)

   if not _is_valid_tag_matcher(query):
      raise Exception("syntax error at '{}'".format(query))

   return query

def _is_valid(query):

   for operator in [ "and", "or" ]:
      left, right = operator + " ", " " + operator
      if query.startswith(left) or query.endswith(right):
         return False

   return True

def _is_valid_tag_matcher(query):

   if " " in query or query == "not": return False
   if "*" not in query: return True
   if query.count("*") > 1: return False

   return query.startswith("*") or query.endswith("*")

def _pair_around(query, keyword):

   return _pair_for_pattern(query, keyword, " {} ")

def _pair_after(query, keyword):

   return _pair_for_pattern(query, keyword, "^{} ")

def _pair_for_pattern(query, keyword, pattern):

   start, end = _outermost(query)
   outermost = query[start:end+1]
   regex = pattern.format(keyword)
   match = re.search(regex, outermost)

   if match is None: return None

   left = query[:start+match.start()]
   right = query[start+match.start()+len(match.group()):]

   return tree_for(left), tree_for(right)

def _outermost(query):

   open, close = querytools.leftmost_paren_group(query)
   end_of_string = len(query) - 1

   if open < 0: return 0, end_of_string
   if open > 0: return 0, open - 1

   start = close + 1
   next_open_paren = querytools.leftmost_paren_group(query[start:])[0]
   end = end_of_string if next_open_paren < 0 else start + next_open_paren - 1

   return start, end
