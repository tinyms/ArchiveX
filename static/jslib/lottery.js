/**
 * Created with PyCharm.
 * User: tinyms
 * Date: 13-8-7
 * Time: 上午11:07
 * To change this template use File | Settings | File Templates.
 */
var timer,matchs_datasource = [];
function show_baseface(match_id) {

}
function show_odds_page(match_id) {
    $("#extern_url_iframe").attr("src","http://odds.500.com/fenxi/ouzhi-"+match_id+"-show-1#datatb");
    $("#OddsComWebPageDlg").modal({show:true,keyboard:true});
}
function fill_datatable(data){
    matchs_datasource = data;
    $("#matchs_table").JsonTableUpdate({
        source:matchs_datasource
    });
}
$(document).ready(function () {
    $("#match_analyze_btn").click(function(){
        var url = $("#season_url_edit").val();
        url = $.trim(url);
        var params = {"url":url};
        $.post("/api/welcome.MatchAnalyze/run",{"params":JSON.stringify(params)},function(data){
            if(data.msg=="Started" || data.msg=="Running" || data.msg=="History"){
                var mum_interval = 10*1000;
                if(data.msg=="History"){
                    mum_interval = 100;
                }
                timer = setInterval(function(){
                    var post_url = "/api/welcome.MatchAnalyze/result";
                    $.post(post_url,{"params":JSON.stringify(params)},function(data){
                        if($.isArray(data)&&data.length>0){
                            //Do..
                            fill_datatable(data);
                            clearInterval(timer)
                        }
                    },"json");
                },mum_interval);//5秒
            }
        },"json")
    });
    
    $("#matchs_table").JsonTable({
        head: ['赛事', '球差', '预测', '赛果', '初盘(威廉)', '对阵球队', '比分', '比赛日期', '#'],
        json: ['season_name', 'ball_diff', 'detect_result', 'result',
            'Odds_WL', 'team_names', 'score', 'match_date', 'match_id'],
        render: function (name, value, row) {
            if (name == "result" && value == -1) {
                return "";
            } else if (name == "Odds_WL") {
                return value[0] + " " + value[1] + " " + value[2];
            } else if (name == "match_id") {
                var html = "";
                html += "<button type='button' class='btn btn-primary btn-xs' onclick='show_baseface("+value+");'>析</button>";
                html += " <button type='button' class='btn btn-default btn-xs' onclick='show_odds_page("+value+");'>欧</button>";
                return html;
            }
            return value;
        }
    });
});