
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
		onRename: onRename
	}
};

var zNodes =[
	{ id:1, pId:0, name:"父节点 1", open:true},
	{ id:11, pId:1, name:"叶子节点 1-1"},
	{ id:12, pId:1, name:"叶子节点 1-2"},
	{ id:13, pId:1, name:"叶子节点 1-3"},
	{ id:2, pId:0, name:"父节点 2", open:true},
	{ id:21, pId:2, name:"叶子节点 2-1"},
	{ id:22, pId:2, name:"叶子节点 2-2"},
	{ id:23, pId:2, name:"叶子节点 2-3"},
	{ id:3, pId:0, name:"父节点 3", open:true},
	{ id:31, pId:3, name:"叶子节点 3-1"},
	{ id:32, pId:3, name:"叶子节点 3-2"},
	{ id:33, pId:3, name:"叶子节点 3-3"}
];
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
function onRemove(e, treeId, treeNode) {
	
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
	console.log(treeNode);
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
		p.parent_id = 1
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
	tinyms.controller.org.OrgEdit.list({},function(b,data){console.log(data);});
	$.fn.zTree.init($("#org_tree"), setting, zNodes);
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
					$("#input_for_org_topcreate").val("");
					toastr.success(v+"创建成功!");
				}
			}
		});
	});
});
//-->
</SCRIPT>
<style type="text/css">
.ztree li span.button.add {margin-left:2px; margin-right: -1px; background-position:-144px 0; vertical-align:top; *vertical-align:middle}
</style>
<ul id="org_tree" class="ztree"></ul>