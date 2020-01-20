# dummy_2020.01.20
---

```py

from django.conf import settings # << 해당 위치의 global settings 내용
# local settings.py에서 오버라이딩 가능

# 기본 로그인 페이지 URL 지정
# login_required 장식자 등에 의해서 사용
LOGIN_URL = '/accounts/login/'

# 로그인 완료 후 next 인자가 지정되면 해당 URL 페이지로 이동
# next 인자가 없으면 아래 URL로 이동
LOGIN_REDIRECT_URL = '/accounts/profile/'

# 로그아웃 후에 next 인자기 지정되면 해당 URL 페이지로 이동
# next 인자가 없으면 LOGOUT_REDIRECT_URL로 이동
# LOGOUT_REDIRECT_URL이 None(디폴트)이면, 'registration/logged_out.html' 템플릿 렌더링
LOGOUT_REDIRECT_URL = None

# 인증에 사용할 커스텀 User 모델 지정 : '앱이름.모델명'
AUTH_USER_MODEL = 'auth.User'


```


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>main</title>
</head>
<body>
   {% if form.errors %}
   <p>
       There's something wrong with what you entered!
   </p>
   {% endif %}

   {% if next %}
   <p>You can't access that page.</p>
   {% endif %}
   <form method="post" action="{% url 'login' %}">
       {% csrf_token %}

       {{ form.username}}
       {{ form.password}}
        <input type="submit" value="login">
        <input type="hidden" name= next value="{{next}}">

</body>
</html>
```