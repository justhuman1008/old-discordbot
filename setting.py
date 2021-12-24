#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 본인 정보로 변경해주세요

Bot_Prefix = "!"
Bot_Name = "봇 이름"
Bot_TOKEN="봇 토큰"
Bot_Image = "봇 프로필 이미지 링크"
Bot_invite = "봇 초대링크"
Bot_id = "봇 ID"

Bot_Owner= "봇 소유자 디스코드 ID" #참고: https://vo.la/7D69P
Owner_Name = "디스코드 닉네임(닉네임#태그)" #본인의 디스코드 닉네임#태그
















#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 이미지 대응
if Bot_Image == "봇 프로필 이미지 링크":
    Bot_Image = "https://discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png"
# 시간대 변경(KST)
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