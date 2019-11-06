var varTable;
$(document).ready(function () {
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
            { "data": "Batch_Name" },
            { "data": "Course_Name" },
            { "data": "Center_Name" },
            { "data": "Trainer_Name" },
            { "data": "Center_Manager_Name" },
            { "data": "Start_Date" },
            { "data": "End_Date" },
            { "data": "Start_Time" },
            { "data": "End_Time" },
            {
            "data": function (row, type, val, meta) {
			
            var varButtons = ""; 
            if(role_id != 2 && role_id != 7 && role_id != 5)
                varButtons += '<a onclick="EditBatchDetail(\'' + row.Batch_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User" class="fas fa-edit" ></i></a>';
            return varButtons;
            }
            }
        ],


    });
}
function EditBatchDetail(BatchId)
{
    $('#hdn_batch_id').val(BatchId);
    $('#form1').submit();
    
}
