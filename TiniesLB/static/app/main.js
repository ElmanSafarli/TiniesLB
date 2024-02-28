const showButton = document.getElementById('showBlockButton');
const hideButton = document.getElementById('hideBlockButton');
const hiddenBlock = document.getElementById('hiddenBlock');
const body = document.body;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const productButtons = document.querySelectorAll('.add-to-cart-btn');
    const sessionID = "{{ request.session.session_key }}"; // Get the session ID from the server-side template
    const cartTotal = document.getElementById('cart-total');
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const quantityButtons = document.querySelectorAll('.quantity-btn');

    // Function to get CSRF token from cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }


    // Function to update quantity and total price
    function updateQuantityAndTotal(button, type) {
        const quantityElement = button.parentElement.querySelector('.quantity');
        const currentQuantity = parseInt(quantityElement.textContent);

        let newQuantity = currentQuantity;
        if (type === 'increase') {
            newQuantity++;
        } else if (type === 'decrease' && newQuantity > 1) {
            newQuantity--;
        }

        quantityElement.textContent = newQuantity;

        const productPrice = parseFloat(button.closest('.cart-product-item').querySelector('.cart-product-item-price').dataset.productPrice);
        const newProductTotalPrice = productPrice * newQuantity;
        const productTotalPriceElement = button.closest('.cart-product-item').querySelector('.cart-product-item-price');
        productTotalPriceElement.textContent = `$${newProductTotalPrice.toFixed(2)}`;

        const currentCartTotal = parseFloat(cartTotal.textContent.replace('$', ''));
        const newCartTotal = currentCartTotal + (newProductTotalPrice - (productPrice * currentQuantity));
        cartTotal.textContent = `$${newCartTotal.toFixed(2)}`;
    }

    quantityButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            updateQuantityAndTotal(button, button.dataset.type);

            // Update localStorage with the new quantity
            const productId = button.closest('.cart-product-item').querySelector('.delete-btn').dataset.productId;
            const quantity = parseInt(button.parentElement.querySelector('.quantity').textContent);
            localStorage.setItem(`cart_${productId}`, quantity.toString());
        });
    });

    // Function to get stored quantity from localStorage
    function getStoredQuantity(productId) {
        const storedQuantity = localStorage.getItem(`cart_${productId}`);
        return storedQuantity ? parseInt(storedQuantity) : 1; // Default to 1 if not found
    }

    // Set initial quantities from localStorage on page load
    quantityButtons.forEach(button => {
        const productId = button.closest('.cart-product-item').querySelector('.delete-btn').dataset.productId;
        const storedQuantity = getStoredQuantity(productId);
        button.parentElement.querySelector('.quantity').textContent = storedQuantity;
    });

    productButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Get the product ID from the clicked button
            const productId = button.dataset.productId;
            const quantity = getStoredQuantity(productId);

            // Send an AJAX request to add the product to the cart
            fetch(`/add-to-cart/${productId}/?quantity=${quantity}&session_id=${sessionID}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
                },
                body: JSON.stringify({ quantity }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Handle success, you may show a notification or update the UI
                        console.log('Product added to cart successfully!');
                    } else {
                        // Handle failure
                        console.error('Failed to add product to cart.', data.message || 'Unknown error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                })
                .finally(() => {
                    // Optional: Perform any cleanup or additional actions
                });
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const productId = button.dataset.productId;
            const productPrice = parseFloat(button.closest('.cart-product-item').querySelector('.cart-product-item-price').dataset.productPrice);
            const quantity = parseInt(button.closest('.cart-product-item').querySelector('.quantity').textContent);

            // Send an AJAX request to remove the product from the cart
            fetch(`/remove-from-cart/${productId}/?quantity=${quantity}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Remove the product from the cart visually
                        button.closest('.cart-product-item').remove();

                        // Update the cart total in the HTML
                        const currentCartTotal = parseFloat(cartTotal.textContent.replace('$', ''));
                        const productTotalPrice = productPrice * quantity;
                        const newCartTotal = currentCartTotal - productTotalPrice;
                        cartTotal.textContent = `$${newCartTotal.toFixed(2)}`; // Limit to 2 decimal places
                    } else {
                        console.error('Failed to remove product from cart.', data.message || 'Unknown error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });

});


function changeImage(imageSrc) {
    document.getElementById('mainImage').src = imageSrc;
}





showButton.addEventListener('click', function () {
    hiddenBlock.style.display = 'block';
    // body.classList.add('blur-background');
});

hideButton.addEventListener('click', function () {
    hiddenBlock.style.display = 'none';
    // body.classList.remove('blur-background');
});