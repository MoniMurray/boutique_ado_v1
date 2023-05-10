// get the stripe public key and client secret from the template using jQuery

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);

// in order to set up Stripe, create a var using our stripe public key

var stripe = Stripe(stripe_public_key);

// now use it to create an instance of stripe elements

var elements = stripe.elements();

// use it to create a card element

var style = {
    base: {
        color: '#000',
        fontWeight: '500',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSize: '16px',
        fontSmoothing: 'antialiased',
            '::placeholder': {
                color: '#aab7c4',
            },
    },
    invalid: {
        iconColor: '#dc3545',
        color: '#dc3545',
    },
    };

    var card = elements.create('card', {style: style});

    // and finally mount the card element to the div in Fieldset 3 'User's Payment Information'

    card.mount('#card-element');

