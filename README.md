# VISC(Video Image Sequence Converter)
# ver 1.0

# About 
>Python Open Source for cropping images into images or into sections

# Tech Stack
- Python
- pyqt
- Visual Studio Code
  
## Division of sections
The function of cutting the image into sections can create a short image. 
Export and resolution can be changed.

## Change the resolution   
Ability to convert image resolution. Lowering the resolution results in image quality degradation, and increasing the resolution only increases, but there is no improvement in image quality

## Split Frame
The ability to import images and frame them (images)
(The extension of the saved image must be entered in advance)
 
## Frame attachment
The ability to combine divided frames into images
(Frame must be entered in advance)
(Must enter an extension of the image to be imported in advance)
- 불러올 이미지의 확장자를 사전에 입력해주어야 함   
</br>

# 작업
```
2021-04-12 ~ 2021-04-12

1. UI 완성
2. UI와 기능 합치기 
3. 에러 잡기
4. 추가 기능 생각

문제점

ffmpeg가 설치 안된 컴퓨터에서는 동작하지 않음
``` 

![메인화면](https://github.com/wlxo0401/video_split/blob/main/readme_img/1.PNG) 

처음 실행 화면 모습

![파일 불러오기](https://github.com/wlxo0401/video_split/blob/main/readme_img/2.PNG) 

파일 선택 다이알로그

![파일 불러오기 완료](https://github.com/wlxo0401/video_split/blob/main/readme_img/3.PNG) 

불러오기 완료 모습

![나누기 시작](https://github.com/wlxo0401/video_split/blob/main/readme_img/4.PNG) 

나누기 시작

![나누기 완료](https://github.com/wlxo0401/video_split/blob/main/readme_img/5.PNG) 

나눈 결과물

<hr>

```
2021-04-16 ~ 2021-04-16

1. 프레임화된 영상을 다시 만들어주는 기능 예정
2. UI 변경
3. 프레임 폴더 선택 기능 추가

예정 
1. 불러온 프레임 수 확인
2. 해당 폴더에 영상 저장용 폴더 생성
3. 프레임 합치기

문제점

원본 영상이 없다고 가정하고 만들어서 합칠때 프레임을 
지정하기가 고민됨
``` 

![바뀐 UI1](https://github.com/wlxo0401/video_split/blob/main/readme_img/6.PNG) 

바뀐 UI 모습 탭1

![바뀐 UI2](https://github.com/wlxo0401/video_split/blob/main/readme_img/7.PNG) 

바뀐 UI 모습 탭2

<hr>

```
2021-04-29 ~ 2021-04-29

1. 불러온 프레임 수 확인
2. 해당 폴더에 영상 저자용 폴더 생성
3. 프레임 합치기
4. 프레임으로 만들때 확장자 지정
5. 불러올 프레임 확장자 지정
6. 프레임을 설정 가능하게

예정 

1. 영상 구간 자르기

```

![바뀐 UI1](https://github.com/wlxo0401/video_split/blob/main/readme_img/8.PNG) 

바뀐 UI 모습 탭1

![바뀐 UI2](https://github.com/wlxo0401/video_split/blob/main/readme_img/9.PNG) 

바뀐 UI 모습 탭2

<hr>

```
2021-04-30 ~ 2021-05-06

1. 탭 메뉴 두개 추가
2. 영상 구간 나누기 추가
3. 구간 나누면서 영상 해상도 변경 추가
4. 해상도는 체크로 구분 가능하게
5. 소스코드 다듬기
6. 파일 경로, 이름, 확장자 나누는 것은 최대한 os 라이브러리 활용
7. ffmpeg 없으면 실행을 안시키도록 변경

예정 

1. 해상도만 변경 가능한 기능 추가하기

```

![해상도 변경 체크 모습](https://github.com/wlxo0401/video_split/blob/main/readme_img/10.PNG) 

해상도 변경 체크 모습

![해상도 변경 체크 안한 모습](https://github.com/wlxo0401/video_split/blob/main/readme_img/11.PNG) 

해상도 변경 체크 안한 모습

<hr>

```
2021-05-13 ~ 2021-05-13

1. 영상 로드하면 1번탭 영상 끝 시간 입력
2. 영상 로드하면 영상 해상도 미리 입력
3. 1번 탭 저장될 파일 위치 + 이름이 같은 파일이 있으면 그 파일은 
   삭제하고 다시 새 파일 저장
4. ffmpeg가 깔리지 않은 컴퓨터는 설치 방법으로 자동 유도

예정 

1. 해상도만 변경 가능한 기능 추가하기

```

![영상정보 미리 로드](https://github.com/wlxo0401/video_split/blob/main/readme_img/12.PNG) 

영상과 해상도가 미리 입력된 모습

<hr>

```
2021-05-14 ~ 2021-05-14

1. ui 이름 정리
2. 출력되는 메세지 내용 변경
3. 해상도 변경용 탭 완성

```

![영상정보 미리 로드](https://github.com/wlxo0401/video_split/blob/main/readme_img/13.PNG) 

영상 해상도 변경하는 부분

<hr>

```
2021-05-20 ~ 2021-05-20

1. mov 확장자 사용 가능
```

