function MyTouch(obj, argument){
    if (!(this instanceof MyTouch)) return new MyTouch(obj, argument);

    var _this = this;

    obj = obj || "body";
    _this.obj = document.querySelector(obj);

    var defaults = {
        "width": Math.floor(_this.obj.offsetWidth),//默认为最大宽度，不包括内外边距
        "switchs": false,//惯性滑动
        "list": ".num",//小图列表
        "automatic": false,//自动播放
        "speed": 3000,//速度
        "loop": false,//循环
        "overflow": false,//系统惯性
        "m": 0 ,//边距
    }

    argument = argument || {};

    for (var def in defaults) {
        if (typeof argument[def] === 'undefined') {
            argument[def] = defaults[def];
        }else if (typeof argument[def] === 'object') {
            for (var deepDef in defaults[def]) {
                if (typeof argument[def][deepDef] === 'undefined') {
                    argument[def][deepDef] = defaults[def][deepDef];
                }
            }
        }
    }

    if (argument.switchs) {
        argument.width.toString().indexOf("%") > 0 ? _this.width =  parseInt(_this.obj.offsetWidth * parseInt(argument.width)/100) : _this.width = parseInt(argument.width) + argument.m;
    }else{
        _this.width = Math.floor(_this.obj.offsetWidth);
    }

    _this.switchs = argument.switchs;
    _this.automatic = argument.automatic;
    _this.speed = argument.speed;
    _this.loop = argument.loop;
    _this.overflow = argument.overflow;
    _this.m = argument.m;

    _this.oDiv = _this.obj.querySelectorAll("ul")[0];//运动的ul
    _this.list = _this.obj.querySelector(argument.list);//小列表
    _this.elements = _this.oDiv.querySelectorAll("li");//li
    _this.length = _this.elements.length - 1;//索引-1

    Array.prototype.forEach.call(_this.elements, function(el, i){
        _this.elements[i].style.width = _this.width - _this.m + "px";
    });

    _this.mLeft = _this.oDiv.getBoundingClientRect().left;

    if(_this.loop && !_this.switchs){
        _this.loopLeft = true;
        _this.loopRight = false;

        var domFirst = _this.elements[0].cloneNode(true);
        var domLast = _this.elements[_this.length].cloneNode(true);

        _this.oDiv.appendChild(domFirst);
        _this.elements[0].parentNode.insertBefore(domLast, _this.elements[0]);

        _this.leftNum = 1;
        _this.newLength = _this.oDiv.querySelectorAll("li").length;//重新获取li
        _this.oDiv.style.width = (_this.width * _this.newLength) + "px";
        _this.maxWidth = -parseInt(_this.oDiv.style.width);
    }else{
        _this.leftNum = 0;
        _this.oDiv.style.width = (_this.width * _this.elements.length) - _this.m + "px";
        _this.maxWidth = -parseInt(_this.oDiv.style.width) + Math.floor(_this.obj.offsetWidth);
    }

    _this.touch = true;
    _this.index = 0;
    _this.endjuli = _this.juli = _this.endX = _this.disX = 0;

    if(_this.list && !_this.switchs){//添加li
        Array.prototype.forEach.call(_this.elements, function(el, i){
            var li = document.createElement("li");
            if(i == 0){
                li.setAttribute("class", "active");
            }
            _this.list.appendChild(li);
        });
    }

    if (_this.automatic && !_this.switchs) {
        _this.fnAutomatic();
    }

    _this.oDiv.style.display = "table";
    _this.oDiv.style.transitionDuration = "0ms";
    _this.oDiv.style.transform = "translate3d(" + (- (_this.leftNum * _this.width)) + "px, 0px, 0px)";

    if (!_this.overflow && _this.width >= Math.floor(_this.obj.offsetWidth)) {
        _this.oDiv.addEventListener("touchstart", function(ev){
            _this.fnStart(ev);
            return false;
        },false) ;
    }else {
        _this.obj.style.overflowX = "auto";
        _this.obj.style.webkitOverflowScrolling = "touch";
    }

};

