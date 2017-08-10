$(document).ready(function () {

    $("#password").click(function () {

        Materialize.toast("The password must be greater than or equal to eight characters, and can not be just numeric.",3000);
    });

    $("#password_repeat").change(function () {
      var password_repeat = $(this).val();
      var password = $("#password").val();
      var message1 = "Password do not match, please try again.";
      if (password_repeat && (password_repeat !== password)){
          Materialize.toast(message1,4000);
      }
  });

    $("#password").change(function () {
        var password = $(this).val();
        var message1 = "The password must be greater than or equal to eight characters, and can not be just numeric." ;
        var message2 = "The password can not be just numeric.";
        var message3 = "The password must be greater than or equal to eight characters.";
        var regexPassword = /^([a-z]+[0-9]+)|([0-9]+[a-z]+).{8,15}/i;
        var regexNumber = /^\d*$/;
        if (password.match(regexNumber)){
            Materialize.toast(message2,4000);
        }
        else if ((password.length)< 8){
            Materialize.toast(message3, 4000);
        }
        else if (!(password.match(regexPassword))) {
            Materialize.toast(message1,4000);
        }
    });

});