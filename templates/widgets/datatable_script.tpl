var {{opt["id"]}}_ = null;
$(document).ready(function () {
    $("#{{opt["id"]}}_form_container").hide();
	{{opt["id"]}}_ = new DataTableX('{{opt["id"]}}','{{opt["entity_name"]}}',{% raw opt["col_defs"] %},'{{opt["edit_form_id"]}}');
	{{opt["id"]}}_.Create();
});
