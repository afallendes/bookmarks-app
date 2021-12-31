// Helpers
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);
const $$$ = (a) => Array.from(a);


// Apply Bootstrap's classes to form elements
const formElements = ['username', 'password'];
formElements.forEach(e => {
    $(`#id_${e}`).classList.add('form-control');
    $(`label[for=id_${e}]`).classList.add('form-label');
});
