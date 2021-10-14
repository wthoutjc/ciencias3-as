from os import error
from keywords import OPINV
from tokn import Token
from keyword import *
from node import *

class Semantics:
   def __init__(self , parser):
      self.tree = Node('PROGRAM')
      self.errors = []
      self.parser = parser.pars
      self.current_token = None
      self.last = None

   def ttype(self):
      return self.current_token.type

   def error(self, msg):
      self.errors.append(msg)

   def factor(self, parent:Factor):
      if self.current_token.type == 'ID':
         self.read('ID')
         id = self.last.value
         typeid = ''
         typevalue = ''
         if id in parent.context:
            if parent.context[id][0]:
               typeid = parent.context[id][1]
               typevalue = parent.context[id][2]
         else:
            self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] {id} not defined')
         child = Id(id, typevalue, self.last.lineno)
         child.parent = parent
         parent.addchild(child)
      elif self.current_token.type == 'INT':
         self.read('INT')
         child = Number(self.last.value, 'INT', self.last.lineno)
         child.parent = parent
         parent.addchild(child)
      elif self.current_token.type == 'FLOAT':
         self.read('FLOAT')
         child = Number(self.last.value, 'FLOAT', self.last.lineno)
         child.parent = parent
         parent.addchild(child)
      elif self.current_token.type == 'LPAREN':
         self.read('LPAREN')
         child = Node('(')
         parent.addchild(child)
         child = Expression(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.expression(child)
         self.read('RPAREN')
         child = Node(')')
         parent.addchild(child)
      else:
         self.last = self.current_token
         self.next_token()

   def term(self, parent:Term):
      child = Factor(parent.context)
      child.parent = parent
      parent.addchild(child)
      self.factor(child)
      while self.ttype() == 'MUL' or self.ttype() == 'DIV':
         child = Node(OPINV[self.ttype()])
         parent.addchild(child)
         self.last = self.current_token
         self.next_token()
         child = Factor(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.factor(child)

   def expression(self, parent:Expression):
      if self.ttype() == 'ADD' or self.ttype() == 'SUB':
         child = Node(OPINV[self.ttype()])
         parent.addchild(child)
         self.last = self.current_token
         self.next_token()
      child = Term(parent.context)
      child.parent = parent
      parent.addchild(child)
      self.term(child)
      while self.ttype() == 'ADD' or self.ttype() == 'SUB':
         child  = Node(OPINV[self.ttype()])
         parent.addchild(child)
         self.last = self.current_token
         self.next_token()
         child = Term(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.term(child)

   def condition(self, parent:Condition):
      if self.current_token.type =='ODD':
         self.read('ODD')
         child = Node('ODD')
         parent.addchild(child)
         child = Expression(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.expression(child)
      else:
         child = Expression(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.expression(child)
         if self.ttype() == 'GE' or self.ttype() == 'LE' or self.ttype() == 'GT' or self.ttype() == 'LT' or self.ttype() == 'EQ' or self.ttype() == 'NEQ':
               child = Node(OPINV[self.ttype()])
               parent.addchild(child)
               self.last = self.current_token
               self.next_token()
               child = Expression(parent.context)
               child.parent = parent
               parent.addchild(child)
               self.expression(child)
         else:
               self.last = self.current_token
               self.next_token()
   
   def statement(self, parent:Statement):
      id = ''
      typeid = ''
      typevalue = ''
      if self.current_token.type == 'ID':
         self.read('ID')
         id = self.last.value
         if id in parent.context:
            typeid = parent.context[id][1]
            if typeid == 'CONST' or typeid == 'PROCEDURE':
               self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] cannot assign type {typeid}')
            else:
               typevalue = parent.context[id][2]
         else:
            self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] {id} not defined')
         child = Id(id, typevalue, self.last.lineno)
         parent.addchild(child)
         child.parent = parent
         self.read('ASSIGN')
         child = Node(':=')
         parent.addchild(child)
         child.parent = parent
         child = Expression(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.expression(child)
      elif self.current_token.type == 'CALL':
         self.read('CALL')
         self.read('ID')
         id = self.last.value
         if id in parent.context:
            if parent.context[id][1] != 'PROCEDURE':
               self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] {id} of type {parent.context[id][1]} is not callable')
         else:
            self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] {id} not defined')
         child = Node(f'CALL {id}')
         child.parent = parent
         parent.addchild(child)
      elif self.current_token.type == 'BEGIN':
         self.read('BEGIN')
         child = Node('BEGIN')
         child.parent = parent
         parent.addchild(child)
         child = Statement(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.statement(child)
         while self.current_token.type == 'SEMIC':
            self.read('SEMIC')
            child = Statement(parent.context)
            child.parent = parent
            parent.addchild(child)
            self.statement(child)
         self.read('END')
         child = Node('END')
         child.parent = parent
         parent.addchild(child)
      elif self.current_token.type == 'IF':
         self.read('IF')
         child = Condition(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.condition(child)
         self.read('THEN')
         child = Node('THEN')
         child.parent = parent
         parent.addchild(child)
         child = Statement(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.statement(child)
      elif self.current_token.type == 'WHILE':
         self.read('WHILE')
         child = Node('WHILE')
         child.parent = parent
         parent.addchild(child)
         child = Condition(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.condition(child)
         self.read('DO')
         child = Statement(parent.context)
         child.parent = parent
         parent.addchild(child)
         self.statement(child)
      elif len(self.parser.tokens) == 0:
         pass      

   def block(self, parent):
      blockcontext = {}
      if self.read('CONST'):
         self.read('ID')
         id = self.last.value
         self.read('EQ')
         if self.current_token.type == 'INT':
            self.read('INT')
            if id not in blockcontext:
               blockcontext[id] = [int(self.last.value), 'CONST', 'INT']
            else:
               self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] CONST {id} already defined.')
         elif self.read('FLOAT'):
            if id not in blockcontext:
               blockcontext[id] = [float(self.last.value), 'CONST', 'FLOAT']
            else:
               self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] CONST {id} already defined.')            
         while self.current_token.type == 'COMMA':
               self.read('COMMA')
               self.read('ID')
               id = self.last.value
               self.read('EQ')
               if self.current_token.type == 'INT':
                  self.read('INT')
                  if id not in blockcontext:
                     blockcontext[id] = [int(self.last.value), 'CONST', 'INT']
                  else:
                     self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] name {id} already defined.')
               elif self.read('FLOAT'):
                  if id not in blockcontext:
                     blockcontext[id] = [float(self.last.value), 'CONST', 'FLOAT']
                  else:
                     self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] name {id} already defined.')  
         self.read('SEMIC')
      while self.current_token.type == 'VAR':
         self.read('VAR')
         toadd = []
         self.read('ID')
         toadd.append(self.last.value)
         while self.current_token.type == 'COMMA':
               self.read('COMMA')
               self.read('ID')
               toadd.append(self.last.value)
         self.read('COLON')
         if self.current_token.type == 'FLOAT':
            self.read('FLOAT')
            for id in toadd:
               if id not in blockcontext:
                  blockcontext[id] = [None, 'VAR', 'FLOAT']
               else:
                  self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] name {id} already defined.')
         elif self.read('INT'):
            for id in toadd:
               if id not in blockcontext:
                  blockcontext[id] = [None, 'VAR', 'INT']
               else:
                  self.error(f'ERROR: Line[{"0" + str(self.last.lineno) if self.last.lineno < 10 else self.last.lineno}] name {id} already defined.')
         self.read('SEMIC')
      while self.current_token.type == 'PROCEDURE':
         self.read('PROCEDURE')
         self.read('ID')
         id = self.last.value
         if id not in blockcontext:
            blockcontext[id] = [None, 'PROCEDURE', '']
         else:
            self.error(f'ERROR: Line[{"0" + self.last.lineno if self.last.lineno < 10 else self.last.lineno}] name {id} already defined.')
         self.read('SEMIC')
         parent.context.update(blockcontext)
         child = Procedure(dict(parent.context))
         child.name += f' {id}'
         parent.addchild(child)
         child.parent = parent
         self.block(child)
         self.read('SEMIC')
      parent.context.update(blockcontext)
      child = Statement(parent.context)
      parent.addchild(child)
      child.parent = parent
      self.statement(child)

   def program(self, parent):
      self.next_token()
      child = Block({})
      parent.addchild(child)
      child.parent = parent
      self.block(child)
      self.read('DOT')

   def next_token(self):
        self.current_token = self.parser.token()

   def read(self, ttype):
      if ttype == self.current_token.type:
         self.last = self.current_token
         #print(f'Se lee correctamente {ttype}')
         self.next_token()
         return True
      else:
         #print(f'Error mientras se lee {ttype} esperaba {self.current_token.type}')
         self.next_token()
      return False

   def removebridges(self, node:Node):
      if type(node) == Term or type(node) == Factor:
         if len(node.parent.childs) == 1:
            node.parent.childs = node.childs
            for child in node.childs:
               child.parent = node.parent
      for child in node.childs:
         self.removebridges(child)
        
   def replaceleaves(self, node, index):
      if type(node) == Term or type(node) == Factor or type(node) == Expression:
         if len(node.childs) == 1:
            node.parent.childs[index] = node.childs[0]
      for i, child in enumerate(node.childs):
         self.replaceleaves(child, i)


   def printtree(self, node, ident):
      print(f'{"   " * ident}{node}')
      for child in node.childs:
         self.printtree(child, ident + 1)

   def updatecontext(self, node:Node):
      if type(node) == Statement and len(node.childs) == 3:
         if type(node.childs[0]) == Id and type(node.childs[2]) == Number:
            id = node.childs[0].value
            typeid = ''
            typevalueid = ''
            if id in node.context:
               typeid = node.context[id][2]
               typevalueid = node.context[id][1]
            typevalue = node.childs[2].type
            if typeid == 'INT' and typevalueid == 'VAR':
               if typevalue == 'INT':
                  node.context[id][0] = node.childs[2].value
               else:
                  self.error(f'ERROR: Line[{"0" + str(node.childs[0].lineno) if node.childs[0].lineno < 10 else node.childs[0].lineno}] cannot assign type FLOAT')
            elif typeid == 'FLOAT' and typevalueid == 'VAR':
               node.context[id][0] = node.childs[2].value
      for child in node.childs:
         self.updatecontext(child)

   def validatevariables(self, node:Node):
      if type(node) == Expression:
         for child in node.childs:
            if type(child) == Id:
               id = child.value
               if id in node.context:
                  if not node.context[id][0]:
                     self.error(f'ERROR: Line[{"0" + str(child.lineno) if child.lineno < 10 else child.lineno}] VAR {id} not initialized')

      for child in node.childs:
         self.validatevariables(child)

            

   def analyze(self):
      self.program(self.tree)
      self.removebridges(self.tree)
      self.replaceleaves(self.tree, 0)
      self.updatecontext(self.tree)
      self.validatevariables(self.tree)
      self.printtree(self.tree, 0)