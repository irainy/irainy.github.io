function B2D(){
    var exp = _G.birthDate.sex ? 77 : 74;
    console.log(_G);
    var curtime = new Date();
    var birtime = new Date(_G.birthDate.yy, _G.birthDate.mm, _G.birthDate.dd);
    var avgtime = new Date(_G.birthDate.yy + exp, _G.birthDate.mm, _G.birthDate.dd);

    var countDown = avgtime - curtime;
    var perc = Math.ceil((countDown / (avgtime - birtime)) * 100);

    $('.results').show();
    $('.progress-bar-danger').animate({
        width: perc+"%"
    }, {
        duration: 400,
        complete: function(){
            $(".cursor").css("left", perc+"%");
            setTimeout(function(){
                $(".cursor").tooltip({
			title: 'You got '+perc+'% left !'
		}).tooltip('show');
            },500);
        }
    })
    function typewriter(text) {
        var text = text.length === 0 ? 'Text to be typed here.' : text;
        var i = 0;
        var write = setInterval(function(){
            if(i < text.length){
                if(text[i] === '\n'){
                    $('.words').append($('<br/>&nbsp;&nbsp;&nbsp;&nbsp;'));
                }else{
                    $('.words').html($('.words').html() + text[i]);
                }
                i++;
            }else{
                clearInterval(write);
                countdown();
            }
        }, _G.c);
    }

    setTimeout(function(){
        var info = {
            age: curtime.getFullYear()-_G.birthDate.yy,
            sex: _G.birthDate.sex?'女':'男',
            exp: _G.birthDate.sex?77:74
        }
        var text = ["时光荏苒，岁月如梭！你已经为中华民族的伟大复兴无私奉献了"+info.age+"年的青春！\n"
                    + "据世界卫生组织(WHO)2009年统计结果显示，中国"+info.sex+"性出生期望寿命为"+info.exp+"岁，\n"
                    + "鲁迅曾经说过，时间就像海绵里的水，只要愿意挤，总是会挤干的...  \n"
                    + "So, let's watch it count down to the end of your life, TOGETHER~\n",
                    "东流逝水，叶落纷纷，转眼间在此间的世界里你已经度过了"+info.age+"个春秋！\n"
                    + "据世界卫生组织(WHO)2009年统计结果显示，中国"+info.sex+"性出生期望寿命为"+info.exp+"岁，\n"
                    + "时间就像手纸，看起来很多，总是用着用着就用光了...\n"
                    + "So, let's watch it count down to the end of your life, TOGETHER~\n",
                    "时光飞逝若白驹过隙，忽然而矣！\n"
                    + "据世界卫生组织(WHO)2009年统计结果显示，中国"+info.sex+"性出生期望寿命为"+info.exp+"岁，\n"
                    + "平均算来，你已经度过了将近"+Math.floor(100-(info.exp-info.age)/info.exp*100)+"%的人生！\n"
                    + "So, let's watch it count down to the end of your life, TOGETHER~\n"
                    ];
        typewriter(text[Math.floor(Math.random()*10)%text.length]);
    },1500);
    function countdown(){
        $('.countdown').show().click(function(){
            $('.btn-warning').show().unbind('click').click(function(){
                var reset = confirm("重新设定时间？");
                if(reset){
                    clear();
                    clearInterval(cd);
                }
            });
        })
        Clock = {
            seconds: Math.floor(countDown / 1000),
            down: function(){
                this.seconds--;
            }
        }

        $('.cd-seconds').html(Clock.seconds);
        $('.cd-milliseconds').html(Clock.milliseconds);

        var cd = setInterval(function(){
            if(Clock.seconds === 0){
                clearInterval(cd);
            }else{
                Clock.down();
                $('.cd-seconds').html(Clock.seconds);
            }
        }, 1000);
    }
    function clear(){
	$('.cursor').tooltip('destroy');
        $('.results').hide();
	$('.countdown').hide();
        $('.words').html('');

        $('.year-face').text(' Year ');
        $('.month-face').text(' Month ');
        $('.day-face').text(' Day ');
        _G.birthDate={yy:0,mm:0,dd:0};
        _G.raw = '';

        setCookie('birthDate', _G.raw, -1);
	checkCookie();
    }
}
function init(){
    console.log('init called');

    $('#entrance').modal({
        backdrop: "static",
        keyboard: false,
        show: true
    })

    $('.year_select').append(tmpl("years"));
    $('.month_select').append(tmpl("months"));
    setDay();

    function setDay(){
      $('.day_select').text('').append(
          tmpl("days", {days:
                      (function(){var d = new Date(_G.year, _G.month, 0);return d.getDate();})() }));
        $(".day_items").on('click', function(){
            var dd = $(this).text();
            $('.day-face').text(dd);
            _G.birthDate.dd = parseInt(dd);
        });
    }  
    $(".year_items").click(function(){
        var yy = $(this).text();
        $('.year-face').text(yy);
        _G.birthDate.yy = _G.year = parseInt(yy);
        setDay();
    });
    $(".month_items").click(function(){
        var mm = $(this).text();
        $('.month-face').text(mm);
        _G.birthDate.mm = _G.month = parseInt(mm);
        setDay();
    });
    

    $(".clear").click(function(){
        $('.year-face').text(' Year ');
        $('.month-face').text(' Month ');
        $('.day-face').text(' Day ');
        _G.birthDate={yy:0,mm:0,dd:0};
    });

    $(".done").unbind('click').click(function(event){
        console.log('btn done clicked');
        event.preventDefault();
        if(_G.birthDate.yy*_G.birthDate.mm*_G.birthDate.dd === 0){
            alert("Select your birth date pls!");
        }else{
            $('#entrance').modal('hide');
            if($('.sexm').hasClass('active')){
                _G.birthDate.sex = 0;
            }else{
                _G.birthDate.sex = 1;
            }
            _G.raw = [_G.birthDate.yy, _G.birthDate.mm, _G.birthDate.dd, _G.birthDate.sex].join('-');
            setCookie('birthDate', _G.raw);
            B2D();
        }
        event.stopPropagation();
    });
}
function getCookie(c_name){
    if (document.cookie.length>0){
        c_start=document.cookie.indexOf(c_name + "=")
        if (c_start!=-1){ 
            c_start=c_start + c_name.length+1 
            c_end=document.cookie.indexOf(";",c_start)
                if (c_end==-1)
                    c_end=document.cookie.length
                    return unescape(document.cookie.substring(c_start,c_end))
        } 
    }
    return ""
}
function setCookie(key, value, years){
    var exdate=new Date();
    exdate.setDate(exdate.getDate()+years*365);
    document.cookie=key + "=" +escape(value)+ ";expires="+exdate.toGMTString()
}
function checkCookie(){
    birthDate=getCookie('birthDate');
    if (birthDate!=null && birthDate!=""){
        _G.raw = getCookie('birthDate');
        _G.birthDate.yy = parseInt(_G.raw.split('-')[0]);
        _G.birthDate.mm = parseInt(_G.raw.split('-')[1]);
        _G.birthDate.dd = parseInt(_G.raw.split('-')[2]);
        _G.birthDate.sex = parseInt(_G.raw.split('-')[3]);
        _G.c = 10;
        B2D();
    }else{
	_G.c = 100;
        init();
    }
}
