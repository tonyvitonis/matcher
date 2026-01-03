from collections import namedtuple
from matcher import parser

class Matcher:

   _pair = namedtuple("Pair", ["left", "right"])

   def __init__(self, query):

      self.tree = parser.tree_for(query)

   def matches(self, tags):

      self.tags = tags
      return self._match_item(self.tree)

   def _or(self, pair):  return self._match_item(pair.left) or self._match_item(pair.right)
   def _and(self, pair): return self._match_item(pair.left) and self._match_item(pair.right)
   def _not(self, pair): return not self._match_item(pair.right)

   def _match_item(self, item):

      matched = self._matched_pair if isinstance(item, tuple) else self._matched_item
      return matched(item)

   def _matched_pair(self, item):

      routines = { "or": self._or, "and": self._and, "not": self._not }
      operator, pair = item

      return routines[operator](self._pair(*pair))

   def _matched_item(self, item):

      return item in self.tags or self._wildcard_matches_any_tag(item)

   def _wildcard_matches_any_tag(self, item):

      if "*" not in item: return False

      return any(self._wildcard_matches_tag(item, tag) for tag in self.tags)

   def _wildcard_matches_tag(self, item, tag):

      if item.startswith("*"): return tag.endswith(item[1:])

      return tag.startswith(item[:-1])
