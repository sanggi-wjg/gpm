function jwt_decode(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
}

function get_cookie(name) {
    const value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value ? value[2] : null;
}

function delete_cookie(name) {
    document.cookie = encodeURIComponent(name) + '=; expires=0';
}

const TOKEN_KEY = "access_token"

function is_authenticated() {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token === '' || token === null) {
        return false;
    }

    try {
        const jwt = jwt_decode(token);
        const exp = jwt.exp;
        if (exp < (new Date().getTime() + 1) / 1000) {
            return false;
        }
    } catch (err) {
        console.log(err)
        return false;
    }
    return true;
}

function logout() {
    localStorage.removeItem(TOKEN_KEY);
    document.location.href = "/";
}

$(document).ready(function () {
    let token = localStorage.getItem(TOKEN_KEY)
    if (token === '' || token === null) {
        const token_cookie = get_cookie(TOKEN_KEY)
        if (token_cookie !== '') {
            delete_cookie(TOKEN_KEY)
            localStorage.setItem(TOKEN_KEY, token_cookie);
        }
    }
    if (is_authenticated()) {
        $("#btn_login").hide();
        $("#btn_logout").show();
    } else {
        $("#btn_login").show();
        $("#btn_logout").hide();
    }
});