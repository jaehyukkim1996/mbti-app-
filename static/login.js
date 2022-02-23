function return_home() {
    window.location.reload();
}

function login() {
    let inputemail = $("#email").val();
    let inputpassword = $("#password").val();
    $.ajax({
        type: "POST",
        url: "/authentication",
        data: { email: inputemail },
        success: function (response) {
            let dbpassword = response["msg"];
            if (dbpassword !== "not") {
                if (inputpassword == dbpassword) {
                    alert("login success");
                    $.ajax({
                        type: "POST",
                        url: "/loginsuccess",
                        data: { email: inputemail },
                        success: window.location.assign(
                            "http://localhost:8000/user"
                        ),
                    });
                } else {
                    alert("wrong password");
                }
            } else {
                alert("user does not exist");
            }
        },
    });
}

function register() {
    window.location.assign("http://localhost:8000/registration");
}
