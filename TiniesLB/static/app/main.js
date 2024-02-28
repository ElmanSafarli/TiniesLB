function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
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
    const showButton = document.getElementById('showBlockButton');
    const hideButton = document.getElementById('hideBlockButton');
    const hiddenBlock = document.getElementById('hiddenBlock');
    loadCartData();

    function updateCartItemQuantity(itemId, quantity) {
        var cart = JSON.parse(localStorage.getItem('cart')) || {};
        cart[itemId].quantity = quantity;
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDisplay(cart);
    }

    function addToCart(itemId, itemName, itemPrice, selectedColor) {
        var cart = JSON.parse(localStorage.getItem('cart')) || {};
        if (cart[itemId]) {
            cart[itemId].quantity += 1;
        } else {
            cart[itemId] = {
                name: itemName,
                price: itemPrice,
                quantity: 1,
                selectedColor: selectedColor,
            };
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDisplay(cart);
    }

    function removeFromCart(itemId) {
        var cart = JSON.parse(localStorage.getItem('cart')) || {};
        delete cart[itemId];
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDisplay(cart);
    }

    function loadCartData() {
        var cart = JSON.parse(localStorage.getItem('cart')) || {};
        updateCartDisplay(cart);
    }

    function updateCartDisplay(cart) {
        var totalPriceElement = document.getElementById('total-price');
        var totalPrice = 0;
        var cartItemsList = document.getElementById('cart-products');

        cartItemsList.innerHTML = '';

        for (var itemId in cart) {
            var item = cart[itemId];
            var itemName = item.name;
            var itemPrice = item.price;
            var itemQuantity = item.quantity;
            var itemTotalPrice = itemPrice * itemQuantity;
            var selectedColor = item.selectedColor;

            var cartItemElement = document.createElement('div');
            cartItemElement.classList.add('cart-items-list', 'cart-product-item');
            cartItemElement.innerHTML = `
                <div class="cart-product-img"><img src="" alt="product"></div>
                <div class="cart-table">
                    <div class="inline-detail">
                        <div class="cart-product-company"> ${selectedColor ? `<div class="cart-product-color">Color: ${selectedColor}</div>` : ''}</div>
                        <button class="delete-cart-item-btn" data-cart-item-id="${itemId}"></button>
                    </div>
                    <div class="cart-product-title">${itemName}</div>
                </div>
                <div class="cart-product-price">$${itemPrice}</div>
                <div class="quantity-container cart-product-qty">
                    <button class="quantity-btn cart-decrement-btn" data-cart-item-id="${itemId}"></button>
                    <span class="quantity" id="cartCount_${itemId}">${itemQuantity}</span>
                    <button class="quantity-btn cart-increment-btn" data-cart-item-id="${itemId}"></button>
                </div>
                <div class="cart-product-total cart-product-item-price">$${itemTotalPrice}</div>
            `;
            cartItemsList.appendChild(cartItemElement);

            totalPrice += itemTotalPrice;
        }

        totalPriceElement.textContent = 'Total Price: $' + totalPrice;
    }

    document.querySelectorAll('.addToCartBtn').forEach(function (button) {
        button.addEventListener('click', function () {
            var itemId = button.getAttribute('data-menu-item');
            var itemName, itemPrice, itemColor;

            // Check if the button is on the product detail page
            var productDetail = button.closest('.product-info');
            if (productDetail) {
                itemName = productDetail.querySelector('.product-title-detail').textContent.trim();
                itemPrice = parseFloat(productDetail.querySelector('.product-price-detail').textContent.trim().replace('$', ''));

                // Check if the product has available colors
                var availableColors = productDetail.querySelectorAll('.detail-color');
                if (availableColors.length > 0) {
                    var selectedColor = productDetail.querySelector('.detail-color.selected');
                    if (selectedColor) {
                        itemColor = selectedColor.style.backgroundColor;
                    } else {
                        alert('Please select a color for the product.')
                        return;
                    }
                }
            } else {
                // Assume the button is on the all products page
                var productBox = button.closest('.product-box');
                itemName = productBox.querySelector('.sellers-box-title').getAttribute('data-menu-item-name');
                itemPrice = parseFloat(productBox.querySelector('.sellers-box-price').textContent.trim());
            }

            // Add to cart if both item name and price are valid
            if (itemName && itemPrice) {
                addToCart(itemId, itemName, itemPrice, itemColor);
            } else {
                console.error('Failed to add item to cart. Item name or price is missing.');
            }
        });
    });

    // Toggle selected class for color selection
    document.querySelectorAll('.detail-color').forEach(function (color) {
        color.addEventListener('click', function () {
            // Deselect other colors
            color.parentNode.querySelectorAll('.detail-color').forEach(function (otherColor) {
                otherColor.classList.remove('selected');
            });
            // Select the clicked color
            color.classList.add('selected');
        });
    });



    document.querySelector('.shopping-cart').addEventListener('click', function (event) {
        if (event.target.classList.contains('delete-cart-item-btn')) {
            var itemId = event.target.getAttribute('data-cart-item-id');
            removeFromCart(itemId);
        }
    });

    document.querySelector('.cart-items-list').addEventListener('click', function (event) {
        var target = event.target;
        if (target.classList.contains('cart-decrement-btn') || target.classList.contains('cart-increment-btn')) {
            var itemId = target.getAttribute('data-cart-item-id');
            var cart = JSON.parse(localStorage.getItem('cart')) || {};
            var currentQuantity = cart[itemId].quantity;
            if (target.classList.contains('cart-decrement-btn')) {
                if (currentQuantity > 1) {
                    updateCartItemQuantity(itemId, currentQuantity - 1);
                }
            } else {
                updateCartItemQuantity(itemId, currentQuantity + 1);
            }
        }
    });

    // function changeImage(imageSrc) {
    //     document.getElementById('mainImage').src = imageSrc;
    // }

    showButton.addEventListener('click', function () {
        hiddenBlock.style.display = 'block';
        // body.classList.add('blur-background');
    });

    hideButton.addEventListener('click', function () {
        hiddenBlock.style.display = 'none';
        // body.classList.remove('blur-background');
    });

});








