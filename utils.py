from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QPushButton, QLineEdit

class Utils(QObject):
    FREEZE_GUI = pyqtSignal(list, list)
    UNFREEZE_GUI = pyqtSignal()
    
    def __init__(self, Video_combiner_object) -> None:
        self.VideoCombinerObject = Video_combiner_object

    def Update_Processing_Folder(self) -> None:
        pass

    def Check_AnyRemaining_Folder(self, i_TotalFolders: int, i_CurrentFolder: int) -> None:
        if i_CurrentFolder <= i_TotalFolders:
            pass
        else:
            pass
        
    def next_merge(self) -> None:
        print("Called")
        self.VideoCombinerObject.CurrentFolderIndex += 1
        if (self.VideoCombinerObject.TotalFolders > self.VideoCombinerObject.CurrentFolderIndex):
            self.VideoCombinerObject.Current_Merge_Setup()
            self.VideoCombinerObject.combineVideos()
        else:
            print("Finished all merges done")

    def Reset_Gui(self, action_btns: list[QPushButton], input_fields: list[QLineEdit]) -> None:
        for action_btn in action_btns:
            action_btn.setEnabled(True)
            
        for input_field in input_fields:
            input_field.setEnabled(True)
            

    def Freeze_Gui(self, action_btns: list[QPushButton], input_fields: list[QLineEdit]) -> None:
        for action_btn in action_btns:
            action_btn.setEnabled(False)
            
        for input_field in input_fields:
            input_field.setEnabled(False)