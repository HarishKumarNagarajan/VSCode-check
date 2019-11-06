var varTable;
$(document).ready(function () {
    LoadSessionPlan();
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 3 || role_id == 8){}
    var number = document.getElementById('SessionPlanDuration');
    // Listen for input event on numInput.
    number.onkeydown = function(e) {
        if(!((e.keyCode > 95 && e.keyCode < 106)
        || (e.keyCode > 47 && e.keyCode < 58) 
        || e.keyCode == 8)) {
            return false;
        }
    }
});

function LoadSessionPlan(){
    var URL=$('#hdn_web_url').val()+ "/AllSessionPlanList"
                $.ajax({
                    type:"GET",
                    url:URL,
                    async:false,
                    beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
                    datatype:"json",
                    success: function (data){
                        if(data.SessionPlans != null)
                        {
                            $('#ddlSessionPlan').empty();
                            var count=data.SessionPlans.length;
                            if( count> 0)
                            {
                                $('#ddlSessionPlan').append(new Option('Choose Session Plan','0'));
                                for(var i=0;i<count;i++)
                                    $('#ddlSessionPlan').append(new Option(data.SessionPlans[i].Session_Plan_Name,data.SessionPlans[i].Session_Plan_Id));
                            }
                            else
                            {
                                $('#ddlSessionPlan').append(new Option('Choose Session Plan','0'));
                            }
                        }
                    },
                    error:function(err)
                    {
                        alert('Error! Please try again');
                        return false;
                    }
                });
}

function GetModulelist(SessionPlanId){
    $('#sessions').hide();
    var URL=$('#hdn_web_url').val()+ "/AllModuleList"
                $.ajax({
                    type:"POST",
                    url:URL,
                    async:false,
                    beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
                    datatype:"json",
                    data:{
                        'session_plan_id' : SessionPlanId
                    },
                    success: function (data){
                        if(data.Modules != null)
                        {
                            $('#ddlModule').empty();
                            var count=data.Modules.length;
                            if( count> 0)
                            {
                                $('#ddlModule').append(new Option('Choose Module','0'));
                                for(var i=0;i<count;i++)
                                    $('#ddlModule').append(new Option(data.Modules[i].Module_Name,data.Modules[i].Module_Id));
                            }
                            else
                            {
                                $('#ddlModule').append(new Option('Choose Module','0'));
                            }
                        }
                        $('#ModuleOrder').val(data.Module_order+1);
                    },
                    error:function(err)
                    {
                        alert('Error! Please try again');
                        return false;
                    }
                });
                if($('#ddlSessionPlan').val()!=0){    
                    $('.moduleDiv').show();
                }
                else{
                    $('.moduleDiv').hide();
                    $('#getsessions').hide();
                }
}

function get_session_order_for_module(ModuleId)
{
    if($('#ddlModule').val()!="0"){
    var URL=$('#hdn_web_url').val()+ "/get_session_order_for_module"
                $.ajax({
                    type:"POST",
                    url:URL,
                    async:false,
                    beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
                    datatype:"json",
                    data:{
                        'module_id' : ModuleId
                    },
                    success: function (data){
                        $('#SessionOrder').val(data.Session_order+1);
                        $('#SessionCode').val(data.SessionCode);
                    },
                    error:function(err)
                    {
                        alert('Error! Please try again for Session Order');
                        return false;
                    }
                });
            }
}

function TableforSessions(ModuleId){
    get_session_order_for_module(ModuleId);
    vartable1 = $("#tbl_sessions").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/module_session_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.session_id = 0;
                d.module_id = ModuleId;
            },
            error: function (e) {
                $("#tbl_sessions tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "Id"},
            {
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(role_id != 2 && role_id != 7 && role_id != 5)
                        varButtons += '<a onclick="EditSessionDetail(\'' + row.Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User" class="fas fa-edit" ></i></a>';
                    return varButtons;
                    }
                },
            { "data": "Session_Name" },
            { "data": "Session_Code" },
            { "data": "Session_Order"},
            { "data": "Session_Duration" },
            { "data": "Session_Type" },
            
        ],
    });
    if($('#ddlModule').val()!=0 ){    
        $('#getsessions').show();
    }
    else{
        $('#getsessions').hide();
    }
}

