
```py
< views.py>
@csrf_exempt
def search_detail(request) :
    if request.method == 'GET' :
        data = list(GDPTable.object.all().values("CountryName"))
        return render(request, 'service/search_detail.html', {'list':data , 'year':range(1960,2020,1), 'how_many':range(1,31,1)})

```



```html
<search_detail.html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Search Country and Year</title>
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
</head>
<body>
<!-- 로그인 start -->
<div class="container-md pt-5">
    
    {% if not request.user.is_authenticated %}
    <p><a href="/member/sign_in"  class="btn btn-dark"> 로그인 - SignIn </a>
    <a href="/member/sign_up"  class="btn btn-dark" > 회원가입 - SignUp </a></p>

    {% else %}

    <p> 반갑습니다. {{request.user.name}}님</p>
    <hr />
    아이디 정보 : {{request.user.username}} <br/>
    이름 정보   : {{request.user.name}} <br/>
    이메일 정보 : {{request.user.email}} <br/>
    <hr />
    
    <p><a href="/member/user_mypage"> 마이페이지 </a>
    <a href="/member/sign_out"> 로그아웃 </a></p>
    
    {% endif %}
</div>


<!-- 로그인 end -->

    <form action ="/service/search_show" method ="post">
        <h4>나라명과 년도 검색하세요 </h4>
            <select class='form-control'  name='country_name' id = 'country_name'>
                <option value='' selected>-- 선택 --</option> 
                {% for one in list %}
                    <option value='{{one.CountryName}}'>{{one.CountryName}}</option>
                {% endfor %}
            </select>
            <select class='form-control'  name='year' id = 'year1'>
                <option value='' selected>-- 선택 --</option> 
                {% for tmp in year %}
                    <option value='{{tmp}}'>{{tmp}}</option>
                {% endfor %}
            </select>
            <input type ="submit" value = "검색" id = 'search1' />
    </form>
    <hr> <hr>
    <form action ="/service/sort_by_year" method ="post">
        <h4>년도 / 1위부터 나라 수 </h4>
            <select class='form-control'  name='year' id = 'year2'>
                <option value='' selected>-- 선택 --</option> 
                {% for tmp in year %}
                    <option value='{{tmp}}'>{{tmp}}</option>
                {% endfor %}
            </select>  
            <select class='form-control'  name='how_many' id = 'how_many'>
                <option value='' selected>-- 선택 --</option> 
                {% for tmp1 in how_many %}
                    <option value='{{tmp1}}'>{{tmp1}}</option>
                {% endfor %}
            </select>
            <input type ="submit" value = "Top Country 검색" id = 'search2'/> 
    </form>
    <hr> <hr>
    <h4> 나라별 GDP 상승세 </h4>
    <a href="/service/search_country" class="form-control" style="margin-bottom: 5px;" > search_country</a>  


<script>
    
    
        $("form").submit(function(){
            if ($('#country_name').val() == "" || $('#year1').val() == "" ){
                alert('똑바로 해1')
                $("#country_name").focus();
                return false;
            }   else {
                    $('#search1').click(function(){
                        $('#form').attr('action', '/service/search_show')
                    })

                }
        })  
    
       
    
    
</script>


</body>

</html>

```




```html
<search_country.html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <title>Document</title>

    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
</head>
<body>
    {% autoescape off %}
    
    <input type='button' value = '뒤로가기' onclick = 'history.back();'/>
    
    
    
    <form action='/service/search_country_graph' method='GET'>
        <label>
            <select class='form-control'  name='CountryName'>
                <option value='' selected>-- 선택 --</option>
                
                {% for one in list %}
                    <option value='{{one.CountryName}}'>{{one.CountryName}}</option>
                {% endfor %}
            </select>
        </label>
        <input type='submit' value = '그래프 보기'/>  
    </form>
    
    
            <!--{% autoescape off %}
            {{df_table}}
            {% endautoescape %}-->

    
    
        
  
    {% endautoescape %}
</body>
</html>

```



