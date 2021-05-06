import os
import subprocess
import ctypes
import time

from PyQt5 import uic
from PyQt5 import QtCore

from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic.properties import DEBUG

form_class = uic.loadUiType("ui/window.ui")[0]

"""
mainwindow
	__init__ : 코드 시작 부분
	startsetting : 시작에 필요한 작업
	ui_action_ready : ui와 코드를 연결 시킴
	ui_lock : 작업 실행하면 UI 잠금
	ui_unlock : 작업 종료하면 UI 잠금 해제
	third_load : 영상 불러오기
	third_export : 영상 프레임으로 내보내기
	fourth_load : 프레임 불러오기
	fourth_export : 프레임 영상으로 내보내기
	createFolder : 폴더 생성하기
	set_text : 레이블에 텍스트 씌우기
	thread_end : 쓰레드 종료되면 실행

Thread3 : 파일 영상에서 프레임으로 만들어 주는 쓰레드
	__init__ : 코드 시작 부분
	run : 작동

Thread4 : 파일 영상에서 프레임으로 만들어 주는 쓰레드
	__init__ : 코드 시작 부분
	run : 작동
"""

class mainwindow(QMainWindow, form_class):
    def __init__(self):
        super(mainwindow, self).__init__()

        if subprocess.getstatusoutput("ffmpeg -version")[0] == 0:
            self.setupUi(self)
            self.setFixedSize(413, 481)
            self.show()
            self.startsetting()
            self.ui_action_ready()
        else:
            ctypes.windll.user32.MessageBoxW(0, "ffmpeg를 설치해주세요.", "에러", 0)
            exit()

    def startsetting(self):
        # 파일 종합 경로
        self.video_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.frame_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.third_export_btn.setEnabled(False)
        self.first_check_num = 0
        self.first_check_change()
        self.set_text("대기중")

    def ui_action_ready(self):
        # 1번 탭
        self.first_load_btn.clicked.connect(self.video_load)
        self.first_export_btn.clicked.connect(self.first_export)
        self.res_change_checkBox.stateChanged.connect(self.first_check_change)

        # 2번 탭

        # 3번 탭
        self.third_load_btn.clicked.connect(self.video_load)
        self.third_export_btn.clicked.connect(self.third_export)

        # 4번 탭
        self.fourth_load_btn.clicked.connect(self.fourth_load)
        self.fourth_export_btn.clicked.connect(self.fourth_export)

        # self.info_btn.clicked.connect(self.info)

    def video_load(self):
        """
            영상 불러오기
        """
        # 필터를 이용하여 정해진 확장자만 선택이 가능하다.
        select_filter = "Image(*.mp4 *.mpg *.mkv)"
        self.video_file_path = QFileDialog.getOpenFileName(None, "파일 선택창", self.video_file_path, select_filter)[0]

        # 비디오 경로
        self.video_path = ""
        # 비디오 이름
        self.video_name = ""
        # 비디오 확장자
        self.video_exp = ""

        if self.video_file_path:
            # 영상 경로 
            self.video_path = os.path.split(self.video_file_path)[0]
            # 영상 이름
            self.video_name = os.path.splitext(os.path.basename(self.video_file_path))[0]
            # 영상 확장자
            self.video_exp = os.path.splitext(self.video_file_path)[-1]
            
            # 이름 저장들
            self.name_lbl_2.setText(self.video_name)
            self.name_lbl.setText(self.video_name)

    def first_export(self):
        try:
            self.ui_lock()
            self.set_text("작업 시작")
            # 폴더 생성
            self.createFolder(self.video_path, self.video_name + "_클립")
            ss = f"{self.h_1_linedit.text()}:{self.m_1_linedit.text()}:{self.s_1_linedit.text()}"
            to = f"{self.h_2_linedit.text()}:{self.m_2_linedit.text()}:{self.s_2_linedit.text()}"
            save_path = os.path.join(self.video_path, self.video_name + "_클립")

            # 탭 1 기능 쓰레드
            self.thread1 = Thread1(self.first_check_num, ss, to, self.res_x_linedit.text(), self.res_y_linedit.text(), self.video_path, self.video_name, self.video_exp, save_path)

            # 피니쉬 신호 받기
            self.thread1.msg_sig.connect(self.set_text)
            self.thread1.end_sig.connect(self.thread_end)
            
            # 스타트
            self.thread1.start()
        
        except:
            self.ui_unlock()
            self.set_text("비디오 나누기 실패")
            
    def first_check_change(self):
        if self.first_check_num == 0:
            self.res_x_linedit.setDisabled(True)
            self.res_y_linedit.setDisabled(True)
            self.first_check_num = 1 
        elif self.first_check_num == 1:
            self.res_x_linedit.setEnabled(True)
            self.res_y_linedit.setEnabled(True)
            self.first_check_num = 0

    def ui_lock(self):
        # 1번 탭
        self.first_load_btn.setDisabled(True)
        self.first_export_btn.setDisabled(True)

        self.h_1_linedit.setDisabled(True)
        self.m_1_linedit.setDisabled(True)
        self.s_1_linedit.setDisabled(True)

        self.h_2_linedit.setDisabled(True)
        self.m_2_linedit.setDisabled(True)
        self.s_2_linedit.setDisabled(True)

        self.res_change_checkBox.setDisabled(True)
        self.res_x_linedit.setDisabled(True)
        self.res_y_linedit.setDisabled(True)

        # 2번 탭

        # 3번 탭
        self.save_img_exp_linedeit.setDisabled(True)
        self.third_load_btn.setDisabled(True)
        self.third_export_btn.setDisabled(True)

        # 4번 탭
        self.frame_lineedit.setDisabled(True)
        self.load_img_exp_linedeit.setDisabled(True)

        self.fourth_load_btn.setDisabled(True)
        self.fourth_export_btn.setDisabled(True)

    def ui_unlock(self):
        # 1번 탭
        self.first_load_btn.setEnabled(True)
        self.first_export_btn.setEnabled(True)

        self.h_1_linedit.setEnabled(True)
        self.m_1_linedit.setEnabled(True)
        self.s_1_linedit.setEnabled(True)

        self.h_2_linedit.setEnabled(True)
        self.m_2_linedit.setEnabled(True)
        self.s_2_linedit.setEnabled(True)

        self.res_change_checkBox.setEnabled(True)

        if self.first_check_num == 1:
            self.res_x_linedit.setDisabled(True)
            self.res_y_linedit.setDisabled(True)
        elif self.first_check_num == 0:
            self.res_x_linedit.setEnabled(True)
            self.res_y_linedit.setEnabled(True)

        # 2번 탭

        # 3번 탭
        self.save_img_exp_linedeit.setEnabled(True)
        self.third_load_btn.setEnabled(True)
        self.third_export_btn.setEnabled(True)

        # 4번 탭
        self.frame_lineedit.setEnabled(True)
        self.load_img_exp_linedeit.setEnabled(True)

        self.fourth_load_btn.setEnabled(True)
        self.fourth_export_btn.setEnabled(True)

    def third_export(self):
        try:
            self.ui_lock()
            self.set_text("작업 시작")
            # 폴더 생성
            self.createFolder(self.video_path, self.video_name.split(".")[0].replace(" ", "_") + "_split")
            # 스플릿 시작
            self.thread3 = Thread3(self.video_file_path, self.folder, self.video_name.split(".")[0].replace(" ", "_"), self.save_img_exp_linedeit.text())
            # 피니쉬 신호 받기
            self.thread3.msg_sig.connect(self.set_text)
            self.thread3.end_sig.connect(self.thread_end)
            # 스타트
            self.thread3.start()
        except:
            self.ui_unlock()
            self.set_text("비디오 나누기 실패")

    def fourth_load(self):
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

    def fourth_export(self):
        try:
            self.ui_lock()
            self.createFolder(self.frame_file_path, "합친영상")
            frame = float(self.frame_lineedit.text())
            self.thread4 = Thread4(frame, self.frame_file_path, self.media_name, self.load_img_exp_linedeit.text())
            # 피니쉬 신호 받기
            self.thread4.msg_sig.connect(self.set_text)
            self.thread4.end_sig.connect(self.thread_end)
            # 스타트
            self.thread4.start()
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

