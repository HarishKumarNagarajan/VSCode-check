var varTable;
$(document).ready(function () {
    $("#tbl_users").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_users").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/user_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_id = 0;
            },
            error: function (e) {
                $("#tbl_users tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id != 5)
                    varButtons += '<a onclick="EditUserDetail(\'' + row.User_Id + '\',\'' + row.User_Role_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "User_Name" },
            { "data": "Email" },
            { "data": "User_Role_Name" },
            { "data": "Mobile_Number"},
            { "visible":false, "data": "Center_Name" },
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
function EditUserDetail(UserId,UserRoleId)
{
    $('#hdn_user_id').val(UserId);
    //alert('Hi');
    $('#form1').submit();
    
}
