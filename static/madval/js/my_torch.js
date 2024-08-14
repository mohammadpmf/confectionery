var torch = document.getElementById("torch");
var body = document.getElementsByTagName("body")[0]
var lamp = true;
body.onmousemove = function move(e){
    var x = e.clientX;
    var y = e.clientY;
    var width = torch.offsetWidth;
    var height = torch.offsetHeight;
    torch.style.left = x-width/2+'px';
    torch.style.top = y-height/2+'px';
};
body.onclick = function(){
    lamp = !lamp;
    torch.style.display=(lamp == true? 'block' : 'none');
}
body.addEventListener("dblclick", function(e) {
    body.style.background="#c7fbff";
}, false);
body.addEventListener('click', function (evt) {
    if (evt.detail === 3) {
        body.style.background="#232323";
    }
});

body.addEventListener("keypress", myFunction);
function myFunction(e) {
    var zoom;
    if(e.key=="+")
        zoom=10;
    else if(e.key=="-")
        zoom=-10;
    var x = e.clientX;
    var y = e.clientY;
    if (lamp){ // یه باگی داشت که وقتی چراغ رو خاموش میکردی و + رو میزدی سایزش صفر میشد. برای رفع این باگ این قسمت رو نوشتم.
        var width = torch.offsetWidth;
        var height = torch.offsetHeight;
    }
    width += zoom;
    height += zoom;
    torch.style.width=width+'px';
    torch.style.height=height+'px';
    torch.style.left = x-width/2+'px';
    torch.style.top = y-height/2+'px';
}

document.onload = setTimeout(function () { alert(
"به بخش درباره من خوش اومدید. اگه استفاده از چراغ قوه براتون سخته، با دابل کلیک کردن\
 میتونید چراغ این بخش رو روشن کنید. اگه براتون جالب بود و خواستید چراغ این بخش رو خاموش\
 کنید، تریپل کلیک کنید. (سه بار کلیک پشت سر هم) اگه هم از چراغ قوه خوشتون اومده\
 و میخواید باهاش بازی کنید😊، باید ماوس رو تو صفحه حرکت بدید که\
 مکان مورد نظر رو براتون روشن کنه. خاموش و روشن کردن خود چراغ قوه هم که با کلیک اتفاق میفته.\
 اگه خواستید چراغ قوه سطح بیشتر یا کمتری از صفحه رو روشن کنه، + و - رو روی کیبوردتون بزنید.\
امیدوارم از خووندن این بخش لذت ببرید. موفق باشید."
); }, 500);