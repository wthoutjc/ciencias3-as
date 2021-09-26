class Token:
   def __init__(self, token_type='UNKNOWN', value=None, string='', line=-1, col=-1):
      self.category = token_type
      self.position = line, col
      self.symbol = string
      self.value = value