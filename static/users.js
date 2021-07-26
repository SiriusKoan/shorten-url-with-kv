function send_remove(user_id) {
    $.ajax({
        url: "/manage_user_backend",
        type: "delete",
        data: JSON.stringify({ "user_id": user_id }),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                add_msg("OK.", "success");
            }
            else {
                add_msg(r.responseText.split(";")[1], "alert");
            }
        })
}

function send_update(element) {
    var parent = element.parentElement.parentElement;
    var user_id = parseInt(parent.children[0].innerText);
    var username = parent.children[1].children[0].value;
    var email = parent.children[2].children[0].value;
    var is_admin = parent.children[3].children[0].checked;
    var verify_code = parent.children[4].children[0].value;
    var api_key = parent.children[5].children[0].value;
    var password = parent.children[7].children[0].value;
    // validate username
    if (username.length < 4 || username.length > 30) {
        add_msg("The name should be 4 to 30 letters long.");
        return;
    }
    // validate password
    if (password != "") {
        if (password.length < 6) {
            add_msg("The password must contain at least 6 characters.", "alert");
            return;
        }
        else {
            data.password = password;
        }
    }
    var data = { "user_id": user_id, "username": username, "email": email, "is_admin": is_admin, "verify_code": verify_code, "api_key": api_key, "password": password }
    $.ajax({
        url: "/manage_user_backend",
        type: "patch",
        data: JSON.stringify(data),
        dataType: "json",
    })
        .always(function (r) {
            if (r.status == 200) {
                add_msg("OK.", "success");
            }
            else {
                add_msg(r.responseText.split(";")[1], "alert");
            }
        })
}