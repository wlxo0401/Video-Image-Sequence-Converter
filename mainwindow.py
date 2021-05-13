import os
import subprocess
import ctypes
import cv2
import webbrowser

from moviepy.editor import VideoFileClip

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
    startsetting : 시작에 필요한 기타 작업
    ui_action_ready : ui와 코드를 연결 시킴
    first_check_change : 해상도를 변경할지 말지 탭 1 기능
    ui_lock : 작업시 ui 잠금
    ui_unlock : 작업 완료시 ui 잠금 해제
    createFolder : 폴더 생성용 함수
    set_text : ui에 상황 알려주기 위한 함수
    thread_end : 쓰레드 끝나면 작동 공용 함수
    video_load : 탭1, 3에서 사용하는 비디오 로드 함수
    first_export : 탭1 작업 시작 함수
    third_export : 탭3 작업 시작 함수
    fourth_load : 탭4 프레임 로드 함수
    fourth_export : 탭4 프레임 영상화 시작 함수

Thread1 : 영상을 구간으로 나누는 쓰레드
    __init__ : 코드 시작 부분
    run : 작동 

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
            webbrowser.open('https://m.blog.naver.com/chandong83/222095346417')
            
            exit()

    def startsetting(self):
        # 파일 종합 경로
        self.video_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        self.frame_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
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

    def get_duration(self, filename):
        clip = VideoFileClip(filename)
        return clip.duration

    def SecondsConvertor(self, duration):
        print(duration)
        day = int(duration / 86400)  #The int call removes the decimals.  Conveniently, it always rounds down.  int(2.9) returns 2 instead of 3, for example.
        duration -= (day * 86400)  #This updates the value of x to show that the already counted seconds won't be double counted or anything.
        hours = int(duration / 3600)
        duration -= (hours * 3600)
        minutes = int(duration / 60)
        duration -= (minutes * 60)
        seconds = int(duration)
        return day, hours, minutes, seconds

    def video_info(self, infilename):
    
        cap = cv2.VideoCapture(infilename)
    
        if not cap.isOpened():
            print("could not open :", infilename)
            exit(0)
    
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        print('length : ', length)
        print('width : ', width)
        print('height : ', height)
        return width, height

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
            # 영상 시간
            _, self.duration_hour, self.duration_min, self.duration_sec = self.SecondsConvertor(self.get_duration(self.video_file_path))
            # 영상 해상도
            res_x, res_y = self.video_info(self.video_file_path)

            # 이름 표현들
            self.name_lbl_2.setText(self.video_name)
            self.name_lbl.setText(self.video_name)
            # 시간 표현
            self.h_2_linedit.setText(str(self.duration_hour).zfill(2))
            self.m_2_linedit.setText(str(self.duration_min).zfill(2))
            self.s_2_linedit.setText(str(self.duration_sec).zfill(2))
            # 해상도 저장
            self.res_x_linedit.setText(str(res_x))
            self.res_y_linedit.setText(str(res_y))

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

    def third_export(self):
        try:
            self.ui_lock()
            self.set_text("작업 시작")
            # 폴더 생성
            self.createFolder(self.video_path, self.video_name + "_split")
            save_path = os.path.join(self.video_path, self.video_name + "_split")
            # 스플릿 시작
            self.thread3 = Thread3(self.video_path, self.video_name, self.video_exp, save_path, self.save_img_exp_linedeit.text())
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
            
            self.frame_name = os.path.splitext(self.frame_list[0])[0][:-9]
            
            print(self.frame_name)
            self.frame_count_lbl.setText(str(len(self.frame_list)))

    def fourth_export(self):
        try:
            self.ui_lock()
            self.createFolder(self.frame_file_path, "합친영상")
            frame = float(self.frame_lineedit.text())
            self.thread4 = Thread4(frame, self.frame_file_path, self.frame_name, self.load_img_exp_linedeit.text())
            # 피니쉬 신호 받기
            self.thread4.msg_sig.connect(self.set_text)
            self.thread4.end_sig.connect(self.thread_end)
            # 스타트
            self.thread4.start()
        except:
            self.ui_unlock()
            self.set_text("프레임 합치기 실패")

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
        svp = os.path.join(self.save_path, self.video_name + "_클립" + self.video_exp)
        if os.path.isfile(svp):
            print("파일있음")
            os.remove(svp)
        else:
            print("파일없음")
        if self.first_check_num == 1:
            print(self.ss)
            print(self.to)
            print(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" -c:v libx264 -crf 1 \"{svp}\"')
            result = subprocess.Popen(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" -c:v libx264 -crf 1 \"{svp}\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
        elif self.first_check_num == 0:
            result = subprocess.Popen(f'ffmpeg -ss {self.ss} -to {self.to} -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" -vf \"scale={self.res_x}x{self.res_y}\" -c:v libx264 -crf 1 \"{svp}\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )

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

    def __init__(self, video_path, video_name, video_exp, save_path, image_exp, debug: bool=False):
        QThread.__init__(self)
        self.video_path = video_path
        self.video_name = video_name
        self.video_exp = video_exp
        self.save_path = save_path
        self.image_exp = image_exp
        self.debug = debug

    # QThread 수행 메소드
    def run(self):
        """
        """
        # 서브 프로세서를 통해서 이미지를 추출합니다.
        self.msg_sig.emit("영상 나누기 진행중")
        result = subprocess.Popen(f'ffmpeg -i \"{os.path.join(self.video_path, self.video_name + self.video_exp)}\" \"{self.save_path}/{self.video_name}_%08d.{self.image_exp}\"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )

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

    def __init__(self, fps, frame_path, frame_name, exp, debug=False):
        QThread.__init__(self)
        self.fps = fps
        self.frame_path = os.path.join(frame_path, frame_name)
        self.save_path = os.path.join(frame_path, "합친영상", frame_name + ".mp4")
        self.debug = debug
        self.exp = exp

    def run(self):
        """
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
