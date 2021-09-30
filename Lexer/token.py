class Token:
   def __init__(self, token_type='UNKNOWN', value=None, string='', line=-1, col=-1):
      self.category = token_type
      self.position = line, col
      self.type = string
      self.value = value
      self.lineno = line

   def __str__(self):
      return f'{self.value:^20} {self.category:<22} {self.type:^20} {self.position[0]:8d}'

   def __repr__(self):
      return f'{self.value:^20} {self.category:<22} {self.type:^20} {self.position[0]:8d}'