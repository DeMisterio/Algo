import re
import subprocess
from kernel_communicator import Communicator
from parser import Parser
from AIprocessor import analyser
import pync
from AIprocessor import Project
from applier import ProjectBuilder
from back_up_engine import BackUper
class Coordinator:
    def __init__(self, impulse='', signal='', signal_location='', Programmcommunicator=None, ProgrammParser=None, ProgrammBackUpper=None, ProgrammThinker=None, ProjectApplier=None):
        self.impulse = impulse
        self.signal = signal
        self.signal_location = signal_location
        self.ProgrammThinker = ProgrammThinker or analyser()
        self.ProjectApplier = ProjectApplier or ProjectBuilder()
        self.Programm_BackUpper = ProgrammBackUpper or BackUper()
        self.Programmcommunicator = Programmcommunicator or Communicator()
        self.ProgrammParser = ProgrammParser or Parser()
        # словарь обработчиков сигналов
        self.signal_patch = {
            'No project': lambda: self.Programmcommunicator.send_signal('NoFiles'),
            "Could not initialize": lambda: self.Programmcommunicator.send_signal('CouldNotInit'),
            'User confirmation needed': lambda: self.ask_mac('Please confirm changes made by the agent'),
            'Error occured': lambda: self.Programmcommunicator.send_signal('EO')
        }
        self.action_patch = {
            'Notify': lambda text: self.notify(text),
            'Confirmation': lambda confirmation: self.ask_mac(confirmation),
            'Changes': lambda data: self.ProjectApplier.build_from_template(data),
            'Colclude': lambda conclusion: self.Programm_BackUpper.set_a_conclusion(conclusion)
        }
    def notify(self,text):
        pync.notify(text, title="Your Agent")
    def ask_mac(self, message: str) -> bool | None:
        """Нативное macOS окно подтверждения через AppleScript"""
        script = f'display dialog "{message}" with title "Confirmation" buttons {{"Cancel", "OK"}} default button "OK"'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if "OK" in result.stdout:
            return True
        elif "Cancel" in result.stdout:
            return False
        return None

    def solution_solver(self, impulse: str):
        """Запускает нужный обработчик по ключу"""
        action = self.signal_patch.get(impulse)
        if action:
            return action()
        return None

    def signal_analyser(self, signal_location: str, signal: str):
        """Анализирует сигнал и решает, что делать"""
        if signal_location == "kernel_communicator":
            response = self.ProgrammThinker.read_unswer(
                "Identify, whether following prompt asks to: "
                "1) Change agent's function "
                "2) Get reports and stats about processing "
                "3) Stop agent working "
                "4) Check whether the agent is still working. "
                "If identified, reply 'CP' if first, 'GRAT' if second, "
                "'SA' if third, 'AS' if fourth, else 'NE'.",
                signal, "gpt-4.1-mini-2025-04-14"
            )
            if response == 'CP':
                pass
            elif response == "GRAT":
                pass
            elif response == "SA":
                pass
            elif response == 'AS':
                pass
            elif response == 'NE':
                self.Programmcommunicator.send_signal("Sorry, I did not understand what you mean :)")

        elif signal_location == "parser":
            self.solution_solver(signal)
    def ordinator(self):
        #Firstly, we parse all the data:
        Struct = self.ProgrammParser.parseStruct()
        Data = self.ProgrammParser.parseData()
        self.Programm_BackUpper.BackUpData()
        Project_management = Project()
        List_of_results = Project_management.order_follower(Data)
        parts = List_of_results.split("(command)")
        result_dict = {}
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Берем первое слово до двоеточия как ключ
            if ":" in part:
                key, value = part.split(":", 1)
                key = key.strip()
                value = value.strip()
            else:
                key = part
                value = ""
            result_dict[key] = value
        print(result_dict)
        for action, text in result_dict.items():
            function = self.action_patch.get(action)  # используем .get() для безопасного доступа
            print(action, ' has started!')
            if function:
                result = function(text)
                if action == "Confirmation":
                    if result == True:
                        pass
                    else:
                        return 'Changes Declined'
        return 'Completed'

        
    
if __name__ == "__main__":
    start = Coordinator()
    start.ordinator()






