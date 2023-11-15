# DigitingGale 
: 딥러닝을 활용한 수액 원격 관리 시스템   
(2022 성균관대학교 창의혁신 DNA Project)

## Overview
vision AI 기반 수액 제어 디바이스를 제안합니다. 주변 환경에 영향을 많이 받고, 정량적 수치만 모니터링할 수 있어 고정밀도가 요구되던 기존 수액 모니터링 디바이스의 문제점을 해결하기 위해 DL기반의 감지부와 peristaltic Pump를 활용한 제어부로 구성된 수액 제어 디바이스를 개발하였습니다.   

![figure1](/assets/figure1.png)  

## Features
1. Flow Dectection
감지부에서는 CNN기반의 Yolov2 DL모델을 사용하여 라즈베리파이 캠에서 송신받은 실시간 수액화면의 수액을 감지하고 flow rate를 계산합니다.
![figure2](/assets/figure2.png)  

2. Peristaltic Pump & Feedback Loop
제어부에서는 사용자로부터 입력받은 정보를 기반으로 수액 pump를 실행하고, 감지부에서 예측한 실시간 유량과 입력정보를 지속적으로 비교하여 pump를 제어합니다.
![figure3](/assets/figure3.png)  

