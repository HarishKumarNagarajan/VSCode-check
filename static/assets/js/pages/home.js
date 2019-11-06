$(document).ready(function(){
    $("#AnchorProjects").click(function () {
        $("#box").load('{{url_for("project")}}');
    });
});