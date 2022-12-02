$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();


        var phone = $("[name='phone']").val();
        var name = $("[name='name']").val();
        var email = $("[name='email']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        console.log(email)

        if (phone == "" || name == "" || address == "" || city == "" || state == "" || pincode == "") {
            swal("Alert!", "All fields are mandatory!", "error");

            return false;
        }


        else {
            $.ajax({
                type: "GET",
                url: "/cart/razorpay",

                success: function (response) {

                    var options = {
                        "key": "rzp_test_JgN88azXlg3vAo", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Torque.in",
                        "description": "Thank You For Buying From us",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responses) {
                            alert(responses.razorpay_payment_id);
                            data = {
                                "name": name,
                                "phone": phone,
                                "address": address,
                                "city": city,
                                "state": state,
                                "pincode": pincode,
                                "payment_mode": "Paid by Razorpay",
                                "payment_id": responses.razorpay_payment_id,
                                csrfmiddlewaretoken: token,

                            }
                            $.ajax({
                                type: "POST",
                                url: "/cart/payment",
                                data: data,
                                success: function (responseb) {
                                    swal("Congratulations!", "Your Order is Placed", "success").then((value) => {
                                        window.location.href = '/'
                                    });
                                }
                            });
                        },
                        "prefill": {
                            "name": name,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.on('payment.failed', function (response) {
                        alert(response.error.code);
                    });

                    rzp1.open();
                }
            });
        }
    });
});