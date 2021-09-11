# 그저 평범한 봇
[![Send mail](https://img.shields.io/badge/-seanking1008@naver.com-63d863?style=flat-square&logo=gmail&logoColor=white&link=mailto:support@leok.kr)](mailto:support@leok.kr)  ![Badge](https://img.shields.io/badge/-v1.2.1-9ACD32?style=flat-square&logo=pypi&logoColor=white&link=mailto:support@leok.kr)  ![Badge](https://img.shields.io/badge/-v3.x-3776AB?style=flat-square&logo=python&logoColor=white&link=mailto:support@leok.kr)  
Discord.py를 이용한 잡탕 봇 프로젝트입니다.

Developer Discord: 그저 평범한 인간#8138     
[개발자 운영버전 봇 초대하기](https://discord.com/oauth2/authorize?client_id=857814380749651998&permissions=173144927479&scope=bot)

<details><summary>▶️봇 도움말 캡쳐(V1.2)</summary>
<p>
<img src="/Image/help.png" alt ="Data" style="width: 500px;"/>  
</p>
</details>

## 💻셀프 호스팅
- 프로그래밍에 대해 1도 모르는분인 경우에 보시면 됩니다. 어느정도 안다는 분은 안보시는게..~~안구테러~~  
##### 1. [Python](https://www.python.org/)을 다운로드 받습니다.
##### 2. 해당 프로젝트 파일을 다운로드 받습니다. 
##### 3. 명령 프롬프트에 다음과 같이 입력합니다.   
  ```shell
  > pip install -r requirements.txt
  ```
##### 4. `setting.py` 파일에 본인의 정보를 입력합니다.   
 - 편집창 들어가기 : `setting.py` 우클릭후 `Edit with IDLE` 클릭    
##### 5. [Heroku](https://www.heroku.com/) 홈페이지에 회원가입합니다.
##### 6. [Git](https://git-scm.com/download/win)과 [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)를 다운로드합니다.
##### 7. 새로운 앱을 만듭니다.
   - `New` -> `Create new app` 클릭
   - 이름 입력후 `Create app` 클릭
   - `Setting` 클릭 -> `Add Buildpack` -> `Python` -> `Save changes` 클릭
##### 8. Heroku에 프로젝트 업로드
   - 명령 프롬프트를 열고 다움과 같이 입력합니다.
       ```shell
       > heroku login
       ```
      아무 키나 누르면 사이트가 열립니다. 그곳에서 `Log In` 클릭    
     

       ```shell
       > cd {프로젝트 폴더 경로}
       ```
       ```shell
       > git init
       > heroku git:remote -a {Heroku 앱이름}
       ```
       ```shell
       > git config --global user.name "a"
       > git config --global user.email "자신의 이메일"  
       ```
       
       ```shell
       > git add .
       > git commit -am "아무거나"
       > git push heroku master
       ```
##### 9. 봇 가동하기
   - [Heroku 사이트](https://dashboard.heroku.com/apps)에 접속해서 본인의 앱을 클릭합니다.
      <img src="/Image/Heroku_Worker.png" alt ="Data"/>  
   - `Resources` -> `연필` -> `스위치` 활성화 -> `confirm` 클릭 (Resource탭에 아무것도 안뜬다면 잠시 기다린 후 새로고침해주세요)
