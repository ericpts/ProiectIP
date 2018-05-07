function getUsername() {
    return $("input#username").val();
}

function getPassword() {
    return $("input#password").val();
}

function createUser(event) {
    event.preventDefault();
   

    var formData = {
        "username": getUsername(),
        "password": getPassword()
    };
    
    console.log(formData);
    alert(formData.username);
    alert(formData.password);

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