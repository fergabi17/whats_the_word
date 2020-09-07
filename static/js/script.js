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


function showEdit(){
    let editDiv = document.querySelector("#edit_participants");
    let showBtn = document.querySelector("#show-edit");
    if(editDiv.classList.contains('edit-hide')){
        editDiv.classList.remove('edit-hide');
        editDiv.classList.add('edit-show');
        showBtn.innerHTML = "Hide"

    } else {
        editDiv.classList.remove('edit-show');
        editDiv.classList.add('edit-hide');
        showBtn.innerHTML = "Update Names"
    }

}