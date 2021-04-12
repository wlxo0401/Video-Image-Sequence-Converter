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

    def startsetting(self):
        # 파일 종합 경로
        self.file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        
        # 불러오기 버튼
        self.load_btn.clicked.connect(self.video_load)
        # 내보내기 버튼
        self.export_btn.clicked.connect(self.video_export)
        self.export_btn.setEnabled(False)
        self.setStext("대기중")

    def video_load(self):
        """
            영상 불러오기
        """
        # 필터를 이용하여 정해진 확장자만 선택이 가능하다.
        select_filter = "Image(*.mp4)"
        self.file_path = QFileDialog.getOpenFileName(None, "파일 선택창", self.file_path, select_filter)[0]
        # 비디오 이름
        self.video_name = ""
        # 비디오 경로
        self.video_path = ""
        if self.file_path:
            # 이미지 리스트에 사진 경로 담기
            self.video_name = self.file_path.split("/")[-1]
            self.name_lbl.setText(self.video_name)
            temp = self.file_path.split("/")
            del temp[-1]
            for i in temp:
                self.video_path += i + "/"
            self.setStext("비디오 불러오기 완료")
            self.export_btn.setEnabled(True)


    def video_export(self):
        self.setStext("작업 시작")
        self.load_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        # 폴더 생성
        self.createFolder(self.video_path, self.video_name.split(".")[0] + "_split")
        # 스플릿 시작
        self.thread = Thread(self.file_path, self.folder, self.video_name.split(".")[0])
        # 피니쉬 신호 받기
        self.thread.msg_sig.connect(self.setStext)
        self.thread.end_sig.connect(self.eenndd)
        # 스타트
        self.thread.start()


    def createFolder(self, folder_path, folder_name):
        # 폴더 경로, 이름.  한번에 다받아서 진행해도됨
        self.folder = os.path.join(folder_path, folder_name)
        # 폴더 유무 확인하고 생성
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            self.setStext("폴더 생성 완료")
        else:
            self.setStext("폴더가 이미 존재합니다.")
            return "FILE_ALREADY"

    def setStext(self, msg):
        self.status_lbl.setText(msg)

    def eenndd(self):
        self.load_btn.setEnabled(True)
        self.export_btn.setEnabled(True)

# 이름 변경용 쓰레드        
class Thread(QThread):
    """ 파일 저장용 스레드 """
    # 사용자 정의 시그널 선언
    msg_sig = QtCore.pyqtSignal(str)
    end_sig = QtCore.pyqtSignal(int)
    def __init__(self, target_video, save_folder_path, media_name, debug: bool=False):
        QThread.__init__(self)

        self.target_video = target_video
        self.save_folder_path = save_folder_path
        self.media_name = media_name
        self.debug = debug

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
        result = subprocess.Popen(f'ffmpeg -i \"{self.target_video}\" \"{self.save_folder_path}/{self.media_name}_%05d.png\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )

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

        

