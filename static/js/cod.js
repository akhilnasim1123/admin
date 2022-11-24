
$(document).ready(function () {
    $('#form-checkout').submit(function (e) {
        e.preventDefault();


        var phone = $("[name='phone']").val();
        var name = $("[name='name']").val();
        var email = $("[name='email']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var pincode = $("[name='pincode']").val();
        console.log(email)

        if (phone == "" || name == "" || address == "" || city == "" || state == "" || pincode == "") {
            swal("Alert!", "All fields are mandatory!", "error");

            return false;
        }
        else{
            return true;
        }
    })})