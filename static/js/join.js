function try_join() {
    const user_email = $("#user_email").val();
    const user_password1 = $("#user_password").val();
    const user_password2 = $("#user_password_check").val();
    const join_result = $("#join-result")

    if (user_email === "" || user_email === null) {
        join_result.html('Email 입력해주세요');
        return false;
    }
    if (user_password1 === "" || user_password1 === null) {
        join_result.html('비밀번호 입력해주세요');
        return false;
    }
    if (user_password2 === "" || user_password2 === null) {
        join_result.html('비밀번호 입력해주세요');
        return false;
    }
    if (user_password1 !== user_password2) {
        join_result.html('비밀번호가 서로 불일치 합니다.');
        return false;
    }

    $.ajax({
        method: "POST",
        url: "/api/v1/users",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            'email': user_email,
            'password1': user_password1,
            'password2': user_password2,
        })
    }).done(function (response_json) {


    }).fail(function (xhr, status, errorThrown) {
        const fail_json = xhr.responseJSON;
        const details = fail_json.detail;

        let html = '';
        $.each(details, function (_, detail) {
            html += `${detail.loc[1]}: ${detail.msg}<br>`;
        });
        join_result.html(html);
    });
}