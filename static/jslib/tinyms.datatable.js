/**
 * User: tinyms
 * Date: 13-9-2
 * @plugins:
 * function datatable_sortable(id){}
 * function datatable_server_params(id,aoData){} //aoData is list(dict)
 * function datatable_server_data(id, data, textStatus, jqXHR){}
 * function datatable_form_fill(id,row){}
 * function datatable_render(id,k,v,row){}
 * function datatable_render_actionbar(id,k,v,row){}
 * function datatable_data_add(id,form_data){}
 * function datatable_data_update(id,pk,form_data){}
 * function datatable_data_delete(id,pk){}
 * function datatable_data_delete_confirm_label(id);
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
        var len = this.cols.length;
        for (var k = 0; k < len; k++) {
            var item = this.cols[k];
            if (typeof(datatable_render) != "undefined") {
                var func = function (col, v, type, row) {
                    return datatable_render(self.id, col, v, row)
                };
                func.prototype.column = item["mData"];
                item["mRender"] = func;
            }
        }
        self.cols.push({"mData": "id", "sTitle": "#", "mRender": function (col, v, type, row) {
            var action_btns = '<a class="btn-link" title="查看" onclick="' + self.id + '_.RecordSetProvider.Modify(this,' + v + ');"><i class="icon-list-alt"></i></a>';
            if (typeof(datatable_render_actionbar) != "undefined") {
                action_btns += datatable_render_actionbar(self.id, "id", v, row);
            }
            action_btns += ' <a class="btn-link" title="添加" onclick="' + self.id + '_.RecordSetProvider.New(this);"><i class="icon-plus"></i></a>';
            action_btns += ' <a class="btn-link" title="修改" onclick="' + self.id + '_.RecordSetProvider.Modify(this,' + v + ');"><i class="icon-pencil"></i></a>';
            action_btns += ' <a class="btn-link" title="删除" onclick="' + self.id + '_.RecordSetProvider.Delete(this,' + v + ');"><i class="icon-remove"></i></a>';
            return action_btns;
        }});

        var bSorting = true;
        if (typeof(datatable_sortable) != "undefined") {
            bSorting = datatable_sortable(self.id);
        }
        self.config = {
            "bServerSide": true,
            "bProcessing": true,
            "asSorting": bSorting,
            "sDom": "<'row'<'col-sm-6'l><'col-sm-6'f>r>t<'row'<'col-sm-6'i><'col col-sm-6'p>>",
            //"sDom": '<"#' + self.id + '_NewRowBtnWrap">T<"clear">lfrtip',
            //"oTableTools": {"sSwfPath": "/static/jslib/datatable/extras/tabletools/swf/copy_csv_xls.swf"},
            "sAjaxSource": self.request_url + "list",
            "fnServerParams": function (aoData) {
                if (typeof(datatable_server_params) != "undefined") {
                    datatable_server_params(self.id, aoData);
                }
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
                        if (typeof(datatable_server_data) != "undefined") {
                            datatable_server_data(self.id, data, textStatus, jqXHR);
                        }
                    }
                });
            },
            "aoColumns": self.cols,
            "sPaginationType": "full_numbers",
            "oLanguage": {
                "sLengthMenu": "每页显示 _MENU_ 条记录",
                "sZeroRecords": "抱歉， 没有找到",
                "sInfo": "从_START_到_END_ / 共<span style='color: #ff5f5f;'>_TOTAL_</span>条数据",
                "sInfoEmpty": "没有数据",
                "sInfoFiltered": "(从 _MAX_ 条数据中检索)",
                "sZeroRecords": "没有检索到数据",
                "sSearch": "搜索:",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "前页",
                    "sNext": "后页",
                    "sLast": "尾页"
                }

            }
        };
        $('#' + self.id).data("EditFormId", self.editFormId);
        self.__dataTable = $('#' + self.id).dataTable(self.config);
        $('#' + self.id + '_length label').append(" <button class='btn btn-sm btn-white' id='" + self.id + "_NewRowBtn'><i class='icon-plus'></i>新增</button>");
        $("#" + self.id + "_NewRowBtn").click(function () {
            self.switchTableAndEditFormPanel(true);
        });
        return self.__dataTable;
    };
    this.dataTable = function () {
        return self.__dataTable;
    };
    this.switchTableAndEditFormPanel = function (is_panel) {
        if (is_panel) {
            var form_html = "<input type='hidden' id='id' name='id'/>";
            form_html += $("#" + self.id + "_EditFormTemplate").html();
            $("#" + self.id + "_EditForm").html(form_html);
            $("#" + self.id + "_wrap").hide();
            $("#" + self.id + "_form_container").show();
        } else {
            $("#" + self.id + "_EditForm").resetForm();
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
        "save": function (btn, state) {
            if (!$("#" + self.id + "_EditForm").valid()) {
                return;
            }
            $("#" + self.id + "_EditForm").ajaxSubmit({
                "dataType": "json", "url": self.request_url + "save", "type": "post",
                "beforSubmit": function (formData, jqForm, options) {
                },
                "success": function (data, statusText, xhr, $form) {
                    if (data.success) {
                        if (data.msg == "Updated") {
                            if (typeof(datatable_data_add) != "undefined") {
                                return datatable_data_add(self.id, null);
                            }
                        } else if (data.msg == "Newed") {
                            if (typeof(datatable_data_update) != "undefined") {
                                return datatable_data_update(self.id, $("#" + self.id + "_EditForm #id").val(), null);
                            }
                        }
                        if (state == "clear") {
                            $("#" + self.id + "_EditForm").resetForm();
                        }
                        self.Refresh();
                    }
                },
                "error": function () {
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
                self.switchTableAndEditFormPanel(true);
                try {
                    for (k in current_row) {
                        $("#" + self.id + "_EditForm #" + k).val(current_row[k]);
                    }
                    if (typeof(datatable_form_fill) != "undefined") {
                        datatable_form_fill(self.id, current_row);
                    }
                } catch (e) {
                }
            }
        },
        "Delete": function (btn, record_id) {
            this.color_current_row(btn);
            var label = "确定要删除当前选中的记录吗?";
            if (typeof(datatable_data_delete_confirm_label) != "undefined") {
                label = datatable_data_delete_confirm_label(self.id);
            }
            if (confirm(label)) {
                $.post(self.request_url + "delete", {id: record_id}, function (data) {
                    if (data.success) {
                        if (typeof(datatable_data_delete) != "undefined") {
                            return datatable_data_delete(self.id, record_id);
                        }
                        self.Refresh();
                    }
                }, "json");
            }
        }
    };
}