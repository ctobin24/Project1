from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    """
    A class representing the logic for the voting gui
    """

    def __init__(self):
        """
        Method that sets up the default logic for the voting gui
        """
        super().__init__()
        self.setupUi(self)

        #Connecting the push buttons
        self.submit_button.clicked.connect(lambda: self.submit())
        self.clear_button.clicked.connect(lambda: self.clear())
        self.results_button.clicked.connect(lambda: self.view_results())

    def submit(self) -> None:
        """
        Method that is called upon when the user presses the SUMBIT button in the voting gui, then saves users name, id_num, and vote to the csvfile
        :return:None
        """
        global vote
        try:

            #Getting name from the gui and checking if it is a valid input
            name = self.name_input.text().strip()
            try:
                if not name.isalpha():
                    raise TypeError
            except TypeError:
                self.message_label.setStyleSheet("color : red;")
                self.message_label.setText('Invalid input for Name')

            #Getting the id from the gui and checkin if it is a valid input
            id_num = self.id_input.text().strip()
            try:
                if not id_num.isdigit():
                    raise TypeError
            except TypeError:
                self.message_label.setStyleSheet("color : red;")
                self.message_label.setText('Invalid input for ID')

            #Checks the csvfile if the users id has already been added
            try:
                with open('results.csv', 'r') as csvfile:
                    content = csv.reader(csvfile, delimiter=',')
                    for line in content:
                        if line[1] == id_num:
                            raise ValueError
            except ValueError:
                self.message_label.setStyleSheet("color : red;")
                self.message_label.setText("Already voted")
            else:
                csvfile.close()
                #Writes and saves to the file
                with open('results.csv', 'a', newline='') as csvfile:
                    content = csv.writer(csvfile)
                    if self.candidate_button_group.checkedButton() is None:
                        self.message_label.setStyleSheet("color : red;")
                        self.message_label.setText("Select a candidate")
                        return
                    else:
                        vote = self.candidate_button_group.checkedButton().text()
                    content.writerow([name, id_num, vote])

                    csvfile.close()
            self.clear()
        #LA helped with this, and he added this try and except statement
        except Exception as e:
            import traceback
            traceback.print_exc()


    def clear(self) -> None:
        """
        Method that is called upn when the user presses the CLEAR button in the voting gui, then wipes all the input boxes to blank
        :return:None
        """
        self.name_input.clear()
        self.id_input.clear()
        self.candidate_button_group.setExclusive(False)
        self.felicia_button.setChecked(False)
        self.edward_button.setChecked(False)
        self.bianca_button.setChecked(False)
        self.candidate_button_group.setExclusive(True)

    def view_results(self) -> None:
        """
        Method that is called upon when the user presses the VIEW RESULTS button in the voting gui, then displays the results of the voting from everyone in the csvfile
        :return:None
        """
        results = []

        with open('results.csv', 'r') as csvfile:
            content = csv.reader(csvfile, delimiter=',')

            for line in content:
                results.append(line[2])

        self.results_textbox.setText(
            f'Bianca:{results.count('Bianca')}\nEdward:{results.count('Edward')}\nFelicia:{results.count('Felicia')}')
