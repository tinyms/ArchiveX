
<SCRIPT type="text/javascript">
<!--
var {{id}}_taxonomy = '{{opt["taxonomy"]}}';
var {{id}}_setting = {
	view: {
		addHoverDom: {{id}}_addHoverDom,
		removeHoverDom: {{id}}_removeHoverDom,
		selectedMulti: false
	},
	edit: {
		enable: true,
		editNameSelectAll: true
	},
	data: {
		simpleData: {
			enable: true,
			idKey: "id",
			pIdKey: "pId",
			rootPId: 1
		}
	},
	callback: {
		beforeDrag: {{id}}_beforeDrag,
		beforeEditName: {{id}}_beforeEditName,
		beforeRemove: {{id}}_beforeRemove,
		beforeRename: {{id}}_beforeRename,
		onRemove: {{id}}_onRemove,
		onRename: {{id}}_onRename,
		onDrop: {{id}}_onDrop
	}
};

var {{id}}_className = "dark";
function {{id}}_beforeDrag(treeId, treeNodes) {
	return true;
}
function {{id}}_beforeEditName(treeId, treeNode) {
	{{id}}_className = ({{id}}_className === "dark" ? "":"dark");
	var zTree = $.fn.zTree.getZTreeObj("{{id}}");
	zTree.selectNode(treeNode);
}
function {{id}}_beforeRemove(treeId, treeNode) {
	{{id}}_className = ({{id}}_className === "dark" ? "":"dark");
	var zTree = $.fn.zTree.getZTreeObj("{{id}}");
	zTree.selectNode(treeNode);
	return confirm("如果删除,其下的组织结构将会一并删除,确定要删除`" + treeNode.name + "`吗?");
}
function {{id}}_onRemove(e, treeId, node) {
	tinyms.controller.org.OrgEdit.delete({id:node.id,taxonomy:{{id}}_taxonomy},function(b,data){
		if(b&&data[0]=="Success"){
			toastr.success(node.name+"删除成功!");
		}else{
			toastr.error(node.name+"删除失败!");
		}
	});
}
function {{id}}_onDrop(e, treeId, treeNodes, targetNode, moveType){
	$.each(treeNodes,function(i,node){
		var params = {"id":node.id,"pId":node.pId,"name":node.name,taxonomy:{{id}}_taxonomy};
		tinyms.controller.org.OrgEdit.update(params,function(b,data){
			if(b){
				if(data[0]=="Success"){
					toastr.success(node.name+"修改成功!");
				}else{
					toastr.error(node.name+"修改失败!");
				}
			}
		});
	});
}
function {{id}}_beforeRename(treeId, treeNode, newName, isCancel) {
	{{id}}_className = ({{id}}_className === "dark" ? "":"dark");
	if (newName.length == 0) {
		toastr.error("组织名称必须填写!")
		var zTree = $.fn.zTree.getZTreeObj("{{id}}");
		setTimeout(function(){zTree.editName(treeNode)}, 10);
		return false;
	}
	return true;
}

function {{id}}_onRename(e, treeId, treeNode, isCancel) {
	var params = {"id":treeNode.id,"pId":treeNode.pId,"name":treeNode.name,taxonomy:{{id}}_taxonomy};
	tinyms.controller.org.OrgEdit.update(params,function(b,data){
		if(b){
			if(data[0]=="Success"){
				toastr.success(treeNode.name+"修改成功!");
			}else{
				toastr.error(treeNode.name+"修改失败!");
			}
		}
	});
}

function {{id}}_addHoverDom(treeId, treeNode) {
	var sObj = $("#" + treeNode.tId + "_span");
	if (treeNode.editNameFlag || $("#addBtn_"+treeNode.tId).length>0) return;
	var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
		+ "' title='add node' onfocus='this.blur();'></span>";
	sObj.after(addStr);
	var btn = $("#addBtn_"+treeNode.tId);
	if (btn) btn.bind("click", function(){
		var zTree = $.fn.zTree.getZTreeObj("{{id}}");
		var catName = window.prompt("{{ph}}名称","");
		if(catName.length==0){
			return;
		}
		p = {};
		p.cat_name = catName;
		p.parent_id = treeNode.id
		p.taxonomy = {{id}}_taxonomy;
		tinyms.controller.org.OrgEdit.add(p,function(b,id){
			if(b&&id>0){
				zTree.addNodes(treeNode, {id:id, pId:treeNode.id, name:catName});
			}
		});
		
		return false;
	});
};
function {{id}}_removeHoverDom(treeId, treeNode) {
	$("#addBtn_"+treeNode.tId).unbind().remove();
};
function {{id}}_create_top_level(btn){
	var v = $.trim($("#{{id}}_toplevel_name").val());
	if(v.length<=0){
		toastr.error("组织名称必须填写!")
		return;
	}
	p = {};
	p.cat_name = v;
	p.parent_id = 1;
	p.taxonomy = {{id}}_taxonomy;
	tinyms.controller.org.OrgEdit.add(p,function(b,data){
		if(b){
			if(data[0]=="Exists"){
				toastr.error(v+"已经存在!");
			}else if(data[0]>0){
				var zTree = $.fn.zTree.getZTreeObj("{{id}}");
				var node = {"id":data[0],"name":p.cat_name};
				zTree.addNodes(null,node);
				$("#{{id}}_toplevel_name").val("");
				toastr.success(v+"创建成功!");
			}
		}
	});
}
$(document).ready(function(){
	$("#{{ id }}_toplevel_name").keypress(function(e){
		if(e.which==13){
			{{id}}_create_top_level(null);
		}
	});
	tinyms.controller.org.OrgEdit.list({taxonomy:{{id}}_taxonomy},function(b,data){
		$.fn.zTree.init($("#{{id}}"), {{id}}_setting, data);
	});
});
//-->
</SCRIPT>
<div class="panel">
<header class="panel-heading">
<div class="row">
	<div class="col-lg-12">
		<div class="input-group">
	  <input type="text" class="form-control" placeholder="{{ ph }}" id="{{ id }}_toplevel_name">
	  <span class="input-group-btn">
		<button class="btn btn-default" type="button" onclick='{{ id }}_create_top_level(this);'><i class="icon-plus icon-large"></i></button>
	  </span>
	</div>
	</div>
</div>
</header>
<div class="panel-body">
	<ul id="{{ id }}" class="ztree"></ul>
</div>
</div>