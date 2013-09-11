<div id="{{opt['id']}}_wrap"  class="table-responsive">
<table id="{{opt['id']}}" class="table table-striped table-hover m-b-none">
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
$(document).ready(function () {
    $("#{{opt['id']}}_form_container").hide();
	{{opt["id"]}}_ = new DataTableX('{{opt["id"]}}','{{opt["entity_name_md5"]}}',{% raw opt["col_defs"] %},'{{opt["edit_form_id"]}}');
	{{opt["id"]}}_.Create();
});
</script>
{% if opt["use_sys_editform"] %}
<script id='{{ opt["id"] }}_EditFormTemplate' type="text/x-jsrender">
	<div class="form-group">
	<div class="col-lg-9 col-lg-offset-3">
	<input type="button" class="btn btn-white btn-sm " id="{{opt['id']}}_form_return"  onclick="{{opt['id']}}_.form.cancel(this);" value="返回"></input>
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