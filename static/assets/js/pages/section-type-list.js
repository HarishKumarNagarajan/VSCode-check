var varTable;
$(document).ready(function () {
    $("#tbl_section_type").dataTable().fnDestroy();
    LoadTable(); 
});

function LoadTable()
{
    vartable1 = $("#tbl_section_type").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/section_type_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.section_type_id = 0;
            },
            error: function (e) {
                $("#tbl_section_type tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditSectionTypeDetail(\'' + row.Section_Type_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Section_Type_Name" }
        ],


    });
}
function EditSectionTypeDetail(SectionTypeId)
{
    $('#hdn_section_type_id').val(SectionTypeId);
    $('#form1').submit();
    
}