
<SCRIPT type="text/javascript">
<!--
var setting = {
	view: {
		addHoverDom: addHoverDom,
		removeHoverDom: removeHoverDom,
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
		beforeDrag: beforeDrag,
		beforeEditName: beforeEditName,
		beforeRemove: beforeRemove,
		beforeRename: beforeRename,
		onRemove: onRemove,
		onRename: onRename,
		onDrop: onDrop
	}
};

var className = "dark";
function beforeDrag(treeId, treeNodes) {
	return true;
}
function beforeEditName(treeId, treeNode) {
	className = (className === "dark" ? "":"dark");
	var zTree = $.fn.zTree.getZTreeObj("org_tree");
	zTree.selectNode(treeNode);
}
function beforeRemove(treeId, treeNode) {
	className = (className === "dark" ? "":"dark");
	var zTree = $.fn.zTree.getZTreeObj("org_tree");
	zTree.selectNode(treeNode);
	return confirm("如果删除,其下的组织结构将会一并删除,确定要删除`" + treeNode.name + "`吗?");
}
function onRemove(e, treeId, node) {
	tinyms.controller.org.OrgEdit.delete({id:node.id},function(b,data){
		if(b&&data[0]=="Success"){
			toastr.success(node.name+"删除成功!");
		}else{
			toastr.error(node.name+"删除失败!");
		}
	});
	console.log(node);
}
function onDrop(e, treeId, treeNodes, targetNode, moveType){
	$.each(treeNodes,function(i,node){
		var params = {"id":node.id,"pId":node.pId,"name":node.name};
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
function beforeRename(treeId, treeNode, newName, isCancel) {
	className = (className === "dark" ? "":"dark");
	if (newName.length == 0) {
		toastr.error("组织名称必须填写!")
		var zTree = $.fn.zTree.getZTreeObj("org_tree");
		setTimeout(function(){zTree.editName(treeNode)}, 10);
		return false;
	}
	return true;
}

function onRename(e, treeId, treeNode, isCancel) {
	var params = {"id":treeNode.id,"pId":treeNode.pId,"name":treeNode.name};
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

var newCount = 1;
function addHoverDom(treeId, treeNode) {
	var sObj = $("#" + treeNode.tId + "_span");
	if (treeNode.editNameFlag || $("#addBtn_"+treeNode.tId).length>0) return;
	var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
		+ "' title='add node' onfocus='this.blur();'></span>";
	sObj.after(addStr);
	var btn = $("#addBtn_"+treeNode.tId);
	if (btn) btn.bind("click", function(){
		var zTree = $.fn.zTree.getZTreeObj("org_tree");
		var catName = window.prompt("组织/部门名称","");
		if(catName.length==0){
			return;
		}
		p = {};
		p.cat_name = catName;
		p.parent_id = treeNode.id
		tinyms.controller.org.OrgEdit.add(p,function(b,id){
			if(b&&id>0){
				zTree.addNodes(treeNode, {id:id, pId:treeNode.id, name:catName});
			}
		});
		
		return false;
	});
};
function removeHoverDom(treeId, treeNode) {
	$("#addBtn_"+treeNode.tId).unbind().remove();
};

$(document).ready(function(){
	
	var zTree = $.fn.zTree.getZTreeObj("org_tree");
	tinyms.controller.org.OrgEdit.list({},function(b,data){
		$.fn.zTree.init($("#org_tree"), setting, data);
	});
	$("#btn_for_org_topcreate").click(function(){
		var v = $.trim($("#input_for_org_topcreate").val());
		if(v.length<=0){
			toastr.error("组织名称必须填写!")
			return;
		}
		p = {};
		p.cat_name = v;
		p.parent_id = 1;
		tinyms.controller.org.OrgEdit.add(p,function(b,data){
			if(b){
				if(data[0]=="Exists"){
					$("#input_for_org_topcreate").val("");
					toastr.error(v+"已经存在!");
				}else if(data[0]>0){
					var zTree = $.fn.zTree.getZTreeObj("org_tree");
					var node = {"id":data[0],"name":p.cat_name};
					zTree.addNodes(null,node);
					$("#input_for_org_topcreate").val("");
					toastr.success(v+"创建成功!");
				}
			}
		});
	});
});
//-->
</SCRIPT>
<ul id="org_tree" class="ztree"></ul>