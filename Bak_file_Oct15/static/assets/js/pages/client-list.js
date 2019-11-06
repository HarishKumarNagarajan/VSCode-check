var varTable;
$(document).ready(function () {
    $("#tbl_clients").dataTable().fnDestroy();
    LoadTable(); 
});

function LoadTable()
{
    vartable1 = $("#tbl_clients").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/client_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.client_id = 0;
            },
            error: function (e) {
                $("#tbl_clients tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Client_Name" },
            { "data": "Client_Code" },  
            {
            "data": function (row, type, val, meta) {
            var varButtons = ""; 
            varButtons += '<a onclick="EditClientDetail(\'' + row.Client_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
            return varButtons;
            }
            }
        ],


    });
}
function EditClientDetail(ClientId)
{
    $('#hdn_client_id').val(ClientId);
    $('#form1').submit();
    
}