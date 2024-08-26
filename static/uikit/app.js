// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.getquerySelector('.alert')
let alertClose = document.getquerySelecto('.alert__close')

if( alertWrapper){
    alertClose.addEventListener('click', () =>
        alertWrapper.style.display = 'none'
    )
}