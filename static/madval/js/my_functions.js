function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function move_messages(){
    await sleep(4.5 * 1000);
    try{
        var messages_div = document.getElementById("madval-messages");
        messages_div.classList.remove("madval-messages");
        messages_div.classList.add("move-to-corner");
    }
    catch{
        // do nothing
    }}

function close_messages(){
    var messages_div = document.getElementById("madval-messages");
    messages_div.style.display='none';
}

function open_comments(){
    document.getElementById("all_comments").style.display="block";
}
function close_comments(){
    document.getElementById("all_comments").style.display="none";
}
function open_anonymous_comments(){
    document.getElementById("all_anonymous_comments").style.display="block";
}
function close_anonymous_comments(){
    document.getElementById("all_anonymous_comments").style.display="none";
}

document.body.addEventListener('keydown', function(e) {
    if (e.key == "Escape") {
        close_comments()
        close_anonymous_comments()
    }
});
move_messages();