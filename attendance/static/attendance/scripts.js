function showPage(page) {
    document.querySelectorAll('.page').forEach(div => {
        div.style.display = 'none';
    })
    document.querySelector(`#${page}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.page_button').forEach(button => {
        button.onclick = function() {
            showPage(this.dataset.page);
        }
    });
});