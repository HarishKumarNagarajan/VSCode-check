var varTable;
$(document).ready(function () {
    $("#tbl_courses").dataTable().fnDestroy();
    LoadTable(); 
    LoadPracticeddl();
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 3 || role_id == 8)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_courses").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/course_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.course_id = 0;
                d.project_id = $('#ddlProject option:selected').val();
                d.practice_id = $('#ddlPractice option:selected').val();
            },
            error: function (e) {
                $("#tbl_courses tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Course_Name" },
            { "data": "Practice_Name" },
            { "data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            },
            {
            "data": function (row, type, val, meta) {
            var varButtons = ""; 
            if(role_id != 3 && role_id != 8)
                varButtons += '<a onclick="EditCourseDetail(\'' + row.Course_Id + '\',\'' + row.Practice_Id + '\',\'' + row.Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
            return varButtons;
            }
            }
        ],


    });
}
function EditCourseDetail(CourseId,PracticeId,ProjectId)
{
    $('#hdn_course_id').val(CourseId);
    $('#form1').submit(); 
    
}

function LoadPracticeddl()
{
    var URL=$('#hdn_web_url').val()+ "/AllPracticeList"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Pratices != null)
            {
                $('#ddlPractice').empty();
                var count=data.Pratices.length;
                if( count> 0)
                {
                    $('#ddlPractice').append(new Option('ALL','0'));
                    for(var i=0;i<count;i++)
                        $('#ddlPractice').append(new Option(data.Pratices[i].Practice_Name,data.Pratices[i].Practice_Id));
                }
                else
                {
                    $('#ddlPractice').append(new Option('ALL','0'));
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

function LoadProjectddl(PracticeId)
{
    var URL=$('#hdn_web_url').val()+ "/AllProjectsBasedOnPractice"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,       
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json", 
        data:{
            "practice_id": PracticeId,
            "project_id" : $('#ddlProject option:selected').val()
        },
        success: function (data){
            if(data.Projects != null)
            {
                $('#ddlProject').empty();
                var count=data.Projects.length;
                if( count> 0)
                {
                    $('#ddlProject').append(new Option('ALL','0'));
                    for(var i=0;i<count;i++)
                        $('#ddlProject').append(new Option(data.Projects[i].Project_Name,data.Projects[i].Project_Id));
                }
                else
                {
                    $('#ddlProject').append(new Option('ALL','0'));
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
    $("#tbl_courses").dataTable().fnDestroy();
    LoadTable(); 
}