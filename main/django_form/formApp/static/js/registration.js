$("#register").click(function(){
    register()
});


function register(){
    var email = $("#email").val();
    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    // var username = $("#username").val();
    var password = $("#password").val();
    var confirm_password =  $("#Repeat_your_password").val();
    $.ajax({
   
        url: '/api/register/',
        type: "POST",
        dataType: "json",
        data: {
            email:email,
            first_name:first_name,
            last_name:last_name,
            // username:username,
            password:password,
            confirm_password:confirm_password
        },
        success: function (data){
          alert("Data has been stored successfully");
          $('#signup_id').hide();
          $('#signin_id').show();
        },
        error: function(error){
            alert("invalid input");
        },
    });
   
}


$("#login_id").click(function(){
    var email = $("#typeEmailX").val();
    var password = $("#typePasswordX").val();
    $.ajax({
        url: '/api/login/',
        type: "POST",
        dataType: "json",
        data: {
            email:email,
            password:password,
        },
        success: (data) => {
            alert("login successfull");
            tokens_save_localStorage(data)
            window.location = "/"

        },
        error: (error) => {
            alert("user is not authenticated");
        },
    });

});



