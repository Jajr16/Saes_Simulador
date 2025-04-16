var buttons = document.querySelectorAll('.button-detail');

buttons.forEach(button => {
    button.addEventListener("click", function() {
        var detailRow = this.parentElement.parentElement.nextElementSibling;

        if (detailRow.style.display == "none" || detailRow.style.display === "") {
            detailRow.style.display = "table-row";
        } else {
            detailRow.style.display = "none";
        }
    })    
});