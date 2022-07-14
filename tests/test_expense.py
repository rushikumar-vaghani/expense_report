import unittest
from expense import Expense

class ExpenseTest(unittest.TestCase):

  def test_process_command_default(self):
    expense = Expense()
    output = expense.process_command("TEST", [])
    self.assertTrue(output == "COMMAND NOT FOUND")

  def test_move_in_wrong_param(self):
    expense = Expense()
    output = expense.process_command("MOVE_IN", [])
    self.assertTrue(output == "INVALID ARGUMENT PASS TO MOVE_IN COMMAND")

  def test_move_in_success(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

  def test_move_in_failure_already_member(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)

    # add member again and verify message
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER ALREADY MOVE_IN")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

  def test_move_in_houseful(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)
    command_list = ["MOVE_IN", "MIKE"]
    expense.process_command(command_list[0], command_list)
    command_list = ["MOVE_IN", "JOY"]
    expense.process_command(command_list[0], command_list)
    command_list = ["MOVE_IN", "BIN"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "HOUSEFUL")
    self.assertTrue(len(expense.name_to_model_map) == 3)
    self.assertTrue(expense.member_count == 3)

  def test_move_out_wrong_param(self):
    expense = Expense()
    output = expense.process_command("MOVE_OUT", [])
    self.assertTrue(output == "INVALID ARGUMENT PASS TO MOVE_OUT COMMAND")

  def test_move_out_not_member(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

    command_list = ["MOVE_OUT", "XYZ"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER_NOT_FOUND")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

  def test_move_out_success(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

    command_list = ["MOVE_OUT", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")
    self.assertTrue(len(expense.name_to_model_map) == 0)
    self.assertTrue(expense.member_count == 0)

  def test_move_out_failure(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

    expense.name_to_model_map["ANDY"]._total_due = 100

    command_list = ["MOVE_OUT", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "FAILURE")
    self.assertTrue(len(expense.name_to_model_map) == 1)
    self.assertTrue(expense.member_count == 1)

  def test_dues_failure(self):
    expense = Expense()

    # verify for invalid arguments
    command_list = ["DUES", "BIN", "100"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "INVALID ARGUMENT PASS TO DUES COMMAND")

    # verify for invalid member
    command_list = ["DUES", "BINTEST"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER_NOT_FOUND")

  def test_dues_success(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)

    command_list = ["MOVE_IN", "BO"]
    expense.process_command(command_list[0], command_list)

    command_list = ["MOVE_IN", "BIN"]
    expense.process_command(command_list[0], command_list)
    self.assertTrue(expense.member_count == 3)

    expense.name_to_model_map["ANDY"]._own["BO"] = 50
    expense.name_to_model_map["ANDY"]._own["BIN"] = 100

    # verify for invalid arguments
    command_list = ["DUES", "ANDY"]
    output = expense.process_command(command_list[0], command_list)
    expected_msg = "{} {}\n{} {}".format("BIN", 100, "BO", 50)
    self.assertTrue(output == expected_msg)

  def test_dues_clear_failure(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)

    # wrong param count
    command_list = ["CLEAR_DUE", "ANDY", "BO"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "INVALID ARGUMENT PASS TO CLEAR_DUE COMMAND")

    # wrong dues or lenter
    command_list = ["CLEAR_DUE", "AND", "BO", "100"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER_NOT_FOUND")

    command_list = ["CLEAR_DUE", "ANDY", "BON", "100"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER_NOT_FOUND")

  def test_dues_clear_grater_amount(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)

    command_list = ["MOVE_IN", "BO"]
    expense.process_command(command_list[0], command_list)
    self.assertTrue(expense.member_count == 2)

    expense.name_to_model_map["ANDY"]._total_own = 1000
    expense.name_to_model_map["BO"]._total_due = 1000

    command_list = ["CLEAR_DUE", "ANDY", "BO", "2000"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "INCORRECT_PAYMENT")

  def test_dues_clear_grater_success(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)

    command_list = ["MOVE_IN", "BO"]
    expense.process_command(command_list[0], command_list)
    self.assertTrue(expense.member_count == 2)

    expense.name_to_model_map["ANDY"]._total_own = 1000
    expense.name_to_model_map["BO"]._total_due = 1000
    expense.name_to_model_map["ANDY"]._own["BO"] = 1000
    expense.name_to_model_map["BO"]._due["ANDY"] = 1000

    command_list = ["CLEAR_DUE", "ANDY", "BO", "500"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == str(500))

  def test_spend_failure(self):
    expense = Expense()
    # wrong param count
    command_list = ["SPEND", "ANDY", "BO"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "INVALID ARGUMENT PASS TO SPEND COMMAND")

    # wrong dues or lenter
    command_list = ["SPEND", "3000", "ANDY", "BO"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER_NOT_FOUND")

    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)
    self.assertTrue(expense.member_count == 1)

    command_list = ["SPEND", "3000", "ANDY", "BON"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "MEMBER_NOT_FOUND")

  def test_spend_success(self):
    expense = Expense()
    command_list = ["MOVE_IN", "ANDY"]
    expense.process_command(command_list[0], command_list)

    command_list = ["MOVE_IN", "BIN"]
    expense.process_command(command_list[0], command_list)

    command_list = ["MOVE_IN", "JOY"]
    expense.process_command(command_list[0], command_list)
    self.assertTrue(expense.member_count == 3)

    command_list = ["SPEND", "3000", "ANDY", "BIN", "JOY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")
    self.assertTrue(expense.name_to_model_map["ANDY"]._total_due == 2000)
    self.assertTrue(expense.name_to_model_map["ANDY"]._due["BIN"] == 1000)
    self.assertTrue(expense.name_to_model_map["ANDY"]._due["JOY"] == 1000)
    self.assertTrue(expense.name_to_model_map["ANDY"]._total_own == 0)

    self.assertTrue(expense.name_to_model_map["BIN"]._own["ANDY"] == 1000)
    self.assertTrue(expense.name_to_model_map["BIN"]._total_own == 1000)
    self.assertTrue(expense.name_to_model_map["JOY"]._total_due == 0)

    self.assertTrue(expense.name_to_model_map["JOY"]._own["ANDY"] == 1000)
    self.assertTrue(expense.name_to_model_map["JOY"]._total_own == 1000)
    self.assertTrue(expense.name_to_model_map["JOY"]._total_due == 0)

    command_list = ["SPEND", "1000", "BIN", "JOY"]
    output = expense.process_command(command_list[0], command_list)
    self.assertTrue(output == "SUCCESS")

    self.assertTrue(expense.name_to_model_map["ANDY"]._total_due == 2000)
    self.assertTrue(expense.name_to_model_map["ANDY"]._due["BIN"] == 500)
    self.assertTrue(expense.name_to_model_map["ANDY"]._due["JOY"] == 1500)
    self.assertTrue(expense.name_to_model_map["ANDY"]._total_own == 0)

    self.assertTrue(expense.name_to_model_map["BIN"]._own["ANDY"] == 500)
    self.assertTrue(expense.name_to_model_map["BIN"]._total_own == 500)
    self.assertTrue(expense.name_to_model_map["JOY"]._total_due == 0)

    self.assertTrue(expense.name_to_model_map["JOY"]._own["ANDY"] == 1500)
    self.assertTrue(expense.name_to_model_map["JOY"]._total_own == 1500)
    self.assertTrue(expense.name_to_model_map["JOY"]._total_due == 0)

if __name__ == "__main__":
  unittest.main()