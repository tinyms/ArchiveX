var {{opt["id"]}}_ = null;
$(document).ready(function () {
	{{opt["id"]}}_ = new DataTableX('{{opt["id"]}}','{{opt["entity_name"]}}',{% raw opt["col_defs"] %},{% raw opt["filter_configs"] %},'{{opt["edit_form_id"]}}');
	{{opt["id"]}}_.Create();
});
