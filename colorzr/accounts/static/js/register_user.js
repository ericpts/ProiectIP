function getUsername() {
    return $("input#username").val();
}

function getPassword() {
    return $("input#password").val();
}

function getEmail() {
    return $("input#email").val();
}

function createUser(event) {
    event.preventDefault();
   

    var formData = {
        "username": getUsername(),
        "password": getPassword(),
        "email": getEmail()
    };
    
    console.log(formData);
    alert(formData.username);

    $.ajax({
        url: "/auth/users/create/",
        headers: {"X-CSRFToken": "csrftoken"},
        success: (data) => {
            alert(data);
        },
        data: formData,
        method: 'POST'
    });
}