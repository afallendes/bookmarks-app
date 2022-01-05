$(document).ready(function() {
    // Add Bootstrap's form-control class to all visible 'input' elements
    $('input:not([type=hidden]):not([type=test])').addClass('form-control');
    
    // Add custom bootstrap-multiselect to all 'select' elements
    $("select[multiple]").bsMultiSelect();
});
