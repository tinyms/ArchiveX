/**
 * User: tinyms
 * Date: 13-9-2
 */
function DataTableX(id_, entityName_, cols_, editFormId_) {
    var self = this;
    this.id = id_;
    this.__dataTable = null;
    this.editFormId = editFormId_;
    this.entityName = entityName_;
    this.cols = cols_;
    this.config = {};
    this.request_url = "/datatable/" + self.entityName + "/";
    this.Create = function () {
        self.cols.push({"mData": "id", "sTitle": "#", "mRender": function (pk, type, full) {
            var action_btns = '<a href="#" onclick="' + self.id + '_.RecordSetProvider.New(this);">增</a>';
            action_btns += ' <a href="#" onclick="' + self.id + '_.RecordSetProvider.Modify(this,' + pk + ');">改</a>';
            action_btns += ' <a href="#" onclick="' + self.id + '_.RecordSetProvider.Delete(this,' + pk + ');">删</a>';
            return action_btns;
        }});
        self.config = {
            "bServerSide": true,
            "bProcessing": true,
            "asSorting": true,
            "sDom": '<"#' + self.id + '_NewRowBtnWrap">T<"clear">lfrtip',
            "oTableTools": {"sSwfPath": "/static/jslib/datatable/extras/tabletools/swf/copy_csv_xls_pdf.swf"},
            "sAjaxSource": self.request_url + "list",
            "fnServerParams": function (aoData) {
            },
            "fnServerData": function (sSource, aoData, fnCallback, oSettings) {
                oSettings.jqXHR = $.ajax({
                    "dataType": "json",
                    "type": "POST",
                    "url": sSource,
                    "data": aoData,
                    "success": function (data, textStatus, jqXHR) {
                        $('#' + self.id).data("DataSet", data);
                        fnCallback(data, textStatus, jqXHR);
                    }
                });
            },
            "aoColumns": self.cols,
            "sPaginationType" : "full_numbers",
			"oLanguage" : {
				"sLengthMenu": "每页显示 _MENU_ 条记录",
				"sZeroRecords": "抱歉， 没有找到",
				"sInfo": "从_START_到_END_ / 共_TOTAL_条数据",
				"sInfoEmpty": "没有数据",
				"sInfoFiltered": "(从 _MAX_ 条数据中检索)",
				"sZeroRecords": "没有检索到数据",
				 "sSearch": "搜索:",
				"oPaginate": {
				"sFirst": "首页",
				"sPrevious": "前一页",
				"sNext": "后一页",
				"sLast": "尾页"
				}

			}
        };
        $('#' + self.id).data("EditFormId", self.editFormId);
        self.__dataTable = $('#' + self.id).dataTable(self.config);
        $('#' + self.id + '_NewRowBtnWrap').html("<button id='" + self.id + "_NewRowBtn'>+</button>");
        $("#" + self.id + "_NewRowBtn").click(function () {
            if(self.editFormId==""){
                self.switchTableAndEditFormPanel(true);
            }
        });
        return self.__dataTable;
    };
    this.dataTable = function () {
        return self.__dataTable;
    };
    this.switchTableAndEditFormPanel=function(is_panel){
        if(is_panel){
            var form_html = "<input type='hidden' id='id' name='id'/>";
            form_html += $("#" + self.id + "_EditFormTemplate").html();
            $("#" + self.id + "_EditForm").html(form_html);
            $("#" + self.id + "_wrap").hide();
            $("#" + self.id + "_form_container").show();
        }else{
            $("#" + self.id + "_wrap").show();
            $("#" + self.id + "_form_container").hide();
        }
    }
    this.Refresh = function () {
        $('#' + self.id).dataTable();
        self.__dataTable.fnClearTable();
    };
    this.DataSet = function () {
        return $('#' + self.id).data("DataSet");
    };
    this.form = {
        "cancel": function (btn) {
            self.switchTableAndEditFormPanel(false);
        },
        "save": function (btn,state) {
            if(!$("#" + self.id + "_EditForm").valid()){
                return;
            }
            $("#" + self.id + "_EditForm").ajaxSubmit({
                "dataType": "json", "url": self.request_url + "save", "type": "post",
                "beforSubmit": function (formData, jqForm, options) {
                },
                "success": function (data, statusText, xhr, $form) {
                    if(data.success){
                        alert(data.msg);
                        if(data.msg=="Updated"){

                        }
                        if(state=="clear"){
                            $("#" + self.id + "_EditForm").resetForm();
                        }
                        self.Refresh();
                    }
                },
                "error":function(){
                    alert("Server Error.");
                }
            });
        },
        "reset": function (btn) {
            $("#" + self.id + "_EditForm").resetForm();
        }
    };
    this.RecordSetProvider = {
        "id": function () {
            return self.id;
        },
        "form_id": function () {
            return $('#' + this.id()).data("EditFormId");
        },
        "color_current_row": function (btn) {
            $("#" + this.id() + " tr").removeAttr("style");
            $(btn).parent().parent().attr("style", "background-color:#99CC99;");
        },
        "New": function (btn) {
            self.switchTableAndEditFormPanel(true);
        },
        "Modify": function (btn, record_id) {
            this.color_current_row(btn);
            var local_ds = $('#' + this.id()).data("DataSet").aaData;
            var current_row = null;
            for (var k = 0; k < local_ds.length; k++) {
                var row = local_ds[k];
                if (row.id == record_id) {
                    current_row = row;
                }
            }
            if (current_row != null) {
                if (this.form_id() == "") {
                    self.switchTableAndEditFormPanel(true);
                    try{
                        for(k in current_row){
                            $("#"+k).val(current_row[k]);
                        }
                    }catch(e){}
                }
            }
        },
        "Delete": function (btn, record_id) {
            this.color_current_row(btn);
            if (confirm("确定要删除当前选中的记录吗?")) {
                $.post(self.request_url + "delete",{id:record_id},function(data){
                    if(data.success){
                        alert(data.msg);
                        self.Refresh();
                    }
                },"json");
            }
        }
    };
}