//触屏开始
MyTouch.prototype.fnStart = function(ev) {
    var _this = this;
    var oEvent = ev || event;

    _this.endX = _this.disX = oEvent.targetTouches[0].pageX;
    _this.endY = _this.disY = oEvent.targetTouches[0].pageY;

    _this.scrollY = undefined;

    _this.move = function(ev){_this.fnMove(ev);}
    _this.end = function(ev){_this.fnEnd(ev);}

    // _this.endjuli = Math.floor(_this.oDiv.getBoundingClientRect().left) - _this.mLeft;
    // _this.fnTranslate(0, _this.endjuli);

    clearInterval(_this.setActive);

    _this.touch = true;

    _this.moveNum = 1;

    _this.startDate = new Date();

    document.addEventListener("touchmove", _this.move, false);
    _this.oDiv.addEventListener("touchend", _this.end, false);
};
//触屏滑动
MyTouch.prototype.fnMove = function(ev){
    var _this = this;
    var oEvent = ev || event;

    _this.moveNum ++;

    if(_this.moveNum == 2){//只获取一次
        _this.endjuli = Math.floor(_this.oDiv.getBoundingClientRect().left) - _this.mLeft;
    }

    _this.endX = oEvent.targetTouches[0].pageX;
    _this.endY = oEvent.targetTouches[0].pageY;


    if (typeof _this.scrollY == 'undefined') {
        _this.scrollY = !!( _this.scrollY || Math.abs(_this.endX - _this.disX) < Math.abs(_this.endY - _this.disY));
    }

    if(!_this.scrollY){
        oEvent.preventDefault();

        if(_this.loopRight && (_this.disX - _this.endX) > 30 && _this.loop){
            _this.juli = _this.endX - _this.disX;
            // console.log(_this.juli);
        }else if(_this.loopLeft && (_this.endX - _this.disX) > 30 && _this.loop){
            _this.juli = _this.endX - _this.disX + _this.maxWidth + _this.width;
        }else{
            _this.juli = _this.endX - _this.disX + _this.endjuli;
        }

        if(_this.juli > 0 && !_this.loop){
            _this.fnTranslate(0, _this.juli/3);
        }else if(_this.juli < _this.maxWidth && !_this.loop){
            _this.fnTranslate(0, _this.maxWidth + (_this.juli - _this.maxWidth)/3);
        }else{
            _this.fnTranslate(0, _this.juli);
        }
    }
};
//触屏结束
MyTouch.prototype.fnEnd = function(){
    var _this = this;

    var endDate = new Date();

    // if (_this.time) {clearInterval(_this.time)};
    // _this.time = setInterval(function () {
    // 	document.title = document.title;
    // }, 1);

    if(_this.automatic && !_this.switchs){
        _this.fnAutomatic();
    }

    if(!_this.switchs){
        if(_this.endX - _this.disX > 30){
            _this.index --;
            _this.fnJudgeIndex(false);
            _this.fnActive();
        }else if(_this.disX - _this.endX > 30){
            _this.index ++;
            _this.fnJudgeIndex(true);
            _this.fnActive();
        }else{
            _this.fnActive();
        }
    }else{
        if (!_this.overflow) {
            var speed =  (Math.abs(_this.endX - _this.disX) / (endDate - _this.startDate)) / 2;
            _this.fnSpeed(speed);
        }
    }

    if(_this.juli > 0){
        _this.fnTranslate(200, 0);
        _this.endjuli = _this.juli;
    }else if(_this.juli < _this.maxWidth){
        _this.fnTranslate(200, _this.maxWidth);
        _this.endjuli = _this.juli;
    }

    document.removeEventListener("touchmove", _this.move, false);
    _this.oDiv.removeEventListener("touchend",  _this.end, false);
};
//惯性
//暂不使用，使用系统默认滚动
MyTouch.prototype.fnSpeed = function(speed) {
    var _this = this;

    if(_this.endX - _this.disX > 30){
        _this.endjuli = _this.endjuli + speed * Math.abs(_this.endX - _this.disX) * 10;
        if(_this.endjuli > 0){
            _this.endjuli = 30;
            changespeed = 300;
        }else{
            changespeed = 1000;
        }
        _this.fnTranslate(changespeed, _this.endjuli);
    }else if(_this.disX - _this.endX > 30){
        _this.endjuli = _this.endjuli - speed * Math.abs(_this.endX - _this.disX) * 10;
        if(_this.endjuli < _this.maxWidth){
            _this.endjuli = _this.maxWidth - 30;
            changespeed = 300;
        }else{
            changespeed = 1000;
        }
        _this.fnTranslate(changespeed, _this.endjuli);
    }else{
        if (_this.time) {clearInterval(_this.time)};
    }
};
//轮播添加状态
MyTouch.prototype.fnActive = function() {
    var _this = this;

    if(_this.list && !_this.switchs){
        for (var i = 0, _thisListLiLength = _this.list.querySelectorAll("li").length; i < _thisListLiLength; i++) {
            _this.list.querySelectorAll("li")[i].className = "";
        }
        _this.list.querySelectorAll("li")[_this.index].className = "active";
    }

    _this.endjuli = -(_this.index * _this.width) - (_this.leftNum * _this.width);

    if(!_this.loop){
        _this.fnJudge();
    }

    _this.fnTranslate(300, _this.endjuli);
};
//判断回弹
MyTouch.prototype.fnJudge = function() {
    var _this = this;

    if(_this.endjuli > 0){
        _this.endjuli = 0;
    }
    if(_this.endjuli < _this.maxWidth){
        _this.endjuli = _this.maxWidth;
    }
};
//运动
MyTouch.prototype.fnTranslate = function(time, adm) {
    var _this = this;

    _this.oDiv.style.transitionTimingFunction = "ease-out";
    _this.oDiv.style.transitionDuration = time +"ms";
    _this.oDiv.style.transform = "translate3d("+ adm +"px, 0, 0)";
    _this.fnTransitionend(adm);
};
//index
MyTouch.prototype.fnJudgeIndex = function(what){
    var _this = this;

    if(_this.index != 0 && _this.loop){
        _this.loopLeft = false;
    }
    if(_this.index != _this.length && _this.loop){
        _this.loopRight = false;
    }

    if (!what){
        if(_this.index < 0){
            if (_this.loop){
                _this.index = _this.length;
            }else{
                _this.index = 0;
            }
        }
    }else{
        if(_this.index > _this.length){
            if (_this.loop){
                _this.index = 0;
            }else{
                _this.index = _this.length;
            }
        }
    }
    if($('.number')){
        $('.number').find('span').html(_this.index+1);
    }
    if(_this.index == 0 && _this.loop){
        _this.loopLeft = true;
    }
    if(_this.index == _this.length && _this.loop){
        _this.loopRight = true;
        // console.log(_this.loopRight);
    }
};
//自动轮播
MyTouch.prototype.fnAutomatic = function() {
    var _this = this;

    _this.setActive = setInterval(function () {
        _this.index ++;
        _this.touch = false;
        if(_this.index == _this.length + 1 && _this.loop){
            _this.oDiv.style.transitionDuration = 0 + "ms";
            _this.oDiv.style.transform = "translate3d(0px, 0, 0)";
        }
        setTimeout(function () {
            _this.fnJudgeIndex(true);
            _this.fnActive();
        }, 100);
    }, _this.speed);
};
//结束
MyTouch.prototype.fnTransitionend = function(_adm) {
    var _this = this;

    _this.oDiv.removeEventListener("transitionend", _this.transitionEnd, false);
    _this.transitionEnd = function () {
        if(_this.switchs){
            _this.endjuli = _adm;

            _this.fnJudge();

            _this.oDiv.style.transitionDuration = 200 + "ms";
            _this.oDiv.style.transform = "translate3d("+ _this.endjuli +"px, 0, 0)";

            clearInterval(_this.time);
        }
    }
    _this.oDiv.addEventListener("transitionend", _this.transitionEnd, false);
};