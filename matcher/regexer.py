import re

class Regexer:

   def __init__(self, regex, to_pattern):

      self.regex = regex
      self.to_pattern = to_pattern

   def apply_to(self, incoming_value):

      work_value = incoming_value

      while re.search(self.regex, work_value):
         work_value = self.apply_once_to(work_value)

      return work_value

   def apply_once_to(self, incoming_value):

      work_value = incoming_value

      for match in re.finditer(self.regex, work_value):
         to_value = self.to_pattern.format(*match.groups())
         work_value = work_value.replace(match.group(), to_value)

      return work_value
