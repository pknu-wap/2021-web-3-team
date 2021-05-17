const id = document.querySelector("#id"),
    pw = document.querySelector("#password"),
    confirmpw = document.querySelector("#confirmpw"),
    nickname = document.querySelector("#nickname"),
    registerBtn = document.querySelector("button");


function validate() {
    var re = /^[a-zA-Z0-9]{4,12}$/

    if (!re.test(id.value)) {
        alert("아이디는 4~12자의 영문 대소문자와 숫자로만 입력");
        id.value = "";
        id.focus();
    }

    if (id.value == "") {
        alert("아이디를 입력해 주세요");
        id.focus();
        return false;
    }
    if (pw.value == "") {
        alert("비밀번호를 입력해 주세요");
        pw.focus();
        return false;
    }
    if (pw.value != confirmpw.value) {
        alert("비밀번호가 다릅니다. 다시 확인해 주세요.");
        confirmpw = "";
        confirmpw.focus();
        return false;
    }
    if (nickname.value == "") {
        alert("닉네임 입력해 주세요");
        nickname.focus();
        return false;
    }

}
registerBtn.addEventListener("click", validate);