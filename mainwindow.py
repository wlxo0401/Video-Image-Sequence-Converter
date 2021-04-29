import os
import subprocess

from PyQt5 import uic
from PyQt5 import QtCore

from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog

form_class = uic.loadUiType("ui/window.ui")[0]

class mainwindow(QMainWindow, form_class):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.show()
        self.startsetting()
        self.ui_action_ready()

    def startsetting(self):
        # 파일 종합 경로
        self.video_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.frame_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.export_btn.setEnabled(False)
        self.set_text("대기중")

    def ui_action_ready(self):
        # 불러오기 버튼
        self.load_btn.clicked.connect(self.video_load)
        # 내보내기 버튼
        self.export_btn.clicked.connect(self.video_export)

        # 내보내기 버튼
        self.frame_load_btn.clicked.connect(self.frame_load)
        # 내보내기 버튼
        self.frame_sum_btn.clicked.connect(self.frame_export)

        # self.info_btn.clicked.connect(self.info)

    def ui_lock(self):
        self.load_btn.setDisabled(True)
        self.export_btn.setDisabled(True)
        self.frame_load_btn.setDisabled(True)
        self.frame_sum_btn.setDisabled(True)
        self.save_img_exp_linedeit.setDisabled(True)
        self.frame_lineedit.setDisabled(True)
        self.load_img_exp_linedeit.setDisabled(True)

    def ui_unlock(self):
        self.load_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        self.frame_load_btn.setEnabled(True)
        self.frame_sum_btn.setEnabled(True)
        self.save_img_exp_linedeit.setEnabled(True)
        self.frame_lineedit.setEnabled(True)
        self.load_img_exp_linedeit.setEnabled(True)

    def video_load(self):
        """
            영상 불러오기
        """
        # 필터를 이용하여 정해진 확장자만 선택이 가능하다.
        select_filter = "Image(*.mp4 *.mpg *.mkv)"
        self.video_file_path = QFileDialog.getOpenFileName(None, "파일 선택창", self.video_file_path, select_filter)[0]
        # 비디오 이름
        self.video_name = ""
        # 비디오 경로
        self.video_path = ""
        if self.video_file_path:
            # 이미지 리스트에 사진 경로 담기
            self.video_name = self.video_file_path.split("/")[-1].replace(" ", "_")
            self.name_lbl.setText(self.video_name)
            temp = self.video_file_path.split("/")
            del temp[-1]
            for i in temp:
                self.video_path += i + "/"
            self.set_text("비디오 불러오기 완료")
            self.export_btn.setEnabled(True)

    def video_export(self):
        try:
            self.ui_lock()
            self.set_text("작업 시작")
            # 폴더 생성
            self.createFolder(self.video_path, self.video_name.split(".")[0].replace(" ", "_") + "_split")
            # 스플릿 시작
            self.thread = Thread(self.video_file_path, self.folder, self.video_name.split(".")[0].replace(" ", "_"), self.save_img_exp_linedeit.text())
            # 피니쉬 신호 받기
            self.thread.msg_sig.connect(self.set_text)
            self.thread.end_sig.connect(self.thread_end)
            # 스타트
            self.thread.start()
        except:
            self.ui_unlock()
            self.set_text("비디오 나누기 실패")

    def frame_load(self):
        # 필터를 이용하여 정해진 확장자만 선택이 가능하다.
        self.frame_file_path = QFileDialog.getExistingDirectory(None, "파일 선택창", self.frame_file_path)
        if self.frame_file_path:
            self.frame_list = list()
            if self.video_file_path:
                for file_name in os.listdir(self.frame_file_path):
                    self.frame_list.append(file_name)
            self.frame_name = self.frame_list[0].split("_")
            del self.frame_name[-1]
            self.media_name = ""
            for i in self.frame_name:
                self.media_name += "_" + i
            self.media_name = self.media_name[1:]
            print(self.media_name)
            self.frame_count_lbl.setText(str(len(self.frame_list)))

    def frame_export(self):
        try:
            self.ui_lock()
            self.createFolder(self.frame_file_path, "합친영상")
            frame = float(self.frame_lineedit.text())
            self.thread2 = Thread2(frame, self.frame_file_path, self.media_name, self.load_img_exp_linedeit.text())
            # 피니쉬 신호 받기
            self.thread2.msg_sig.connect(self.set_text)
            self.thread2.end_sig.connect(self.thread_end)
            # 스타트
            self.thread2.start()
        except:
            self.ui_unlock()
            self.set_text("프레임 합치기 실패")

    def createFolder(self, folder_path, folder_name):
        # 폴더 경로, 이름.  한번에 다받아서 진행해도됨
        self.folder = os.path.join(folder_path, folder_name)
        # 폴더 유무 확인하고 생성
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            self.set_text("폴더 생성 완료")
        else:
            self.set_text("폴더가 이미 존재합니다.")

    def set_text(self, msg):
        self.status_lbl.setText(msg)

    def thread_end(self):
        self.ui_unlock()

