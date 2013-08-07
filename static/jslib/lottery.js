/**
 * Created with PyCharm.
 * User: tinyms
 * Date: 13-8-7
 * Time: 上午11:07
 * To change this template use File | Settings | File Templates.
 */
var matchs_datasource = [];
function show_baseface(match_id) {

}
function show_odds_page(match_id) {

}
$(document).ready(function () {
    $("#match_analyze_btn").click(function(){
        var url = $("#season_url_edit").val();
        url = $.trim(url);
        var params = {"url":url};
        $.post("/api/welcome.MatchAnalyze/run",{"params":JSON.stringify(params)},function(data){
            console.log(data);
        },"json")
    });
    $("#abc").JsonTable({
        head: ['赛事', '球差', '预测', '赛果', '初盘(威廉)', '对阵球队', '比分', '比赛日期', '#'],
        json: ['season_name', 'ball_diff', 'detect_result', 'result',
            'Odds_WL', 'team_names', 'score', 'match_date', 'match_id'],
        render: function (name, value, row) {
            if (name == "score" && value == -1) {
                return "";
            } else if (name == "Odds_WL") {
                return value[0] + " " + value[1] + " " + value[2];
            } else if (name == "match_id") {
                var html = "";
                html += "<button type='button' class='btn btn-primary btn-xs' onclick='show_baseface("+value+");'>析</button>";
                html += "<button type='button' class='btn btn-default btn-xs' onclick='show_odds_page("+value+");'>欧</button>";
                return html;
            }
            return value;
        }
    });
});