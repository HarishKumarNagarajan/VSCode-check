var varTable;
$(document).ready(function () {
    $('.dropdown-search-filter').select2();
    $("#tbl_candidate").dataTable().fnDestroy();
    LoadTable();
    LoadCourseddl(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    var course_id=$('#ddlCourse').val();
    var course_selected="",data='';
    var count;
    console.log(course_id.length);
    if (course_id == ""){
        course_selected='';
    }
    else{
        count=course_id.length;
        for (var i=0;i<count;i++){
            data+='{"course_id":'+ course_id[i]+'},';            
        }
        data=data.substring(0,data.length-1);
        data='['+data+']';
        course_selected=data;
    }
    console.log(course_selected);
    vartable1 = $("#tbl_candidate").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/candidate_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.candidate_id = 0;
                d.course_id = course_selected;
            },
            error: function (e) {
                $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Candidate_Id"},
            { "data": "Candidate_Name"},
            { "data": "Mobile_Number"},
            { "data": "Course_Name"}
            // {
            // "data": function (row, type, val, meta) {
            // var varButtons = ""; 
            // if(role_id != 5)
            //     varButtons += '<a onclick="EditCenterTypeDetail(\'' + row.Candidate_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
            // return varButtons;
            // }
            // }
        ],


    });
}
function EditCandidateDetail(CandidateId)
{
    $('#hdn_candidate_id').val(CandidateId);
    $('#form1').submit();
    
}
function LoadCourseddl()
{
    //alert("course_section");
    var URL=$('#hdn_web_url').val()+ "/AllCourseList"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Courses != null)
            {
                $('#ddlCourse').empty();
                var count=data.Courses.length;
                if( count> 0)
                {
                    $('#ddlCourse').append(new Option('Choose Course','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCourse').append(new Option(data.Courses[i].Course_Name,data.Courses[i].Course_Id));
                }
                else
                {
                    $('#ddlCourse').append(new Option('Choose Course','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}

function LoadTableBasedOnSearch(){
    
    $("#tbl_candidate").dataTable().fnDestroy();
    LoadTable(); 
}