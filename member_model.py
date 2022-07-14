"""
Member class to store details of perticular member
ex. name, dues, total dues
"""
class MemberModel:
  def __init__(self, name):
    self._name = name
    self._due = {}
    self._own = {}
    self._total_due = 0
    self._total_own = 0
    self._moveIn = False
    self._moveOut = True

  # def moveIn(self):
  #   self.moveIn = True
  #   self.moveOut = False
  #   self._due = {}
  #   self._own = {}
  #   self._total_due = 0
  #   self._total_own = 0
  #   return True
  #
  # def verifyAndMoveOut(self):
  #   if self._total_due == 0:
  #     self.moveOut = True
  #     self.moveIn = False
  #     self._due = {}
  #     self._own = {}
  #     self._total_due = 0
  #     self._total_own = 0
  #     return True
  #   return False