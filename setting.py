#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 본인 정보로 변경해주세요
Bot_Prefix = "!"
Bot_Name = "봇 이름"
Bot_TOKEN="봇 토큰"
Bot_Image = "봇 프로필 이미지"
Bot_invite = "봇 초대링크"

Bot_Owner= "봇 소유자 디스코드 ID"
Owner_Name = "디스코드 닉네임(닉네임#태그)"


Email_Sender="보내는 이메일"
Sender_PW= "보내는 이메일 비밀번호"
Receive_Email= "받는 이메일"

Stop_SelfCheck = " 08:10:00"# !일괄진단이 멈추는 시간


















#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 파일 공통 변수
import os
from datetime import datetime
import pytz

now = datetime.utcnow()
now_local = datetime.now()
UTC = pytz.timezone('UTC') 
KST = pytz.timezone('Asia/Seoul')
now_utc = now.replace(tzinfo=UTC)
Now_KST=now_utc.astimezone(KST)
Today_KST=Now_KST.strftime("%Y-%m-%d")
Now_KST=Now_KST.strftime("%Y-%m-%d %H:%M:%S")