function AddSessionPlanDetail(){
    if ($('#SessionPlanName').val()!='' && $('#SessionPlanDuration').val() !=''){
    var URL=$('#hdn_web_url').val()+ "/add_session_plan_details";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "SessionPlanName" : $('#SessionPlanName').val(),
                    "SessionPlanDuration" : $('#SessionPlanDuration').val(),
                    "isactive" : $('#isactive').prop('checked')
                },
                success:function(data){
                    swal({   title:data.PopupMessage.message,
                        text:data.PopupMessage.message+" Successfully !!",
                        icon:"success",
                        confirmButtonClass:"btn btn-confirm mt-2"
                        }).then(function(){
                                    window.location.href = '/session_course';
                                }); 
                },
                error:function(x){
                    alert('error');
                }
            });
        }
        
}

function AddModuleDetail(){
    if($('#ModuleName').val()!='' && $('#ModuleCode').val()!='' && $('#ModuleOrder').val()!='' && $('#ModuleOrder').val()!='' && $('#ddlSessionPlan').val()!=''){
    var URL=$('#hdn_web_url').val()+ "/add_module_details";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "ModuleName" : $('#ModuleName').val(),
                    "ModuleCode" : $('#ModuleCode').val(),
                    "ModuleOrder": $('#ModuleOrder').val(),
                    "SessionPlanId" : $('#ddlSessionPlan').val(),
                    "isactive" : $('#module_isactive').prop('checked')
                },
                success:function(data){
                    swal({   title:data.PopupMessage.message,
                    text:data.PopupMessage.message+" Successfully !!",
                    icon:"success",
                    confirmButtonClass:"btn btn-confirm mt-2"
                    }).then(function(){
                        window.location.href = '/session_course';
                    }
                    );
                },
                error:function(x){
                    alert('error');
                }
            });
        }
        
}

function AddEditSessionDetail(){
    if($('#SessionName').val()!='' && $('#SessionCode').val() !='' && $('#SessionOrder').val()!='' && $('#SessionDescription').val()!='' && $('#LearningOutcome').val()!='' && $('#LearningAids').val()!='' && $('#LearningAct').val()!='' && $('#ddlModule').val()){
    var URL=$('#hdn_web_url').val()+ "/add_edit_session_details";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    "SessionName" : $('#SessionName').val(),
                    "SessionCode" : $('#SessionCode').val(),
                    "SessionOrder": $('#SessionOrder').val(),
                    "SessionDescription" : $('#SessionDescription').val(),
                    "LearningOutcome" : $('#LearningOutcome').val(),
                    "LearningAids": $('#LearningAids').val(),
                    "LearningAct" : $('#LearningAct').val(),
                    "ModuleId" : $('#ddlModule').val(),
                    "isactive" : $('#session_isactive').prop('checked'),
                    "SessionId":$('#hdn_session_id').val(),
                    "SessionDuration" : $('#SessionDuration').val()
                },
                success:function(data){
                    swal({   title:data.PopupMessage.message,
                    text:data.PopupMessage.message+" Successfully !!",
                    icon:"success",
                    confirmButtonClass:"btn btn-confirm mt-2"
                    }).then(function(){
                        window.location.href = '/session_course';
                    }
                    );
                },
                error:function(x){
                    alert('error');
                }
            });
        }
        
}
function EditSessionDetail(SessionId){
    $('#hdn_session_id').val(SessionId);
    var URL=$('#hdn_web_url').val()+ "/GetSessionDetails";
            $.ajax({
                type:"POST",
                url:URL,
                data:{
                    session_id : $('#hdn_session_id').val()
                },
                success:function(data){
                   if(data!=null)
                   {
                       if(data.SessionDetail!="")
                       {
                           $('#SessionName').val(data.SessionDetail.Session_Name);
                           $('#SessionCode').val(data.SessionDetail.Code);
                           $('#SessionOrder').val(data.SessionDetail.Session_Order);
                           $('#SessionDescription').val(data.SessionDetail.Session_Description);
                           $('#LearningOutcome').val(data.SessionDetail.Learning_Outcome);
                           $('#LearningAids').val(data.SessionDetail.Learning_Aids);
                           $('#LearningAct').val(data.SessionDetail.Learning_Activity);
                           $('#SessionDuration').val(data.SessionDetail.Duration);
                           if(data.SessionDetail.Is_Active){
                                $('#session_isactive').prop('checked',true);
                           }
                            else{
                                $('#session_isactive').prop('checked',false);
                            }
                       }
                   } 
                },
                error:function(x){
                    alert('error');
                }
            });
            $('#getsessions').hide();
            $('#add_edit_session').show();
}