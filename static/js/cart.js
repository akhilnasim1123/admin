var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId", productId, "action", action, "");

    console.log("USER:", user);
    updateUserOrder(productId, action);

  });
}
function updateUserOrder(productId, action) {
  console.log("User is Logged in, sending data..?");
  console.log(action + "dsfajhdfasdja");

  var url = "/cart/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },

    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      console.log(response);
     


      return response.json();
      // location.reload()
    })
    .then((data) => {
      console.log("data:", data);
      console.log(',op gh ty r')
      
      // location.reload()
      // location.reload()
    });
}

function increaseValue(button, id, limit, price) {
  const numberInput = button.parentElement.querySelector(".number");
  var value = parseInt(numberInput.innerHTML, 10);
  if (isNaN(value)) value = 0;
  if (limit && value >= limit) return;
  numberInput.innerHTML = value + 1;
  updateUserOrder(id, "add");
  let currenttotp = document.getElementById(id).innerHTML;
  let newcurrentp = parseFloat(currenttotp);
  let newprice = newcurrentp + parseFloat(price);
  document.getElementById(id).innerHTML = newprice;
  let totalquantity = document.getElementById("totalquantity").innerHTML;
  let newtotalquantity = parseInt(totalquantity) + 1;
  document.getElementById("totalquantity").innerHTML = newtotalquantity;
  let cartotalprice = document.getElementById("carttotalprice").innerHTML;
  let newtotalprice = parseFloat(cartotalprice) + parseFloat(price);
  document.getElementById("carttotalprice").innerHTML = newtotalprice;
  let cartr= Number(document.getElementById('cart-total-ppp').innerHTML)

  document.getElementById('cart-total-ppp').innerHTML = cartr + 1
 

}

function decreaseValue(button, id, limit, price) {
  console.log(limit + "this is the stock left ");
  const numberInput = button.parentElement.querySelector(".number");
  var value = parseInt(numberInput.innerHTML, 10);
  if (isNaN(value)) value = 0;
  if (value < 2) return;
  numberInput.innerHTML = value - 1;
  updateUserOrder(id, "remove");
  let currenttotp = document.getElementById(id).innerHTML;
  let newcurrentp = parseFloat(currenttotp);
  let newprice = newcurrentp - parseFloat(price);
  document.getElementById(id).innerHTML = newprice;
  let totalquantity = document.getElementById("totalquantity").innerHTML;
  let newtotalquantity = parseInt(totalquantity) - 1;
  document.getElementById("totalquantity").innerHTML = newtotalquantity;
  let cartotalprice = document.getElementById("carttotalprice").innerHTML;
  let newtotalprice = parseFloat(cartotalprice) - parseFloat(price);
  document.getElementById("carttotalprice").innerHTML = newtotalprice;
  document.getElementById('cart-total-ppp').innerHTML -= 1 
}
function addToCart(){
    let cartr= Number(document.getElementById('cart-total-ppp').innerHTML)
    document.getElementById('cart-total-ppp').innerHTML  = cartr + 1
}