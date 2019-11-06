var varTable;
$(document).ready(function () {
    $("#tbl_centers").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_centers").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/center_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.center_id = 0;
            },
            error: function (e) {
                $("#tbl_centers tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {
                "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id != 5)
                    varButtons += '<a onclick="EditCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Center" class="fas fa-edit" ></i></a><a onclick="AddSubCenterDetail(\'' + row.Center_Id + '\')" class="btn" style="cursor:pointer" ><i title="Add SubCenter" class="fas fa-plus" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Center_Name" },
            { "data": "Center_Type_Name"},
            { "data": "Center_Category_Name" },
            { "data": "Bu_Name"},
            { "data": "Region_Name"},
            { "data": "Cluster_Name"},
            { "data": "Country_Name"},
            { "data": "State_Name" },
            { "data": "District_Name"},
            { "data": "Location" },
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
        "ColumnDefs":[
            {
                orderable:false,
                targets:[1]
            }
        ]

    });
}
function EditCenterDetail(CenterId)
{
    $('#hdn_center_id').val(CenterId);
    $('#form1').submit();
    
}
function AddSubCenterDetail(ParentCenterId)
{
    //alert(ParentCenterId);
    $('#hdn_center_id').val(ParentCenterId);
    $('#form1').attr('action', '/assign_parent_center_id_for_sub_center');
    //alert($('#hdn_parent_center_id').val());
    $('#form1').submit();
}