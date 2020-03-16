function submit(vaptchaObj){
    $.ajax({
        url:"/submit",
        data:{
            name: $("#name")[0].value,
            contact: $("#contact")[0].value,
            content: $("#content")[0].value,
            token: vaptchaObj.getToken()
        },
        type: "POST",
        dataType: "JSON"
    }).done(
        function(json){
            if(json["status"]==="success"){
                M.toast({html:"Submit Success"});
                $("#name")[0].value=$("#contact")[0].value=$("#content")[0].value="";
                vaptchaObj.reset();
            }
            else{
                vaptchaObj.reset();
                M.toast({html:json['message']});
            }
        }
    )
}

function vaptcha_init(){
    vaptcha({
        vid: '5e3ace29587395e501f50442',
        type: 'invisible',
        scene: 2,
        offline_server: 'no-offline_server'

}).then(function (vaptchaObj) {
    obj = vaptchaObj;
    vaptchaObj.listen('pass', function() {
        submit(obj)
  });
    //关闭验证弹窗时触发
    vaptchaObj.listen('close', function() {
        vaptchaObj.reset();
    })
})
}

$(function(){
    vaptcha_init();
    $('#send_content').on('submit',function(e){
        e.preventDefault();
        obj.validate();
    })
});