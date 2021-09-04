import discord #pip
from discord.ext import commands
import asyncio
import smtplib # 메일을 보내기 위한 라이브러리 모듈
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 

import setting
Owner_ID = setting.Bot_Owner
Now_KST = setting.Now_KST
sendEmail = setting.Email_Sender
recvEmail = setting.Receive_Email
password = setting.Sender_PW

class semail(commands.Cog):

    def __init__(self, client):
        self.bot = client
        self.stopcodes = 0


    @commands.command(aliases=['DB전송']) # Com1
    async def DB저장(self, ctx):
        if str(ctx.author.id) == Owner_ID:
            print("------------------------------")
            print(f'DB 전송을 준비합니다.')
            print(f'-이메일 계정을 입력합니다.')
            if sendEmail == "-":
                print("전송용 이메일이 입력되어 있지 않아 전송을 중단합니다 `setting.py`에 이메일을 등록해주세요`")
                return
            if recvEmail == "-":
                print("받는 이메일이 입력되어 있지 않아 전송을 중단합니다 `setting.py`에 이메일을 등록해주세요`")
                return
            if password == "-":
                print("전송용 이메일의 비밀번호가 입력되어 있지 않아 전송을 중단합니다 `setting.py`에 비밀번호를 등록해주세요`")
                return

            smtpName = "smtp.gmail.com"
            smtpPort = 587

            #여러 MIME을 넣기위한 MIMEMultipart 객체 생성
            msg = MIMEMultipart()
            print("-메일 제목을 입력합니다.")
            msg['Subject'] ="봇(Discord) DB"
            print("-메일 전송자와 수신자를 입력합니다.")
            msg['From'] = '디스코드 봇' 
            msg['To'] = recvEmail 

            #본문 추가
            print("-메일 본문을 입력합니다.")
            text = ("전송된 시각: "+Now_KST)
            contentPart = MIMEText(text) #MIMEText(text , _charset = "utf8")
            msg.attach(contentPart) 

            #파일 추가
            print("-DB를 메일에 첨부합니다.")
            print('')
            etcFileName = 'userDB.xlsx'
            with open(etcFileName, 'rb') as etcFD : 
                etcPart = MIMEApplication( etcFD.read() )
                #첨부파일의 정보를 헤더로 추가
                etcPart.add_header('Content-Disposition','attachment', filename=etcFileName)
                msg.attach(etcPart) 

            etcFileName = 'selfcheckDB.xlsx'
            with open(etcFileName, 'rb') as etcFD : 
                etcPart = MIMEApplication( etcFD.read() )
                #첨부파일의 정보를 헤더로 추가
                etcPart.add_header('Content-Disposition','attachment', filename=etcFileName)
                msg.attach(etcPart) 

            s=smtplib.SMTP( smtpName , smtpPort )
            print("등록된 이메일 계정으로 로그인합니다.")
            s.starttls()
            s.login( sendEmail , password ) 
            s.sendmail( sendEmail, recvEmail, msg.as_string() )  
            s.close()
            print("DB를 성공적으로 전송하였습니다.")
            print("------------------------------")
            await ctx.send(embed=discord.Embed(title='봇 DB가 관리자 메일로 전송되었습니다.', description='전송된 시각 : '+Now_KST, color=0xf8e71c))
        
        else:
            print(f'{ctx.author}님이 DB파일 전송을 시도하였습니다. : '+Now_KST)




def setup(client):
    client.add_cog(semail(client))