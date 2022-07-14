"""
This class implement core logic behind
all commands
"""
import itertools
from member_model import MemberModel

class Expense:
  def __init__(self):
    self.name_to_model_map = {}
    self.member_count = 0

  def move_in_command(self, command_data):
    """
    process move in command data and print approriate message.
    :param command_data: command details <str>
    :return: output_msg <str>
    """
    if len(command_data) != 2:
      return "INVALID ARGUMENT PASS TO MOVE_IN COMMAND"

    member_name = command_data[1]
    # first check if member is already part of group/house
    # if not then check total member in house
    # else create member model and print SUCCESS
    if member_name in self.name_to_model_map:
      return "MEMBER ALREADY MOVE_IN"
    elif self.member_count >= 3:
      return "HOUSEFUL"
    else:
      member_obj = MemberModel(member_name)
      self.name_to_model_map[member_name] = member_obj
      self.member_count += 1
      return "SUCCESS"

  def _settle_with_each_other(self, owns_name, lent_name, amount):
    # settle amount to each other if lent own something alread from owns
    # if lent already borrow some money earlier from owns
    # then settle that amount by reducing from lent _own
    # and return remaining amount
    owns = self.name_to_model_map[owns_name]
    lent = self.name_to_model_map[lent_name]

    if owns_name in lent._own and lent._own[owns_name] > 0:
      # update again in case if some remain amount left over.
      lent_own_amount = lent._own[owns_name]
      if amount <= lent_own_amount:
        lent._total_own -= amount
        lent._own[owns_name] = lent._own.get(owns_name, 0) - amount

        owns._total_due -= amount
        owns._due[lent_name] = owns._due.get(lent_name, 0) - amount
        amount = 0
      else:
        lent._total_own -= lent_own_amount
        lent._own[owns_name] = lent._own.get(owns_name, 0) - lent_own_amount

        owns._total_due -= lent_own_amount
        owns._due[lent_name] = owns._due.get(lent_name, 0) - lent_own_amount
        amount -= lent_own_amount

    return amount

  def _update_each_account_data(self, owns_name, lent_name, remain_amount):
    """
    update each other (own, lent) entry for remaining amount.
    :param owns_name: owne name <str>
    :param lent_name: lenter name <str>
    :param remain_amount: amount <int>
    :return: None
    """
    owns = self.name_to_model_map[owns_name]
    lent = self.name_to_model_map[lent_name]

    # update again in case if some remain amount left over.
    # update _total_own and create entry for lenter in _own for owne account.
    # update _total_due  and create entry for owne in _due in lenter account.
    owns._total_own += remain_amount
    lent._total_due += remain_amount
    lent._due[owns_name] = lent._due.get(owns_name,
                                         0) + remain_amount
    owns._own[lent_name] = owns._own.get(lent_name,
                                         0) + remain_amount

  def _settle_with_each_other_owne(self, owne_name, other_owne_name,
                                     lent_name, remain_amount):
    """
    settle amount with each other owne and give to lenter
    :param owne_name:
    :param other_owne_name:
    :param lent_name:
    :param remain_amount:
    :return: remaining amount
    """
    owne_data = self.name_to_model_map[owne_name]
    other_owne_data = self.name_to_model_map[other_owne_name]
    lent_data = self.name_to_model_map[lent_name]
    if owne_name not in other_owne_data._own or \
      other_owne_data._own[owne_name] == 0:
      return remain_amount

    owne_amount = other_owne_data._own[owne_name]
    if (owne_amount >= remain_amount):
      other_owne_data._own[owne_name] -= remain_amount
      other_owne_data._own[lent_name] = \
        other_owne_data._own.get(lent_name, 0) + remain_amount
      owne_data._total_due -= remain_amount
      owne_data._due[other_owne_name] -= remain_amount
      return 0
    else:
      other_owne_data._own[owne_name] -= owne_amount
      other_owne_data._own[lent_name] = \
        other_owne_data._own.get(lent_name, 0) + owne_amount
      owne_data._total_due -= owne_amount
      owne_data._due[other_owne_name] -= owne_amount
      remain_amount -= owne_amount
      return remain_amount

  def spend_command(self, command_data):
    """
    process spend command command data and print approriate message.
    :param command_data: command details <str>
    :return: output_msg <str>
    """
    if len(command_data) < 4:
      return "INVALID ARGUMENT PASS TO SPEND COMMAND"

    amount = int(command_data[1])
    lent, lent_name = None, command_data[2]

    # check lenter is present in group/house
    if lent_name not in self.name_to_model_map:
      return "MEMBER_NOT_FOUND"

    # check if all ownes present in house or not
    for owes_name in command_data[3:]:
      if owes_name not in self.name_to_model_map:
        return "MEMBER_NOT_FOUND"

    owes_len = len(command_data) - 2
    amount_spend_on_each = int(amount / owes_len)

    lent = self.name_to_model_map[lent_name]

    # calculate each owes and lenter amount
    # update accordigly each model values
    for owne_name in command_data[3:]:
      owes = self.name_to_model_map[owne_name]
      # here assuming owes will be present.
      # settle amount if possible with own and lenter
      remain_amount = self._settle_with_each_other(owne_name, lent_name,
                                                   amount_spend_on_each)

      # settle amount with among ownes
      for other_owne_name in command_data[3:]:
        if owne_name != other_owne_name:
          other_owne_data = self.name_to_model_map[other_owne_name]
          if owne_name in other_owne_data._own:
            remain_amount = \
              self._settle_with_each_other_owne(
                owne_name, other_owne_name, lent_name, remain_amount)

      # do settle if possible
      for lent_owes, lent_owes_amount in lent._own.items():
        for owes_owes, owes_owes_amount in owes._own.items():
          if lent_owes == owes_owes:
            lent_owes_obj = self.name_to_model_map[lent_owes]
            if (owes_owes_amount >= remain_amount):

              # update lenter amount and reduce from his account
              lent._total_own -= remain_amount
              lent._own[lent_owes] = lent._own.get(lent_owes, 0) - remain_amount

              # update ownes ammount and increase from his amount
              owes._total_own += remain_amount
              owes._own[lent_owes] = owes._own.get(lent_owes, 0) + remain_amount

              # update details in account to whom we are settling
              lent_owes_obj._due[lent_name] -= remain_amount
              lent_owes_obj._due[owes_name] += remain_amount
              remain_amount = 0
            else:
              remain_amount -= owes_owes_amount
              # update lenter amount and reduce from his account
              lent._total_own -= owes_owes_amount
              lent._own[lent_owes] = lent._own.get(lent_owes, 0) - owes_owes_amount

              # update ownes ammount and increase from his amount
              owes._total_own += owes_owes_amount
              owes._own[lent_owes] = owes._own.get(lent_owes, 0) + owes_owes_amount

              # update details in account to whom we are settling
              lent_owes_obj._due[lent_name] -= owes_owes_amount
              lent_owes_obj._due[owes_name] += owes_owes_amount

      # update remaning amount to each other account if any
      self._update_each_account_data(owne_name, lent_name, remain_amount)
    return "SUCCESS"

  def dues_command(self, command_data):
    """
    process dues command command data and print approriate message.
    :param command_data: command details <str>
    :return: output_msg <str>
    """
    if len(command_data) != 2:
      return "INVALID ARGUMENT PASS TO DUES COMMAND"

    member_name = command_data[1]
    if member_name not in self.name_to_model_map:
      return "MEMBER_NOT_FOUND"

    member = self.name_to_model_map[member_name]
    # fetch dues from model map
    data = {}
    for name, value in self.name_to_model_map.items():
      if name != member_name:
        data[name] = 0
        if name in member._own:
          data[name] += member._own[name]

    # sort data based on amount
    sorted_data = []
    sorted_data_by_value = \
      sorted(data.items(), key=lambda x: (x[1], x[0]), reverse=True)
    for k,v in itertools.groupby(sorted_data_by_value, lambda item: item[1]):
        sorted_data.extend(sorted(v))

    message = ""
    for name, amount in sorted_data:
      message += "{} {}\n".format(name, amount)
    return message.strip()

  def clear_due_command(self, command_data):
    """
    process clear due command data and print approriate message.
    :param command_data: command details <str>
    :return: output_msg <str>
    """
    if len(command_data) != 4:
      return "INVALID ARGUMENT PASS TO CLEAR_DUE COMMAND"

    owes, lent = None, None
    owes_name, lent_name, amount = \
      command_data[1], command_data[2], int(command_data[3])

    # check for owes and lenter both are present in house/group
    if owes_name not in self.name_to_model_map:
      return "MEMBER_NOT_FOUND"

    if lent_name not in self.name_to_model_map:
      return "MEMBER_NOT_FOUND"

    owes = self.name_to_model_map[owes_name]
    lent = self.name_to_model_map[lent_name]

    # check for amount less/equal to total own
    # if not print approiate message
    if owes._total_own >= amount:
      owes._total_own -= amount
      owes._own[lent_name] -= amount

      lent._total_due -= amount
      lent._due[owes_name] -= amount

      return "{}".format(owes._own[lent_name])
    else:
      return "INCORRECT_PAYMENT"

  def move_out_command(self, command_data):
    """
    process move out command data and print approriate message.
    :param command_data: command details <str>
    :return: output_msg <str>
    """
    if len(command_data) != 2:
      return "INVALID ARGUMENT PASS TO MOVE_OUT COMMAND"

    member_name = command_data[1]
    if member_name not in self.name_to_model_map:
      return "MEMBER_NOT_FOUND"

    # if member present then fetch data and verify
    # total due and own if its zero then print SUCCESS else FAILURE
    member_data = self.name_to_model_map[member_name]
    if member_data._total_due == 0 and member_data._total_own == 0:
      del self.name_to_model_map[member_name]
      self.member_count -= 1
      return "SUCCESS"
    else:
      return "FAILURE"

  def process_command(self, command, command_data):
    """
    process command
    :param command: command to execute <str>
    :param command_data: command data <list>
    :return: output_msg <str>
    """
    if command == "MOVE_IN":
      return self.move_in_command(command_data)
    elif command == "SPEND":
      return self.spend_command(command_data)
    elif command == "DUES":
      return self.dues_command(command_data)
    elif command == "CLEAR_DUE":
      return self.clear_due_command(command_data)
    elif command == "MOVE_OUT":
      return self.move_out_command(command_data)
    else:
      return "COMMAND NOT FOUND"