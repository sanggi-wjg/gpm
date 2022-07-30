function move_page_scroll(obj, offset_delta = 100) {
    const offset = obj.offset();
    $("html, body").animate({scrollTop: offset.top - offset_delta}, 200);
}

function show_tech_stacks(tech_categories) {
    let html = `<div class="row justify-space-between py-2">`;
    // tech categories
    $.each(tech_categories, function (_, category) {
        // console.log(category);
        html += `<div class="info">
                    <h5 class="text-white">${category.name}</h5>
                 </div>`
        // tech stacks
        $.each(category.tech_stacks, function (_, stack) {
            // console.log(stack);
            html += `<button type="button" class="btn bg-gradient-light w-auto me-2 btn-tech-stack"
                            onclick="choose_tech_stacks($(this))"
                            data-user-choose="0"
                            data-tech-category-name="${category.name}"
                            data-tech-stack-color="${stack.color}"
                            data-tech-stack-name="${stack.name}">${stack.name}</button>`
        });
        // console.log("=============");
    });
    html += '</div>';
    // print
    const tech_stack = $("#tech_stack");
    tech_stack.append(html)
}

function choose_tech_stacks(btn_teck_stack) {
    // $(".btn-tech-stack").click(function () {
    // console.log(btn_teck_stack);
    if (btn_teck_stack.attr("data-user-choose") === "0") {
        btn_teck_stack.attr("class", "btn bg-gradient-primary w-auto me-2 btn-tech-stack");
        btn_teck_stack.attr("data-user-choose", "1");
    } else {
        btn_teck_stack.attr("class", "btn bg-gradient-light w-auto me-2 btn-tech-stack");
        btn_teck_stack.attr("data-user-choose", "0");
    }
}


function get_user_socials() {
    let social_sites = [
        $("#social_tistory"),
        $("#social_github"),
        $("#social_naver_blog"),
        $("#social_instagram")
    ];

    let socials = [];
    $.each(social_sites, function (_, site) {
        if (site.val() !== '') {
            socials.push({
                site_name: site.parent().children('label').text(),
                site_url: site.parent().children('span').text(),
                site_user_name: site.val(),
            })
        }
    });
    return socials;
}

function get_techs() {
    let techs = [];
    $(".btn-tech-stack[data-user-choose=1]").each(function (_, btn) {
        techs.push({
            tech_category_name: $(this).attr('data-tech-category-name'),
            tech_stack_name: $(this).attr('data-tech-stack-name'),
            tech_stack_color: $(this).attr('data-tech-stack-color')
        })
    })
    return techs;
}


function save_markdown() {
    const UserMarkdownCreateForm = {
        user_github_name: $("#user_github_name").val(),
        user_introduction: $("#user_introduction").val(),
        user_socials: get_user_socials(),
        user_techs: get_techs(),
    }
    if (UserMarkdownCreateForm.user_github_name === "") {
        move_page_scroll($("#user_github_name"))
        return false;
    }
    // console.log(UserMarkdownCreateForm)

    $.ajax({
        method: "POST",
        url: "/api/v1/markdowns",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(UserMarkdownCreateForm),
        xhrFields: {
            responseType: "blob",
        },
    }).done(function (blob, status, xhr) {
        console.log(blob, status, xhr);
        let fileName = "";
        const disposition = xhr.getResponseHeader("Content-Disposition");

        if (disposition && disposition.indexOf("attachment") !== -1) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) {
                fileName = decodeURI(matches[1].replace(/['"]/g, ""));
            }
        }
        const URL = window.URL || window.webkitURL;
        const downloadUrl = URL.createObjectURL(blob);

        if (fileName) {
            const a = document.createElement("a");
            if (a.download === undefined) {
                window.location.href = downloadUrl;
            } else {
                a.href = downloadUrl;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
            }
        } else {
            window.location.href = downloadUrl;
        }
    }).fail(function (xhr, status, errorThrown) {
        alert("fail to download markdown");
    });
}

$(document).ready(function () {
    const user_introduction = document.getElementById("user_introduction");
    user_introduction.value = `👍 Python 백엔드 개발자에요
🌱 Backend 개발에 대해서 공부하고 있어요
✨ FastAPI 같은 최신 기술에 관심 있어요
🤝 같이 미니 프로젝트 참여하실 분을 찾고 있어요`;

    $.ajax({
        method: "GET",
        url: "/api/v1/tech-categories",
        dataType: "json",
    }).done(function (response_json) {
        show_tech_stacks(response_json);
    }).fail(function (xhr, status, errorThrown) {
        $("#tech_stack").append(`<div class="alert alert-danger" role="alert"><strong>failed fetch tech category</div>`)
    });
});