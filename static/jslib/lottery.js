/**
 * Created with PyCharm.
 * User: tinyms
 * Date: 13-8-7
 * Time: 上午11:07
 */
var timer, matchs_datasource = [];
function set_team_names_title(names) {
    $(".team_names_title").each(function (i) {
        $(this).html(names);
    });
}

function odds_style(com_name, start, end) {
    var item = {"com_name": com_name, "start": "", "end": "", "change": ""};
    if ($.isArray(start)&&start.length != 3) {
        return item;
    }
    var draw = start[1] - parseInt(start[1]);
    if (draw > 0.4) {
        draw = "<span style='color: red;'>" + start[1] + "</span>"
    }
    item.start = $.number(start[0], 2) + " " + draw + " " + $.number(start[2], 2);
    if ($.isArray(end)&&end.length != 3) {
        return item;
    }
    item.end = $.number(end[0], 2) + " " + $.number(end[1], 2) + " " + $.number(end[2], 2);
    var diff_win = start[0] - end[0];
    var diff_draw = start[1] - end[1];
    var diff_lost = start[2] - end[2];
    if(diff_win>0){
        diff_win = "<span style='color: red;'>+"+$.number(diff_win, 2)+"</span>";
    }else{
        diff_win = "<span style='color: green;'>"+$.number(diff_win, 2)+"</span>";
    }
    if(diff_draw>0){
        diff_draw = "<span style='color: red;'>+"+$.number(diff_draw, 2)+"</span>";
    }else{
        diff_draw = "<span style='color: green;'>"+$.number(diff_draw, 2)+"</span>";
    }
    if(diff_lost>0){
        diff_lost = "<span style='color: red;'>+"+$.number(diff_lost, 2)+"</span>";
    }else{
        diff_lost = "<span style='color: green;'>"+$.number(diff_lost, 2)+"</span>";
    }
    item.change = diff_win + " " + diff_draw + " " + diff_lost;
    return item;
}

function show_baseface(match_id) {
    var current = undefined;
    for (var k = 0; k < matchs_datasource.length; k++) {
        var row = matchs_datasource[k];
        if (row.match_id == match_id) {
            current = row;
            break;
        }
    }
    if (current != undefined) {
        set_team_names_title(current.team_names);
        var detail = {}
        detail.mix_10 = current.last_mix_total_10;
        detail.last_10 = current.last_10_text_style;
        detail.last_6 = current.last_6_text_style;
        detail.last_4 = current.last_4_text_style;
        detail.ball_diff = current.ball_diff;
        detail.last_battle = current.last_4_status_text_style;
        detail.detect_result = current.detect_result;

        var odds = [];
        odds[0]=odds_style("威廉",current.Odds_WL,current.Odds_WL_Change);
        odds[1]=odds_style("立博",current.Odds_LB,current.Odds_LB_Change);
        odds[2]=odds_style("易博",current.Odds_YSB,current.Odds_YSB_Change);
        odds[3]=odds_style("贝塔",current.Odds_365,current.Odds_365_Change);
        odds[4]=odds_style("澳门",current.Odds_AM,current.Odds_AM_Change);
        detail.odds = odds;

        var html = Mustache.render($("#match_details_tpl").html(),detail);
        console.log(html);
        $("#base_face_details").html(html);
    }
    $("#DataParseDlg").modal({show: true, keyboard: true});
}
function show_odds_page(match_id) {
    var current = undefined;
    for (var k = 0; k < matchs_datasource.length; k++) {
        var row = matchs_datasource[k];
        if (row.match_id == match_id) {
            current = row;
            break;
        }
    }
    if (current != undefined) {
        set_team_names_title(current.team_names);
        $("#extern_url_iframe").attr("src", "http://odds.500.com/fenxi/ouzhi-" + match_id + "-show-1#datatb");
        $("#OddsComWebPageDlg").modal({show: true, keyboard: true});
    }
}
function fill_datatable(data) {
    matchs_datasource = data;
    $("#matchs_table").JsonTableUpdate({
        source: matchs_datasource
    });
}
$(document).ready(function () {

    $('#DataParseDlg').on('show', function () {
        $(this).css({
            'margin-top': function () {
                alert(1);
                return window.pageYOffset - ($(this).height() / 2);
            }
        });
    });

    $("#match_analyze_btn").click(function () {
        var url = $("#season_url_edit").val();
        url = $.trim(url);
        var params = {"url": url};
        $.post("/api/welcome.MatchAnalyze/run", {"params": JSON.stringify(params)}, function (data) {
            if (data.msg == "Started" || data.msg == "Running" || data.msg == "History") {
                var mum_interval = 5 * 1000;
                if (data.msg == "History") {
                    mum_interval = 100;
                }
                timer = setInterval(function () {
                    var post_url = "/api/welcome.MatchAnalyze/result";
                    $.post(post_url, {"params": JSON.stringify(params)}, function (data) {
                        if ($.isArray(data) && data.length > 0) {
                            //Do..
                            fill_datatable(data);
                            clearInterval(timer)
                        }
                    }, "json");
                }, mum_interval);//5秒
            }
        }, "json")
    });

    $("#matchs_table").JsonTable({
        head: ['赛事', '球差', '预测', '赛果', '初盘(威廉)', '对阵球队', '比分', '比赛日期', '#'],
        json: ['season_name', 'ball_diff', 'detect_result', 'result',
            'Odds_WL', 'team_names', 'score', 'match_date', 'match_id'],
        render: function (name, value, row) {
            if (name == "result" && value == -1) {
                return "";
            } else if (name == "Odds_WL") {
                return $.number(value[0], 2) + " " + $.number(value[1], 2) + " " + $.number(value[2], 2);
            } else if (name == "match_id") {
                var html = "";
                html += "<button type='button' class='btn btn-primary btn-xs' onclick='show_baseface(" + value + ");'>析</button>";
                html += " <button type='button' class='btn btn-default btn-xs' onclick='show_odds_page(" + value + ");'>欧</button>";
                return html;
            }
            return value;
        }
    });
});