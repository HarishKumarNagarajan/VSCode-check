var varTable;
$(document).ready(function () {
    $("#tbl_qp").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_qp").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/qp_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.qp_id = 0;
            },
            error: function (e) {
                $("#tbl_qp tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(role_id != 5)
                        varButtons += '<a onclick="EditCenterCategoryDetail(\'' + row.Qp_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                    return varButtons;
                }
            },
            { "data": "Qp_Name" },
            { "data": "Qp_Code"},
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
function EditCenterCategoryDetail(QpId)
{
    $('#hdn_qp_id').val(QpId);
    $('#form1').submit();
    
}