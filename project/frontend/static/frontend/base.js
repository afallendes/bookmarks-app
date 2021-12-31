// Helpers
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);
const $$$ = (a) => Array.from(a)

// Apply Bootstrap's form-control class to form's search input
$('#id_search').classList.add('form-control')
