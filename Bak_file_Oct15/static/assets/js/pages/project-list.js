var varTable;
$(document).ready(function () {
    $("#alternative-page-datatable").dataTable().fnDestroy();
    LoadTable();      

  /*  $("#alternative-page-datatable").DataTable({
		pagingType: "full_numbers",
		drawCallback: function () {
			$(".dataTables_paginate > .pagination").addClass("pagination-rounded")
		}
    })*/
});

function LoadTable()
{
    vartable1 = $("#alternative-page-datatable").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/project_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.project_id = 0;
            },
            error: function (e) {
                $("#alternative-page-datatable tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Project_Name" },
            { "data": "Client_Name" },            
            { "data": "Practice_Name"},
            {
            "data": function (row, type, val, meta) {
            var varButtons = ""; 
            varButtons += '<a onclick="EditProjectDetail(\'' + row.Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Project" class="fas fa-edit" ></i></a>';
            return varButtons;
            }
            }
        ],


    });
}
function EditProjectDetail(ProjectId)
{
    $('#hdn_project_id').val(ProjectId);
    $('#form1').submit();
    
}