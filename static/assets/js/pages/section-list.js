var varTable;
$(document).ready(function () {
    $("#tbl_section").dataTable().fnDestroy();
    LoadTable(); 
});

function LoadTable()
{
    vartable1 = $("#tbl_section").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/section_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.section_id = 0;
            },
            error: function (e) {
                $("#tbl_section tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditSectionDetail(\'' + row.Section_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Section_Name" },
            { "data": "Section_Type_Name"},
            { "data": "Parent_Section_Name"}
        ],


    });
}
function EditSectionDetail(SectionId)
{
    $('#hdn_section_id').val(SectionId);
    $('#form1').submit();
    
}