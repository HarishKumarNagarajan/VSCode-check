var varTable;
$(document).ready(function () {
    $("#tbl_user_role").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 3 || role_id == 8)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_user_role").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/user_role_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_role_id = 0;
            },
            error: function (e) {
                $("#tbl_user_role tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "User_Role_Name" },
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
                varButtons += '<a onclick="EditUserRoleDetail(\'' + row.User_Role_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
            return varButtons;
            }
            }
        ],


    });
}
function EditUserRoleDetail(UserRoleId)
{
    $('#hdn_user_role_id').val(UserRoleId);
    $('#form1').submit();
    
}