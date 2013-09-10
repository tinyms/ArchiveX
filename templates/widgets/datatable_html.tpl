<div id="{{opt['id']}}_wrap"  class="table-responsive">
<table id="{{opt['id']}}" class="table table-striped m-b-none">
<tfoot><tr>{% raw opt['thTags'] %}</tr></tfoot>
</table>
</div>
 <div id="{{opt['id']}}_form_container" class="panel">
	<div><button id="{{opt['id']}}_form_return"  onclick="{{opt['id']}}_.form.cancel(this);">返回</button></div>
	<form class="form-horizontal" role="form" id="{{opt['id']}}_EditForm"></form>
	<div class="footer">
		<button id="{{opt['id']}}_form_save" onclick="{{opt['id']}}_.form.save(this,'');">保存</button>
		<button id="{{opt['id']}}_form_save_continue" onclick="{{opt['id']}}_.form.save(this,'clear');">保存并继续</button>
		<button id="{{opt['id']}}_form_reset" onclick="{{opt['id']}}_.form.reset(this);">重填</button>
	</div>
 </div>
<script type="text/javascript">
var {{opt["id"]}}_ = null;
$(document).ready(function () {
    $("#{{opt['id']}}_form_container").hide();
	{{opt["id"]}}_ = new DataTableX('{{opt["id"]}}','{{opt["entity_name_md5"]}}',{% raw opt["col_defs"] %},'{{opt["edit_form_id"]}}');
	{{opt["id"]}}_.Create();
});
</script>
{% if opt["use_sys_editform"] %}
<script id='{{ opt["id"] }}_EditFormTemplate' type="text/x-jsrender">
	{% for item in opt["cols"] %}
	<div class="form-group">
		<label for="{{ item['name'] }}" class="col-lg-2 control-label">{{ item['name'] }}</label>
		<div class="col-lg-10">
		  <input type="text" class="form-control" id="{{ item['name'] }}" name="{{ item['name'] }}" {{ item['required'] }} {{ item['type'] }}>
		</div>
	</div>
	{% end %}
</script>
{% end %}