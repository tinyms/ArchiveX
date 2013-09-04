{% if opt["use_sys_editform"] %}
<script id='{{ opt["dom_id"] }}_EditFormTemplate' type="text/x-jsrender">
	{% for item in opt["cols"] %}
	<div class="form-group">
		<label for="{{ item['name'] }}" class="col-lg-2 control-label">{{ opt["col_title_mapping"][item['name']] }}</label>
		<div class="col-lg-10">
		  <input type="text" class="form-control" id="{{ item['name'] }}" name="{{ item['name'] }}" {{ item['required'] }} {{ item['type'] }}>
		</div>
	</div>
	{% end %}
</script>
{% end %}