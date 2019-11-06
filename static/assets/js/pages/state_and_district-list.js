var varTable;
$(document).ready(function () {
    $("#tbl_state").dataTable().fnDestroy();
    LoadTable(); 
});

function LoadTable()
{
    vartable1 = $("#tbl_state").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/state_and_district_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.state_id = 0;
            },
            error: function (e) {
                $("#tbl_state tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditStateAndDistrictDetail(\'' + row.State_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "State_Name" }
        ],


    });
}
function EditStateAndDistrictDetail(StateId)
{
    $('#hdn_state_id').val(StateId);
    $('#form1').submit();
    
}