error1 = '''
<!DOCTYPE html>
<html lang="en">
{% include '../main/head.html' %}
 <body class="bg-light">
<div class="container" style="width: 80%">
{% include '../main/navbar.html' %}
<a href="/service/search_main"  type="button"> 메인으로 </a></p>
<h1>로그인 실패 다시 시도해주세요.</h1>
<p><a href="/member/sign_up"  type="button"> 회원가입 </a>
<a href="/member/sign_in" type="button"> 로그인 </a>
</div>
</body>
</html>
'''
 
 
error = '''
<!DOCTYPE html>
<html lang="en">
<!-- head  -->
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
  <meta name="generator" content="Jekyll v3.8.6">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
 
<title>GDP</title>
<!-- CSS -->
 
  <!-- Bootstrap-->
  <link rel="canonical" href="https://getbootstrap.com/docs/4.4/examples/cover/">
  <!--내 위치 입력(바탕화면 및 navbar)-->
  <link href="/static/css/navbar.css" rel="stylesheet">
  <link href="/static/css/cover.css" rel="stylesheet">
  <!-- Bootstrap core CSS -->
  <link href="https://getbootstrap.com/docs/4.4/dist/css/bootstrap.min.css" rel="stylesheet" >
  <!-- Favicons -->
 
  <!-- 그래프 -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.3/c3.min.css" rel="stylesheet" />
  <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
  <script src = "https://cdnjs.cloudflare.com/ajax/libs/d3/5.9.7/d3.min.js"></script>
  <script src = "https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.3/c3.min.js"></script>
 
  <script src="https://d3js.org/d3-format.v1.min.js"></script>
  <!--Bootstrap and c3 style-->
  
 
<!-- style  -->
  <style>
    .bd-placeholder-img {
      font-size: 1.125rem;
      text-anchor: middle;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
      }
     
    @media (min-width: 768px) {
      .bd-placeholder-img-lg {
        font-size: 3.5rem;
      }
 
      .c3-region-0 {
      fill: red;
      }
      .c3-region.foo {
      fill: green;
      }
      .c3-region.foo1 {
      fill: blue;
      }
      .c3-xgrid-line.red line {
      stroke: rgb(214, 121, 121);
    }
    .c3-xgrid-line.red_text text {
    fill: rgb(250, 0, 0);
    }
    .c3-xgrid-line.black_text text {
    fill: rgb(0, 0, 0);
    }
    }
    </style>
  <!-- Custom styles for this template -->
</head>
 
 
<body class="bg-light">
    <div class="container-md pt-0" style="width: 80%">
            <header class="masthead mb-auto ">
                <div class="inner">
                    <nav class="nav nav-masthead justify-content-center">
                    <a class="nav-link active" href="/service/search_main">Home</a>
                    <a class="nav-link" href="/member/sign_in">Sign In</a>
                    <a class="nav-link" href="/member/sign_up">Sign Up</a>
                    <a class="nav-link" href="/board/board_qna"> Q & A </a>
                    </nav>
                </div>
            </header>
        <div class="container-md pt-5" style="width: 80%">
            <hr class="my-5">
            <br>
            <center>
                <h1> 로그인 실패 </h1>
                <h2 class="md py-5"> 다시 시도해주세요 ! </h2>
            </center>
            <hr class="py-2" >
            <br>
                
            <br>
        </div>
    </div>
</body>
</html>
'''
 
 
#  <div class="container-md pt-2" style="width: 45%" >
#                 <a href="/member/sign_in"  class="btn btn-lg btn-dark btn-block" type="button"> Sign In </a>
#                 <a href="/member/sign_up"   class="btn btn-lg btn-dark btn-block" type="button"> Sign Up </a>
#             </div>