
class Node:
   def __init__(self, name):
      self.parent = None
      self.name = name
      self.childs = []

   def __repr__(self):
      return self.name

   def addchild(self, child):
      self.childs.append(child)

   def __repr__(self):
      return self.name

class Block(Node):
   def __init__(self, context):
       super().__init__('BLOCK')
       self.context = context

class Statement(Node):
   def __init__(self, context):
       super().__init__('STATEMENT')
       self.context = context

class Condition(Node):
   def __init__(self, context):
       super().__init__('CONDITION')
       self.context = context
       self.type = 'boolean'
       self.value = None

class Expression(Node):
   def __init__(self, context):
       super().__init__('EXPRESSION')
       self.context = context
       self.type = ''
       self.value = None

class Term(Node):
   def __init__(self, context):
       super().__init__('TERM')
       self.context = context
       self.type = ''
       self.value = None

class Factor(Node):
   def __init__(self, context):
       super().__init__('FACTOR')
       self.context = context
       self.type = ''
       self.value = None

class Id(Node):
   def __init__(self, value, context):
       super().__init__('ID')
       self.context = context
       self.type = ''
       self.value = value

class Procedure(Node):
   def __init__(self, context):
       super().__init__('PROCEDURE')
       self.context = context

class Id(Node):
   def __init__(self, value, tp, lineno):
       super().__init__('ID')
       self.type = tp
       self.value = value
       self.lineno = lineno

   def __repr__(self):
       return str(self.value)

class Number(Node):
   def __init__(self, value, tp, lineno):
       super().__init__('NUMBER')
       self.type = tp
       self.value = value
       self.lineno = lineno

   def __repr__(self):
       return str(self.value)