# 이름 변경용 쓰레드        
class Thread(QThread):
    # 사용자 정의 시그널 선언
    msg_sig = QtCore.pyqtSignal(str)
    end_sig = QtCore.pyqtSignal(int)
    def __init__(self, target_video, save_folder_path, media_name, exp, debug: bool=False):
        QThread.__init__(self)

        self.target_video = target_video
        self.save_folder_path = save_folder_path
        self.media_name = media_name
        self.debug = debug
        self.exp = exp

    # QThread 수행 메소드
    def run(self):
        """
            영상을 이미지로 만들어 줍니다.

            target_video :
                이미지로 만들 영상의 경로를 넣어줍니다.
            save_folder_path :
                이미지를 저장할 폴더의 경로를 넣어줍니다.
                경로를 넣어주지 않을 시 디폴트 경로인 파일 이름으로 폴더 생성 및 경로 설정 됩니다.
            debug :
                디버그 모드를 활성화 합니다.
                작업이 끝나거나 오류가 발생할 경우 서브 프로세스에 대한 출력을 가져옵니다.
        """
        # 서브 프로세서를 통해서 이미지를 추출합니다.
        self.msg_sig.emit("영상 나누기 진행중")
        result = subprocess.Popen(f'ffmpeg -i \"{self.target_video}\" \"{self.save_folder_path}/{self.media_name}_%08d.{self.exp}\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )

        if self.debug:
            out, err = result.communicate()
        else:
            result.communicate()

        exitcode = result.returncode

        if exitcode != 0:
            # 오류 발생 할 때 결과입니다.
            self.msg_sig.emit("영상 나누기 실패")
            self.end_sig.emit(1)
        else:
            # 정상 완료 될 때 결과입니다.
            self.msg_sig.emit("영상 나누기 완료")  
            self.end_sig.emit(0)

class Thread2(QThread):
    msg_sig = QtCore.pyqtSignal(str)
    end_sig = QtCore.pyqtSignal(int)

    def __init__(self, fps, frame_path, media_name, exp, debug=False):
        QThread.__init__(self)
        self.fps = fps
        self.frame_path = os.path.join(frame_path, media_name)
        self.save_path = os.path.join(frame_path, "합친영상", media_name + ".mp4")
        self.debug = debug
        self.exp = exp

    def run(self):
        """
        이미지를 영상으로 만들어 줍니다.

        frame_path :
        프레임을 영상으로 바꾸어 줍니다. 옵션들을 적용하느냐에 따라서 이미지를 불러오는 폴더는 변경이 됩니다.

        completed_folder :
        저장될 위치를 담을 변수입니다. 
        """

        self.msg_sig.emit("프레임 합치기 진행중")
        # 서브 프로세서를 통해서 이미지를 영상으로 만듭니다.
        result = subprocess.Popen(f'ffmpeg -y -f image2 -r {self.fps} -i \"{self.frame_path}_%08d.{self.exp}\" -vcodec libx264 \"{self.save_path}\"', stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        
        if self.debug:
            out, err = result.communicate()
        else:
            result.communicate()

        exitcode = result.returncode

        
        if exitcode != 0:
            # 오류 발생 할 때 결과입니다.
            self.msg_sig.emit("영상 합치기 실패")
            self.end_sig.emit(1)
        else:
            # 정상 완료 될 때 결과입니다.
            self.msg_sig.emit("영상 합치기 완료")  
            self.end_sig.emit(0)
