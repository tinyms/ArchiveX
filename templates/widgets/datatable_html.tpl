{% if auth({opt["point"].list}) %}
<div id="{{opt['id']}}_wrap"  class="table-responsive">
<table id="{{opt['id']}}" class="table table-condensed table-hover m-b-none">
<tfoot><tr>{% raw opt['thTags'] %}</tr></tfoot>
</table>
</div>
<div class="col-sm-6">
 <div id="{{opt['id']}}_form_container" class="panel-body">
	<form class="form-horizontal" role="form" id="{{opt['id']}}_EditForm"></form>
 </div>
</div>
<script type="text/javascript">
var {{opt["id"]}}_ = null;
function {{opt["id"]}}_actionbar_render(col,v,type,row){
	var action_btns = '<a class="btn-link" title="查看" onclick="{{opt["id"]}}_.RecordSetProvider.Modify(this,' + v + ');"><i class="icon-list-alt"></i></a>';
	if (typeof(datatable_render_actionbar) != "undefined") {
		action_btns += datatable_render_actionbar('{{opt["id"]}}', "id", v, row);
	}
	{% if auth({opt["point"].add}) %}
	action_btns += ' <a class="btn-link" title="添加" onclick="{{opt["id"]}}_.RecordSetProvider.New(this);"><i class="icon-plus"></i></a>';
	{% end %}
	{% if auth({opt["point"].update}) %}
	action_btns += ' <a class="btn-link" title="修改" onclick="{{opt["id"]}}_.RecordSetProvider.Modify(this,' + v + ');"><i class="icon-pencil"></i></a>';
	{% end %}
	{% if auth({opt["point"].delete}) %}
	action_btns += ' <a class="btn-link" title="删除" onclick="{{opt["id"]}}_.RecordSetProvider.Delete(this,' + v + ');"><i class="icon-remove"></i></a>';
	{% end %}
	return action_btns;
}
$(document).ready(function () {
    $("#{{opt['id']}}_form_container").hide();
	{{opt["id"]}}_ = new DataTableX('{{opt["id"]}}','{{opt["entity_name_md5"]}}',{% raw opt["col_defs"] %},'{{opt["edit_form_id"]}}',{{opt["id"]}}_actionbar_render);
	{{opt["id"]}}_.Create();
});
</script>
{% if opt["use_sys_editform"] %}
<script id='{{ opt["id"] }}_EditFormTemplate' type="text/x-jsrender">
	<div class="form-group">
	<div class="col-lg-9 col-lg-offset-3">
	<input type="button" class="btn btn-white btn-sm " id="{{opt['id']}}_form_return"  onclick="{{opt['id']}}_.form.cancel(this);" value="返回"/>
	</div>
	</div>
	{% for item in opt["cols"] %}
	<div class="form-group">
		<label for="{{ item['name'] }}" class="col-lg-3 control-label">{{ item['name'] }}</label>
		<div class="col-lg-8">
		  <input type="text" class="form-control" id="{{ item['name'] }}" name="{{ item['name'] }}" {{ item['required'] }} {{ item['type'] }}>
		</div>
	</div>
	{% end %}
	<div class="form-group">
	<div class="col-lg-9 col-lg-offset-3">
		<input type="button" class="btn btn-primary btn-sm" id="{{opt['id']}}_form_save" onclick="{{opt['id']}}_.form.save(this,'');" value="保存"></button>
		<input type="button" class="btn btn-white btn-sm" id="{{opt['id']}}_form_save_continue" onclick="{{opt['id']}}_.form.save(this,'clear');" value="保存并继续"></button>
		<input type="button" class="btn btn-white btn-sm" id="{{opt['id']}}_form_reset" onclick="{{opt['id']}}_.form.reset(this);" value="重填"></button>
	</div>
	<div class="col-lg-10"></div>
	</div>
</script>
{% end %}
{% end %}