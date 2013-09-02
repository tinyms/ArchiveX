<div id="{{domId}}_wrap">
<table id="{{domId}}">
<tfoot><tr>{% raw thTags %}</tr></tfoot>
</table>
</div>
 <div id="{{domId}}_form_container" class="panel">
	<div><button id="{{domId}}_form_return"  onclick="{{domId}}_.form.cancel(this);">返回</button></div>
	<form class="form-horizontal" role="form" id="{{domId}}_EditForm"></form>
	<div class="footer">
		<button id="{{domId}}_form_save" onclick="{{domId}}_.form.save(this);">保存</button>
		<button id="{{domId}}_form_save_continue" onclick="{{domId}}_.form.saveNext(this);">保存并继续</button>
		<button id="{{domId}}_form_reset" onclick="{{domId}}_.form.reset(this);">重填</button>
	</div>
 </div>