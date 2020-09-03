function showLoading(){
    let loadingDiv = document.getElementById("loading");
    if (loadingDiv.classList.contains('loading-hidden')){
        loadingDiv.classList.remove('loading-hidden');
        loadingDiv.classList.add('loading-show');
    }
}


function copyLink(){
    let textArea = document.getElementById("sharable-link");
    textArea.value = window.location.href;
    textArea.focus();
    textArea.select();
    document.execCommand("Copy");
    textArea.value = "Copied!";
}