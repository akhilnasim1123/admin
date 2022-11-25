
$(document).ready(function () {
    $('#form-checkout').submit(function (e) {
        e.preventDefault();


        var phone = $("[name='phone']").val();
        var name = $("[name='name']").val();
        var email = $("[name='email']").val();
        var address = $("[name='addresses']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var pincode = $("[name='pincode']").val();
        var value = $("[name='butt']").val();
        var discound_or_not = $("[name='check']").val();
        var coupen = $("[name='coupens']").val();
        console.log(coupen)

        if (phone === "" || name === "" || address === "" || city === "" || state === "" || pincode === "") {
            swal("Alert!", "All fields are mandatory!", "error");

        }
        else{
            $.ajax({

                url: "/cart/payment",
                data: $('#form-checkout').serialize(),
                method:'post',
                success: function (response) {
                    swal("Congratulations!","Your Order is Placed","success").then((value) => {
                        window.location.href = '/'
                    });
                    
                }
            });
        }

        

    })})