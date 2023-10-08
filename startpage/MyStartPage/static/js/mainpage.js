function save_settings() {
    fetch('/save_settings/').then();
}

function save_and_go(url){
    fetch('/save_settings/').then(response => {
            window.location.href = url;
    });
}

function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;

    document.getElementById('clock').innerHTML = timeString;
}

window.onbeforeunload = save_settings;

setInterval(updateClock, 250);
updateClock();