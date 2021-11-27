# README.md

💡 **실행 방법**

1. python server.py로 서버 실행
    
    ```python
    -- port : 서버 포트 설정 default:8080
    -- model_dir : model directory 설정
    ```

2. chrome 127.0.0.1:8080 접속
3. 원하는 부분 check하고 start 클릭 
  

💡 **코드 구조**

1. `pose_modeule.py`
    - `draw_count`
        - pose_estimation 적용, 그리고 classification 학습모델 적용후 count

1. `server.py`
    - Web server / python
    - WebRTC를 적용, 그리고 server.py와 client.js의 실시간 비디오/오디오 스트리밍

1. `client.js`
    - Web front side
    - 유저 카메라에 연결 요청,  서버와 webRTC 적용
#
# 
#
💡 **WebRTC 동작 순서**
#  
#
#  
-  웹 브라우저가 서버에 `client.js`와  `index.html` 요청.
-  Start 버튼을 누르면 `RTCPeerConnection` 객체를 생성, 그리고 그 객체에 여러 event listener들을 붙힘.
-  `negotiate()`함수를 통해 **signaling** 수행
    - Signaling은 peer-to-peer connection을 설립시키기 위해 두 peer가 준비됬는지를 확인하기 위한 과정
-  Stream 전송 
    - Signaling 작업이 끝나고 WebRTC connection이 완료되면 바로 video transmission 시작.
    - 모든 stream에 addTrack() 함수가 붙혀져 있기 때문에 서버에서 이걸 바로 읽고 이에 대해 원하는 작업이 가능.
# 
# 
#
💡 **현재 프로젝트 WebRTC 구조**
#
#
#
- 기존 WebRTC는 peer2peer, 즉 브라우저/브라우저 간의 직접적인 연결을 적용하고자함.
- 다만 우리 프로젝트에서는 브라우저간의 연결은 할 필요가 없다.
- 때문에 현재 서버를 하나의 브라우저처럼 사용
- 이를 가능하게 해주는 것이 airotc 라이브러리.
- 브라우저와 서버가 offer/answer을 통해 signaling을 완료한 후, SRTP, TURN, STUN과 같은 자체 지원 프로토콜을 통해 통신하게 된다.
- 때문에 Video, audio전송에 있어서 빠르게 진행이 가능하고,  aiortc라이브러리가 받은 stream 값에 대해 ml 모델을 적용하기 쉽게 해준다.