```html
# 민섭이
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Country_graph</title>

    <link href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.3/c3.min.css" rel="stylesheet" />
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/d3/5.9.7/d3.min.js"></script>
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.3/c3.min.js"></script>

    <script src="https://d3js.org/d3-format.v1.min.js"></script>

    <style>
    .c3-region-0 {
        fill: red;
    }

    .c3-region.foo {
        fill: green;
    }

    .c3-region.foo1 {
        fill: blue;
    }
    </style>
</head>
    <body>
        <div class="container">
            <h3>{{one.CountryName}} </h3>

            <form action='/service/search_country_graph_pop' method='GET' name='2'>
                <table>
                    <tr>
                    <input type="submit" value="{{one.CountryName}}" name = "CountryName_pop"/>
                    </tr>
                </table>
            </form>

            <div style="margin-top:5px; margin-bottom: 5px;">
                <h3><a href="/service/search_country" class="btn btn-primary">목록으로</a></h3>
            </div>
            <table class="table">

            </table>
            <div id="chart"></div>
            
            
            
                <!-- <img src='{{graph1}}' width="1600" height="800"/> -->
                </tr>         
        </table>

        <script> 
        $(function(){               

            var obj = eval('{{Country_gdp}}')  //python 문자를 script 배열로 변환
            obj.unshift('{{one.CountryName}}');
            //console.log(obj);
            
            var obj1 = ['x']
            for (var i=1960; i<=2018; i++){
                obj1.push(i)
                //console.log(obj1);   
            }

            var korea = eval('{{korea_gdp}}')
            korea.unshift('KOREA')
            console.log(korea);
                
            var korea1 = ['x1']
            for (var i=1960; i<=2018; i++){
                korea1.push(i)
            }
            console.log(korea1);

                // 차트의 x축, y축의 값을 결정
            var chart = c3.generate({
                data: {
                    xs:{
                        '{{one.CountryName}}':'x',
                        'KOREA':'x1',
                    },
                    columns: [
                        obj1,  // 년도
                        korea1, // 한국 년도
                        obj, // gdp값
                        korea, // 한국  gdp
                    ]
                },
                // 현재 x축의 값을 결정
                axis: { 
                    // x축의 높이를 결정
                    x: {
                            height: 20,
                            tick: {
                            values: [1960, 1965, 1970, 1975, 1980, 1985,1990,1995,2000,2005,2010,2015,2018],
                            type : 'category'
                        }
                    },

                    // y축의 범위 결정 및 라벨 제목 설정
                    y: { 
                        label: 'GDP (Current USD)',
                        tick: {
                    // y축의 포맷 설정 ($,d)를 넣는다 (d= 정수)
                            format: d3.format("$,d"),
                        }    
                        // max: 30000000000000,
                        // min: -100,
                    }
                },
                // 그리드의 범위 지정
                regions: [  
                    {start:1979, end:1980, class:'foo'},
                    {start:1980, end:1983, class:'foo1'}
                ]
                // 차트의 크기 설정
            });
            setTimeout(function () {
            chart.resize({height:700, width:1800})
            }, 1000);
                // 그리드 설정
            setTimeout(function () {
                chart.xgrids([
                        {value: 1973, text: '제1차 석유파동(1973)'}, 
                        {value: 1980, text: '제2차 석유파동(1979~1980)'}, 
                        {value: 1983, text: '유럽 경기침체(1980~1983)'}, 
                        {value: 1985, text: '플라자 합의(1985)'}, 
                        {value: 1994, text: '일본 버블경제 붕괴(1994)'},
                        {value: 1997, text: 'IMF(1997)'},
                        {value: 2007, text: '서브프라임 모기지 사태(2007)'},
                        {value: 2011, text: '동일본 대지진(2011)'},
                        {value: 2016, text: '브렉시트(2016)'},
                        {value: 2018, text: '현재'}
                        
                    ]);
            }, 1000);
        })
        </script>        
    </body>
</html>

```
