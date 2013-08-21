var {{opt["id"]}} = null;
$(document).ready(function () {
	/*DataTable EditForm Dialog*/
	$('#{{opt["id"]}}_EditFormDialog').dialog({
		autoOpen: false,
		title: 'Edit Form',
		height: 450,
		width: 600,
		modal:true,
		buttons:{
			"Save":function(){},
			Cancel: function(){
				$(this).dialog("close");
			}
		}
	});
	/*DataTable*/
	var aoColumns = {% raw opt["col_defs"] %};
	aoColumns.push({"mData":"id","sTitle":"#","mRender":function(pk, type, full){
		var action_btns = '<a href="#" onclick="{{opt["id"]}}.RecordSetProvider.New(this);">增</a>';
        action_btns += ' <a href="#" onclick="{{opt["id"]}}.RecordSetProvider.Modify(this,'+pk+');">改</a>';
        action_btns += ' <a href="#" onclick="{{opt["id"]}}.RecordSetProvider.Delete(this,'+pk+');">删</a>';
        return action_btns;
	}});
	var {{opt["id"]}}_Configs = {
		"bServerSide": true,
        "bProcessing": true,
        "asSorting": true,
		"sDom":'T<"clear">lfrtip',
		"oTableTools":{"sSwfPath":"/static/jslib/datatable/extras/tabletools/swf/copy_csv_xls_pdf.swf"},
        "sAjaxSource": '/datatable/{{opt["entity_name"]}}',
		"fnServerParams": function(aoData){},
		"fnServerData": function(sSource,aoData,fnCallback,oSettings){
			oSettings.jqXHR = $.ajax({
				"dataType":"json",
				"type":"POST",
				"url":sSource,
				"data":aoData,
				"success":function(data, textStatus, jqXHR){
					$('#{{opt["id"]}}').data("DataSet",data);
					fnCallback(data, textStatus, jqXHR);
				}
			});
		},
		"aoColumns": aoColumns
	};
	try{
		if($.isFunction({{opt["id"]}}_Config_Plug)){
			{{opt["id"]}}_Config_Plug({{opt["id"]}}_Configs);//Custom your datatable config.
		}
	}catch(e){}
	$('#{{opt["id"]}}').data("EditFormId",'{{opt["edit_form_id"]}}');
	var {{opt["id"]}}_ColumnFilter_Configs = {% raw opt["filter_configs"] %};
	{{opt["id"]}}_ColumnFilter_Configs.push(null);
    {{opt["id"]}} = $('#{{opt["id"]}}').dataTable({{opt["id"]}}_Configs).columnFilter({"aoColumns":{{opt["id"]}}_ColumnFilter_Configs});
	new FixedHeader({{opt["id"]}});
	{{opt["id"]}}.RecordSetProvider = {
		"id":function(){
			return '{{opt["id"]}}';
		},
		"form_id":function(){
			return $('#'+this.id()).data("EditFormId");
		},
		"color_current_row":function(btn){
			$("#"+this.id()+" tr").removeAttr("style");
			$(btn).parent().parent().attr("style","background-color:#99CC99;");
		},
		"New" : function(btn){
			$('#'+this.id()+'_EditFormDialog').dialog("open");
			if(this.form_id()==""){
				return;
			}
			var html = Mustache.render($("#"+this.form_id()).html(), {});
			//open edit dialog
			$('#'+this.id()+'_EditFormDialog').dialog("open");
		},
		"Modify": function(btn,record_id){
			this.color_current_row(btn);
			var local_ds = $('#'+this.id()).data("DataSet").aaData;
			var current_row = null;
			for(var k=0;k<local_ds.length;k++){
				var row = local_ds[k];
				if(row.id==record_id){
					current_row = row;
				}
			}
			if(current_row!=null){
				console.log(current_row);
				if(this.form_id()==""){
					return;
				}
				var html = Mustache.render($("#"+this.form_id()).html(), current_row);
				//open edit dialog
				$('#'+this.id()+'_EditFormDialog').dialog("open");
			}
		},
		"Delete":function(btn,record_id){
			this.color_current_row(btn);
			if(confirm("确定要删除当前选中的记录?")){
			
			}
		}
	};
});
