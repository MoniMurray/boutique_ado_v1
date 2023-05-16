// get the value of the country field when the page loads and store it
// in a variable
let countrySelected = $('#id_default_country').val();
// the value will be an empty string if the first option from the list
// is selected, so to determine if that's selected we can use this as a boolean
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab74c');
};
// we want to capture the change event and every time that happens
// get the value of it (which choice is made)
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab74c');
    } else {
        $(this).css('color', '#000');
    }
});