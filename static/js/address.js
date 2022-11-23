function addressSelection(addressId){
    console.log(addressId);

    $.ajax({
        url: "/cart/addressSelect/"+addressId,
        method:'get',
        success: function (response) {
            console.log(response.name);
            document.getElementById('name-test').value= response.name
            document.getElementById('phone').value = response.phone
            document.getElementById('address-es').value = response.address
            document.getElementById('city').value = response.city
            document.getElementById('state').value= response.state
            document.getElementById('pincode').value= response.pincode
            
            
        }
    });

}