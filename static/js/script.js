function showLoading(){
    let loadingDiv = document.getElementById("loading");
    if (loadingDiv.classList.contains('loading-hidden')){
        loadingDiv.classList.remove('loading-hidden');
        loadingDiv.classList.add('loading-show');
    }
}