import sys
import os
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# from TextVideo import AddTextVideo
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QListWidget, QProgressBar, QAbstractItemView, QFileSystemModel, QTreeView 
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from MergeVideos import merge_videos
from utils import Utils

class VideoProcessor(QObject):
    finished = pyqtSignal()
    progressChanged = pyqtSignal(int)

    def __init__(self, video_files, output_folder, output_file, btns):
        super().__init__()
        self.video_files = video_files
        self.output_folder = output_folder
        self.output_file = output_file
        self.bns = btns

    def run(self):
        merge_videos(video_files=self.video_files, output_path=self.output_folder, output_filename=self.output_file)
        for btn in self.bns:
            btn.setEnabled(True)
        self.finished.emit()


class VideoCombinerApp(QWidget):
    Show_Video_list = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()
        self.SelectFolders = None
        self.TotalFolders = None
        self.CurrentFolderIndex = None
        self.DefaultOutputName = None
        self.Show_Video_list.connect(self.loadVideoNamesAndTimings)
        self.utility = Utils(self)
        # self.utility.next_merge()
        
        # self.Show_Video_list.connect(self.loadVideoNamesAndTimings)
        
        self.video_Processing_thread = QThread()
        # u.Reset_Gui()

    def initUI(self):
        self.setWindowTitle('Video Combiner')
        self.setGeometry(100, 100, 600, 200)

        self.selected_folder_path = None
        self.out_select_folder_path = None
        self.out_file_name = None
        self.video_files = None
        self.btns = []
        self.input_fields = []
        
        #UI Elements Defined
        self.lbl_folder_path = QLabel("Videos Path:", self)
        self.input_folder_path = QLineEdit(self)
        self.btn_select_folder = QPushButton('Select', self)
        
        self.lbl_out_folder_path = QLabel("Output Path:", self)
        self.input_out_folder_path = QLineEdit(self)
        self.btn_out_select_folder = QPushButton('Select', self)
        
        self.lbl_out_file_name = QLabel("Output File:", self)
        self.input_out_file_name = QLineEdit(self)

        self.video_list = QListWidget(self)

        self.btn_combine_videos = QPushButton('Combine Videos', self)
        
        self.progress_bar = QProgressBar(self)
        
        

        #Input files path
        self.btn_select_folder.clicked.connect(self.selectFolder)
        

        #Output file path
        self.btn_out_select_folder.clicked.connect(self.out_selectFolder)

        #Output file name
        self.btn_combine_videos.clicked.connect(self.combineVideos)


        self.btns.append(self.btn_select_folder)
        self.btns.append(self.btn_out_select_folder)
        self.btns.append(self.btn_combine_videos)
        
        self.input_fields.append(self.input_folder_path)
        self.input_fields.append(self.input_out_folder_path)
        self.input_fields.append(self.input_out_file_name)
        

        btn_layout_1 = QHBoxLayout()
        btn_layout_1.addWidget(self.lbl_folder_path)
        btn_layout_1.addWidget(self.input_folder_path)
        btn_layout_1.addWidget(self.btn_select_folder)
        
        btn_layout_2 = QHBoxLayout()
        btn_layout_2.addWidget(self.lbl_out_folder_path)
        btn_layout_2.addWidget(self.input_out_folder_path)
        btn_layout_2.addWidget(self.btn_out_select_folder)

        btn_layout_3 = QHBoxLayout()
        btn_layout_3.addWidget(self.lbl_out_file_name)
        btn_layout_3.addWidget(self.input_out_file_name)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout_1)
        main_layout.addLayout(btn_layout_2)
        main_layout.addLayout(btn_layout_3)

        main_layout.addWidget(self.video_list)

        main_layout.addWidget(self.btn_combine_videos)

        main_layout.addWidget(self.progress_bar)


        self.setLayout(main_layout)

    def selectFolder(self):

        if self.isProcessing():
            return
        
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)
        folder_dialog.setOption(QFileDialog.DontUseNativeDialog, True)  # Disable native folder_dialog for customization

        for view in folder_dialog.findChildren((QListWidget, QTreeView)):
            if isinstance(view.model(), QFileSystemModel):
                view.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Allow multi-selection

        if folder_dialog.exec_():
            self.SelectFolders = folder_dialog.selectedFiles()
            self.TotalFolders = len(folder_dialog.selectedFiles())
            self.CurrentFolderIndex = 0
            print("Total Folder : ",self.TotalFolders)
            # selected_folder = folder_dialog.selectedFiles()
            if self.SelectFolders:
                self.Current_Merge_Setup()
                # self.selected_folder_path = self.SelectFolders[self.CurrentFolderIndex]
                # self.input_folder_path.setText(self.selected_folder_path)
                # self.DefaultOutputName = os.path.basename(self.selected_folder_path)
                # self.Show_Video_list.emit()
                # self.loadVideoNamesAndTimings()
                
    def Current_Merge_Setup(self):
        self.selected_folder_path = self.SelectFolders[self.CurrentFolderIndex]
        self.input_folder_path.setText(self.selected_folder_path)
        self.DefaultOutputName = os.path.basename(self.selected_folder_path)
        self.Show_Video_list.emit()
    
    def out_selectFolder(self):
        if self.isProcessing():
            return
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)
        folder_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        if folder_dialog.exec_():
            selected_folder = folder_dialog.selectedFiles()
            if selected_folder:
                self.out_selected_folder_path = selected_folder[0]
                self.input_out_folder_path.setText(self.out_selected_folder_path)


    def loadVideoNamesAndTimings(self):
        if self.isProcessing():
            return
        self.video_list.clear()

        if not self.selected_folder_path:
            return

        self.video_files = [f for f in os.listdir(self.selected_folder_path) if f.endswith((".mp4", ".avi", ".mkv"))]

        for video_file in self.video_files:
            self.video_list.addItem(f"{video_file}")


    def combineVideos(self):
        if not self.selected_folder_path:
            return
        
        print("Combined_Called")
        print("Current FOlder index: ", self.CurrentFolderIndex)
        
        # for btn in self.btns:
        #     btn.setEnabled(False)
        self.utility.Freeze_Gui(self.btns, self.input_fields)


        video_files = [os.path.join(self.selected_folder_path,v) for v in self.video_files]

        output_file = self.out_selected_folder_path+"/"
        self.out_file_name = self.input_out_file_name.text()
        # print(output_file)

        # thread = QThread()
        self.videoProcessor = VideoProcessor(video_files, output_file, self.DefaultOutputName, self.btns)
        self.videoProcessor.moveToThread(self.video_Processing_thread)
        
        self.video_Processing_thread.started.connect(self.videoProcessor.run)
        # self.videoProcessor.started(self.utility.next_merge)
        
        self.videoProcessor.finished.connect(self.video_Processing_thread.quit)
        # self.video_Processing_thread.finished.connect(self.video_Processing_thread.deleteLater)
        self.videoProcessor.finished.connect(lambda: self.utility.Reset_Gui(self.btns, self.input_fields))
        self.videoProcessor.finished.connect(lambda: self.utility.next_merge())
        # self.videoProcessor.finished.connect(lambda: self.utility.Check_AnyRemaining_Folder(self.TotalFolders, self.CurrentFolderIndex))
        
        self.video_Processing_thread.start()

    def updateProgress(self, progress):
        self.progress_bar.setValue(10)

    def isProcessing(self):
        return not self.btn_select_folder.isEnabled() or not self.btn_combine_videos.isEnabled()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_combiner_app = VideoCombinerApp()
    video_combiner_app.show()
    sys.exit(app.exec_())
