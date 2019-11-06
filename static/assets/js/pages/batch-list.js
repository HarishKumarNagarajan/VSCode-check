var varTable;
$(document).ready(function () {
    var Course=0,Batch=0;
    $("#tbl_batchs").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 2 || role_id == 7 || role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_batchs").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/batch_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.batch_id = 0;
            },
            error: function (e) {
                $("#tbl_batchs tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id != 2 && role_id != 7 && role_id != 5)
                    varButtons += '<a onclick="EditBatchDetail(\'' + row.Batch_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User" class="fas fa-edit" ></i></a><a onclick="MapCandidateBatch('+row.Course_Id+','+row.Center_Id+','+row.Batch_Id+')" class="btn" style="cursor:pointer" ><i title="Map Candidate" class="fas fa-plus" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Batch_Name" },
            { "data": "Batch_Code"},
            { "data": "Course_Name" },
            { "data": "Center_Name" },
            { "data": "Trainer_Name" },
            { "data": "Center_Manager_Name" },
            { "data": "Start_Date" },
            { "data": "End_Date" },
            { "data": "Start_Time" },
            { "data": "End_Time" },
            { "data": "Actual_Start_Date"},
            { "data": "Actual_End_Date"}
        ],


    });
}
function EditBatchDetail(BatchId)
{
    $('#hdn_batch_id').val(BatchId);
    //alert('Hi');
    $('#form1').submit();
    
}

function MapCandidateBatch(CourseId,CenterId,BatchId){
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
                    "url": $('#hdn_web_url').val()+ "/ALLCandidatesBasedOnCourse",
                    "type": "POST",
                    "dataType": "json",
                    "data": function (d) {
                        d.candidate_id = 0;
                        d.course_id = CourseId;
                        d.center_id = CenterId;
                        d.batch_id = BatchId;
                    },
                    error: function (e) {
                        $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
                    }

                },

                "columns": [
                    { "data": "S_No"},
                    {
                        "data": function (row, type, val, meta) {
                        if(row.Is_Added){
                            var varButtons = "";
                                varButtons += '<input id="addedchk" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" checked>';
                            return varButtons;
                        }
                        else{
                            var varButtons = "";
                                varButtons += '<input id="addedchk" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" >';
                            return varButtons;
                        }
                        }
                    },
                    { "data": "Candidate_Id"},
                    { "data": "Candidate_Name" },
                    { "data": "Course_Name" },
                    { "data": "Center_Name"},
                    { "data": "Mobile_Number" },
                    { "data": "Registration_Id" },
                    { "data": "Enrollment_Id" },
                    { "data": "Salutaion"}
                    
                ],
            });
            // if(addch){
            //     $('#addedchk').prop('checked',true);
            // }
            // else{
            //     $('#addedchk').prop('checked',false);
            // }
            Course=CourseId;
            Batch=BatchId;
            $('#get').hide();
            $('.center').show();
            

}

function add_map_message(){
    var cands='';
    $('[name=checkcase]:checked').each(function () {
        cands+= $(this).val()+',';
    });
    cands=cands.substring(0,cands.length-1)
    var URL=$('#hdn_web_url').val()+ "/add_edit_map_candidate_batch";
        //alert($('#ddlCourse').val());
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "course_id": Course,
                    "candidate_ids": cands.toString(),
                    "batch_id": Batch
                },
                success:function(data){
                    // var table = $('#tbl_candidate');
                    
                    // swal({
                    //     html: table
                    // }).then(function(){
                    swal({   
                        title:data.PopupMessage.message,
                        text:data.PopupMessage.message+" Successfully !!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                            window.location.href = '/after_popup_batch';
                        });
                //    alert("The Inserted/Upadated Id is "+data.PopupMessage.message);
                //    window.location.href="/after_popup"; 
                // })
                },
                error:function(err)
                {
                    alert('Error! Please try again');
                    return false;
                }
            });
    }