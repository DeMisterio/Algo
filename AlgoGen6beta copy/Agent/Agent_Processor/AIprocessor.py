import openai
import os
import sys
'''gpt-5-mini-2025-08-07'''
class analyser():
    def __init__(self, signal='', MAINinstruction='instruction.txt', EXTRAinstruction='', ProjectStruct = '', ProjectData = '', ProjectModel=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))  # путь до AIprocessor.py
        path = os.path.join(script_dir, MAINinstruction)

        if os.path.exists(path):
            with open(path, 'r') as instruction:
                self.MAINinstruction = instruction.read()
        self.EXTRAinstruction = EXTRAinstruction 
        self.signal = signal
        self.ProjectModel = ProjectModel
        self.ProjectStruct = ProjectStruct
        self.ProjectData = ProjectData
    def read_unswer(self, EXTRAinstruction, signal, ProjectModel):
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model=ProjectModel,
            messages=[
                {"role": "system", "content": str(EXTRAinstruction)},
                {"role": "user", "content": str(signal)},
            ]
        )

        return response["choices"][0]["message"]["content"]

class Project(analyser):
    def __init__(self, MAINinstruction='instruction.txt', ProjectData=None):
        super().__init__(MAINinstruction)
        self.ProjectData = ProjectData
    def construct_the_order(self):
        print("Order_Making_Has_Started")
        order = self.read_unswer(
        'from following instruction, make the order of the actions, from the options available below (you dont have to use all of them, only those ones which are listed in the instrution). You must include option Change only once in your order, and please, try to use other options maximum 2 times. YOU DONT HAVE TO USE EVERY OPTION!:'
        '1)Read: (what to read)'
        '2)Notify: (what to notify about)'
        '3)Change: (what to change)'
        '4)Detect: (what to detect)'
        '5)Confirmation: (if user needs to confirm the changes if they are massive)'
        '6)Remove: (what to remove)'
        '7)Summorize: (what to remove)' 
        '8)Change: (what to change)'
        '9)Colclude: (all of the changes made)', self.MAINinstruction,'gpt-4.1-mini-2025-04-14' 
                                )
        print(order)
        return order
    def order_follower(self, ProjectData):
        order = self.construct_the_order()
        print("Order_Following_Has_Started")
        refabrished_project_material = self.read_unswer(
            f"You are the agent of the project, and you will now have to use this instruction below: "
            f"with the project data in order to process. here is how: "
            f'1 - read the order of tasks (instruction) carefully. all of them refer to the project, and you need to operate with this'
            f'project. Your output should include this actions from the order: '
            f'1) Notify: if there is notify option, you will have to make the notification based on what you had to notify about in this instruction. Make really small notifications, maximum 10 words lengh.'
            f'2) Confirmation: if the project changes are massive, you can ask for users confirmation. In this field, you can specify, that user must confirm the changes as they are massive'
            f'2) Change: the instruction will not necesseraly include this option, and you will have to apply those changes, or improvements, which are listed in the instruction below. The projects you make shall include minimum comments in code, try to make a lot of code. '
            f'3) Conclude: if there is conclude option, you will have to make the conclusion about what you have changed in the project.'
            f'Other actions, if they are included in the list, are only for you to perform them on the project.'
            f'While making the changes in the projects data, you must not change the form of how are the files and directories listed,'
            f'but you can add an extra files with the needed code, if you think this will better for the changes. You can also modify and expand the code that will be in this data while making the changes.'
            f'if you see the use of certain files in the code, such us txt files, (f.e: readme text files) you can also modify them if you think this will be needed for the project.'
            f'if you see the files included in the code, which are not the text, (f.e: images, videos, sounds), notice - they are unsupported for making any changes in them, but you can include these files in the project. Just use the name of this file which you will be provided with.'
            f'Overall, your output shall be looking like this: ((command) is separator before the action you will need to use)'
            f'(command)Notify: (f.e: You have the errors in these lines of codes in your project, this make the project vulnarable...)'
            f'(command)Confirmation: (f.e: Please confirm the changes made in New version of your project!)'
            f'(command)Changes:'
            f'(output the full project you have improved with all the code (or not, if not stated in instrution)(You must start from the new line))'
            f'(command))Conclude:(f.e: New version serves the improvements in logic...)',
             order + ProjectData, 'gpt-5-mini-2025-08-07'        
              )
        print("Order_Following_Has_Finished") 
        return refabrished_project_material



