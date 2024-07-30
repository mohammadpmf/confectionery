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

move_messages();