class Thread1(QThread):
    # 사용자 정의 시그널 선언
    msg_sig = QtCore.pyqtSignal(str)
    end_sig = QtCore.pyqtSignal(int)
    def __init__(self, first_check_num, ss, to, res_x, res_y, video_path, video_name, video_exp, save_path, debug: bool=False):
        QThread.__init__(self)
        self.first_check_num = first_check_num
        self.ss = ss
        self.to = to
        self.res_x = res_x
        self.res_y = res_y
        self.video_path = video_path
        self.video_name = video_name
        self.video_exp = video_exp
        self.save_path = save_path
        self.debug = debug

    def run(self):
        self.msg_sig.emit("영상 구간 나누기 진행중")
        print("영상 나누기")
        if self.first_check_num == 1:
            print(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name, self.video_exp)}\" -c:v libx264 -crf 1 \"{os.path.join(self.save_path, self.video_name + "_클립", self.video_exp)}\"')
            result = subprocess.Popen(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" -c:v libx264 -crf 1 \"{os.path.join(self.save_path, self.video_name + "_클립" + self.video_exp)}\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
        elif self.first_check_num == 0:
            print(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" -vf \"scale={self.res_x}x{self.res_y}\" -c:v libx264 -crf 1 \"{os.path.join(self.save_path, self.video_name + "_클립" + self.video_exp)}\"')
            result = subprocess.Popen(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" -vf \"scale={self.res_x}x{self.res_y}\" -c:v libx264 -crf 1 \"{os.path.join(self.save_path, self.video_name + "_클립" + self.video_exp)}\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )

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

class Thread3(QThread):
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

class Thread4(QThread):
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
