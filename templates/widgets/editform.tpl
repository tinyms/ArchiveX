<div id='{{ opt["dom_id"] }}_EditFormDialog'>
<form class="form-horizontal" role="form" id='{{ opt["dom_id"] }}_EditForm'>
<!--Require a hidden input to place table id-->
</form>
</div>
{% if opt["use_sys_editform"] %}
<script id='{{ opt["dom_id"] }}_EditFormTemplate' type="text/x-jsrender">
	{% for elem in opt["cols"] %}
	<div class="form-group">
		<label for="{{ elem }}" class="col-lg-2 control-label">{{ opt["col_title_mapping"][elem] }}</label>
		<div class="col-lg-10">
		  <input type="text" class="form-control" id="{{ elem }}" name="{{ elem }}">
		</div>
	</div>
	{% end %}
</script>
{% end %}