로그인 & 회원가입 기능 
(login & registration function)

사용한 기술: flask session, pymongo 
(skills used: flask session, pymongo)

기능: 
1) 유저가 로그인하면 데이터베이스에서 확인한다. 
   (Authentification with mongoDB) 
2) 회원가입하면 데이터베이스에 저장된다 
   (Storing user-data in mongoDB upon registration) 
3) 로그인 또는 회원가입을 안한 경우 홈페이지로 이동불가 + 이미 한 경우 다시 로그인, 회원가입 페이지로 이동불가 
   (cannot access user-homepage if not logged-in or registered + and vice versa) 
