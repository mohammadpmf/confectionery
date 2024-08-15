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
"\
به بخش درباره من خوش اومدید.\n\
با کلیک کردن، میتونید چراغ قوه رو خاموش و روشن کنید.\n\
با - و + هم میتونید شعاعش رو کم و زیاد کنید.\n\
اگه مطالعه با چراغ قوه براتون سخته، با دابل کلیک میتونید لامپ این بخش رو روشن کنید.\n\
اگه خواستید لامپ رو خاموش کنید، تریپل کلیک کنید.\n\
موفق باشید.\
"
); }, 500);
