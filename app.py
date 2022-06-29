import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import av
qrDetector = cv2.QRCodeDetector()
class QRreader:
    def __init__(self) -> None:
        self.QRresult = None
        
    def get_QRresult(self):
        return self.QRresult

    def recv(self,frame):
        img = frame.to_ndarray(format="bgr24")
        data= qrDetector.detectAndDecode(img)
        if data[0] != "":
            self.QRresult = data[0]
            for i in range(4):
                cv2.line(img,tuple(map(int,data[1][0][i-1])),
                tuple(map(int,data[1][0][i])), (255, 0, 0), 
                thickness=3, lineType=cv2.LINE_4)
            cv2.putText(img,text=data[0],org=tuple(map(int,data[1][0][0])),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,
                        color=(0, 0, 255),thickness=2,lineType=cv2.LINE_4)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("WEBカメラ取り込み")
ctx = webrtc_streamer(key="example", video_processor_factory=QRreader,
                    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })
if ctx.video_processor:
    if st.button("テキスト出力"):
        st.write(ctx.video_processor.get_QRresult())