function trashCart(itemId,total){
    console.log(itemId);

    $.ajax({
        method:'get',
        url: "/cart/deletecart/"+itemId,
        success: function (response) {
            console.log(response);
                console.log(document.getElementById('cart-user'+itemId));
                document.getElementById(itemId).remove()
                if (response.count != 0){
                document.getElementById('carttotalprice').innerHTML = response.total
                document.getElementById('totalquantity').innerHTML = response.count     
            }else{
                location.reload()
            }
        }
    });
}


function wishlist(productId,userId){
    console.log(userId);
    $.ajax({
        method:'get',
        url: "/add-wishlist/"+productId+"/"+userId,
        success: function (response) {
            console.log(response)
            
            if (response == 'added'){
                // document.getElementsByClassName('bi bi-heart text-danger') = 'fa fa-heart'
                $('a i').removeClass('bi bi-heart');
                $('a i').addClass('fa fa-heart');

            }
            else{
                $('a i').removeClass('fa fa-heart ');
                $('a i').addClass('bi bi-heart');
                document.getElementById('user-side-wishlist').remove()
                
            }
        }
    });
}
function addressTrash(addressId,userId){
    $.ajax({
        url: "/delete-address/"+addressId+"/"+userId,
        method:"get",
        success: function (response) {
            console.log(response)
            document.getElementById('address-of-user').remove()
        }
    });

}

function displayOrder(){
    console.log('orderes');
    document.getElementById('user-orders').classList.remove('hidden')
    document.getElementById('user-profile').classList.add('hidden')
    document.getElementById('user-wishlist').classList.add('hidden')
}
function displayWishlist(){
    console.log('orderes');
    document.getElementById('user-orders').classList.add('hidden')
    document.getElementById('user-profile').classList.add('hidden')
    document.getElementById('user-wishlist').classList.remove('hidden')
}
function displayProfile(){
    console.log('orderes');
    document.getElementById('user-orders').classList.add('hidden')
    document.getElementById('user-profile').classList.remove('hidden')
    document.getElementById('user-wishlist').classList.add('hidden')
}