var varTable;
$(document).ready(function () {
    $("#tbl_center_types").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_center_types").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/center_type_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.center_type_id = 0;
            },
            error: function (e) {
                $("#tbl_center_types tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
            "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(role_id != 5)
                        varButtons += '<a onclick="EditCenterTypeDetail(\'' + row.Center_Type_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                    return varButtons;
                }
            },
            { "data": "Center_Type_Name" },
            { "data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            }
        ],


    });
}
function EditCenterTypeDetail(CenterTypeId)
{
    $('#hdn_center_type_id').val(CenterTypeId);
    $('#form1').submit();
    
}