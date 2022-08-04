function try_login() {
    const user_email = $("#user_email").val();
    const user_password = $("#user_password").val();
    const login_result = $("#login-result");

    if (user_email === "" || user_email === null) {
        login_result.html("Email 입력해주세요");
        return false;
    }
    if (user_password === "" || user_password === null) {
        login_result.html("Password 입력해주세요");
        return false;
    }

    $.ajax({
        method: "POST",
        url: "/token",
        dataType: "json",
        data: {
            'username': user_email,
            'password': user_password,
        }
    }).done(function (response_json) {
        localStorage.setItem(TOKEN_KEY, response_json.access_token);
        document.location.href = "/";

    }).fail(function (xhr, status, errorThrown) {
        alert('login failed');
    });
}