```html
<form action='/service/search_country_graph_pop' method='GET'>
            <table>
                <tr>
                <input type="submit" value="{{one.CountryName}}" name = "CountryName_pop" />
                </tr>
            </table>
</form>


<input type="submit" value="{{one.CountryName}}1인당gdp" name = "CountryName" />

            var korea = eval('{{korea}}')
            korea.unshift('KOREA')
            console.log(korea);
            
            // 년도
            var korea1 = ['x1']
            for (var i=1960; i<=2018; i++){
                korea1.push(i)
            }
            console.log(korea1);

-----------------------------X,Y 축 있는 그래프 설정-----------------------------------
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Country_graph</title>

    <!-- c3 사용하기 위해 필요한 css -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.3/c3.min.css" rel="stylesheet" />
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/d3/5.9.7/d3.min.js"></script>
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.3/c3.min.js"></script>

    <script src="https://d3js.org/d3-format.v1.min.js"></script>
    
    <!-- 그래프의 범위 그리드 설정하기 위한 스타일 css-->
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
            <tr>
                <th class="bg-light">그래프 들어갈 자리</th>
            </tr>
            </table>
            <div id="chart"></div>
                </tr>         
        </table>

        <script> 
        $(function(){               
            // 1인당 GDP(y축) , eval은 python문자를 script 배열로 변환
            var obj = eval('{{capita}}')  
            obj.unshift('y');
            //console.log(obj);
            
            // 년도
            var obj1 = ['x']
            for (var i=1960; i<=2018; i++){
                obj1.push(i)
                //console.log(obj1);   
            }

                // 차트의 x축, y축의 값을 결정
            var chart = c3.generate({
                data: {
                    x:'x',
                    y:'y',
                    // x, y축이 된다
                    columns: [
                        obj1,  // 년도
                        // korea1, // 한국 년도
                        obj, // gdp값
                        // korea, // 한국  gdp
                    ]
                },
                // 현재 x축의 값을 결정 //
                axis: { 
                    x: {    // x축의 높이를 결정
                            height: 20,
                            tick: {
                            // x축에 표시 될 값을 결정
                            values: [1960, 1965, 1970, 1975, 1980, 1985,1990,1995,2000,2005,2010,2015,2018],
                            // x 축에 표시될 type 결정 (다양한 type이 있다)
                            type : 'category'
                        }
                    },

                    // y축의 범위 결정 및 라벨 제목 설정 //
                    y: { 
                        // y축의 라벨 이름 결정
                        label: 'GDP (Current USD)',
                        tick: {
                        // y축의 포맷 설정 ($,d)를 넣는다 (d= 정수)
                            format: d3.format("$,d"),
                        }    
                        // y축의 최대값과 최소값 결정
                        // max: 30000000000000,
                        // min: -100,
                    }
                },
                // 그리드의 범위 지정
                regions: [  
                    {start:1979, end:1980, class:'foo'},
                    {start:1980, end:1983, class:'foo1'}
                ]
            });
            // 차트의 크기 설정
            setTimeout(function () {
            chart.resize({height:700, width:1800})
            }, 1000);
            // x축 그리드 설정
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
            // 그래프가 1/1000초 뒤에 표시 된다는 뜻
            }, 1000);
        })
        </script>        
    </body>
</html>
</body>
</html>

-----------------------------MULTI X,Y 축 있는 그래프 설정-----------------------------------

<!-- 이상 생략-->

<div id="chart"></div>          
    <script> 
    $(function(){               

        var obj = eval('{{year}}')
        obj.unshift('{{one.CountryName}}');
        
        var obj1 = ['x']
        for (var i=1960; i<=2018; i++){
            obj1.push(i)
        }
        // 추가로 들어갈 x값과 y값 입력
        var korea = eval('{{korea}}')
        korea.unshift('KOREA')
            
        var korea1 = ['x1']
        for (var i=1960; i<=2018; i++){
            korea1.push(i)
        }
        var chart = c3.generate({
            data: {
                xs:{
                    
                    '{{one.CountryName}}':'x',
                    'KOREA':'x1',
                },
                columns: [
                // columns에 4개 넣는다 x축 2개, y축 2개 순으로
                    obj1,   // 년도
                    korea1, // 한국 년도
                    obj,    // gdp값
                    korea,  // 한국  gdp
                ]
            }});
    </script>        
</body>
</html>
```


```py
return render(request,'service/search_country_graph_pop.html',{'x':x, 'pop_real':pop_real, 'x_korea':x_korea, 'real_korea':real_korea,'gdp1_real':gdp1_real})


```