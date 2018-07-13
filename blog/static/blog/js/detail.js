function tagFunction(){
    if ($("#addtag").is(":hidden")){
        $("#addtag").css("display","");
    }else{
        $("#addtag").css("display","none");
    }

}

function replyformFunction(id){
    if ($("#replyform"+id).is(":hidden")){
        $("#replyform"+ id).css("display","");
    }
    else{
        $("#replyform"+ id).css("display","none")
    }
}
function showreplyFunction(comment_id, max){
    var i;
    if ($("#reply"+comment_id+"_4").is(":hidden")){
        for(i=4;i<=max;i++){
            $("#reply"+comment_id+"_"+i).css("display","");
        }
        $("#showreply"+comment_id).text("Show less");
    }
    else{
        for(i=4;i<=max;i++){
            $("#reply"+comment_id+"_"+i).css("display","none");
        }
        $("#showreply"+comment_id).text("Show more");
    }
}


