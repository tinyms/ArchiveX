/**
 * Created with PyCharm.
 * User: tinyms
 * Date: 13-8-7
 * Time: 上午11:07
 */
var timer, matchs_datasource = [], history_relation_query_datasource = undefined;
function set_team_names_title(names) {
    $(".team_names_title").each(function (i) {
        $(this).html(names);
    });
}

function odds_style(com_name, start, end) {
    var item = {"com_name": com_name, "start": "", "end": "", "change": ""};
    if ($.isArray(start) && start.length != 3) {
        return item;
    }
    var draw = start[1] - parseInt(start[1]);
    if (draw > 0.4) {
        draw = "<span style='color: red;'>" + $.number(start[1], 2) + "</span>"
    } else {
        draw = $.number(start[1], 2);
    }
    item.start = $.number(start[0], 2) + " " + draw + " " + $.number(start[2], 2);
    if ($.isArray(end) && end.length != 3) {
        return item;
    }
    item.end = $.number(end[0], 2) + " " + $.number(end[1], 2) + " " + $.number(end[2], 2);
    var diff_win = end[0] - start[0];
    var diff_draw = end[1] - start[1];
    var diff_lost = end[2] - start[2];
    if (diff_win > 0) {
        diff_win = "<span style='color: red;'>+" + $.number(diff_win, 2) + "</span>";
    } else if (diff_win < 0) {
        diff_win = "<span style='color: green;'>" + $.number(diff_win, 2) + "</span>";
    } else {
        diff_win = "+" + $.number(diff_win, 2);
    }
    if (diff_draw > 0) {
        diff_draw = "<span style='color: red;'>+" + $.number(diff_draw, 2) + "</span>";
    } else if (diff_draw < 0) {
        diff_draw = "<span style='color: green;'>" + $.number(diff_draw, 2) + "</span>";
    } else {
        diff_draw = "+" + $.number(diff_draw, 2);
    }
    if (diff_lost > 0) {
        diff_lost = "<span style='color: red;'>+" + $.number(diff_lost, 2) + "</span>";
    } else if (diff_lost < 0) {
        diff_lost = "<span style='color: green;'>" + $.number(diff_lost, 2) + "</span>";
    } else {
        diff_lost = "+" + $.number(diff_lost, 2);
    }
    item.change = diff_win + " " + diff_draw + " " + diff_lost;
    return item;
}
function hightlight_matchs_grid_row(btn) {
    $("#matchs_table tr").removeClass("success");
    var tr = $(btn).parent().parent();
    $(tr).addClass("success");
}
function show_baseface(self, match_id) {
    hightlight_matchs_grid_row(self);
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
        odds[0] = odds_style("威廉", current.Odds_WL, current.Odds_WL_Change);
        odds[1] = odds_style("立博", current.Odds_LB, current.Odds_LB_Change);
        odds[2] = odds_style("易博", current.Odds_YSB, current.Odds_YSB_Change);
        odds[3] = odds_style("贝塔", current.Odds_365, current.Odds_365_Change);
        odds[4] = odds_style("澳门", current.Odds_AM, current.Odds_AM_Change);
        detail.odds = odds;

        var html = Mustache.render($("#match_details_tpl").html(), detail);
        $("#base_tab").html(html);
        $("#extern_url_iframe").attr("src", "http://odds.500.com/fenxi/ouzhi-" + match_id + "-show-1#datatb");
        var ctx = document.getElementById("team_force_chart").getContext("2d");
        var chart_data = {
            labels: ["近10场", "近06场", "近04场"],
            datasets: [
                {
                    fillColor: "rgba(255,228,196,0.5)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    data: current.client_forces
                },
                {
                    fillColor: "rgba(151,187,205,0.5)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    data: current.main_forces
                }
            ]
        }
        new Chart(ctx).Line(chart_data);
        $("#ref_odds_force").val(current.detect_result);
        $("#ref_odds_companys").val("beta");
        var first = current.Odds_365;
        if (first.length == 3) {
            var draw = first[1] - parseInt(first[1]);
            $("#ref_odds_draw_ext").val($.number(draw, 2));
            var direct = "3";
            var diff = first[0] - first[2];
            if (diff > 0) {
                direct = "0"
            } else if (diff == 0) {
                direct = "1";
            }
            var diff2 = "gt";
            if (current.Odds_365_Change[1] - first[1] < 0) {
                diff2 = "lt";
            }
            $("#ref_odds_change_direct").val(diff2);
            $("#ref_win_direct").val(direct);
            if(direct=="3"){
                $("#ref_odds_win").val($.number(first[0], 1));
            }else if(direct=="0"){
                $("#ref_odds_win").val($.number(first[2], 1));
            }
            history_query();
        }
    }
    $("#DataParseDlg").modal({show: true, keyboard: true});
}

function fill_datatable(data) {
    matchs_datasource = data;
    $("#matchs_table").JsonTableUpdate({
        source: matchs_datasource
    });
}
function history_query(){
    var params_ = {
            "force": $("#ref_odds_force").val(),
            "company": $("#ref_odds_companys").val(),
            "draw_ext": $("#ref_odds_draw_ext").val(),
            "draw_change_direct": $("#ref_odds_change_direct").val(),
            "draw_range": $("#ref_odds_draw_range").val(),
            "win_direct": $("#ref_win_direct").val(),
            "odds_win": $("#ref_odds_win").val()
        };
        WelcomeMatchHistoryQuery.find(params_, function (b, data) {
            if (b) {
                history_relation_query_datasource = data;
                console.log(data);
                $("#badge_win").html(data["win"]["total"])
                $("#badge_draw").html(data["draw"]["total"])
                $("#badge_lost").html(data["lost"]["total"])
                $("#query_result_win_table").JsonTableUpdate({source: data["win"]["items"]})
                $("#query_result_draw_table").JsonTableUpdate({source: data["draw"]["items"]})
                $("#query_result_lost_table").JsonTableUpdate({source: data["lost"]["items"]})
            }
        }, "json");
}
$(document).ready(function () {

    $('#DataParseDlg').on('show', function () {
        $(this).css({
            'margin-top': function () {
                return window.pageYOffset - ($(this).height() / 2);
            }
        });
    });

    $("#btn_history_relation_query").click(function () {
        history_query();
    });

    $("#match_analyze_btn").click(function () {
        $("#loading").show();
        var url = $("#season_url_edit").val();
        url = $.trim(url);
        var state = $("#match_parse_action").prop("checked");
        console.log(state);
        if (state) {
            state = "Refresh";
        } else {
            state = "Parse";
        }
        var params = {"url": url, "act": state};
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
                            $("#loading").hide();
                        }
                    }, "json");
                }, mum_interval);//5秒
            }
        }, "json")
    });

    $("#matchs_table").JsonTable({
        head: ['赛事', '球差', '预测', '赛果', '初盘(威廉)', '对阵球队', '比分', '比赛日期', '#'],
        json: ['season_name', 'ball_diff', 'detect_result', 'actual_result',
            'Odds_WL', 'team_names', 'score', 'match_date', 'match_id'],
        render: function (name, value, row) {
            if (name == "actual_result" && value != -1) {
                return value;
            } else if (name == "Odds_WL") {
                return $.number(value[0], 2) + " " + $.number(value[1], 2) + " " + $.number(value[2], 2);
            } else if (name == "match_id") {
                var html = "";
                html += "<button type='button' class='btn btn-primary btn-xs' onclick='show_baseface(this," + value + ");'>析</button>";
                return html;
            }
            return value;
        }
    });

    // 查询表
    var query_table_meta = {
        head: ['球差', "初赔", "变赔", "变化", "球队", "赛事", "#"],
        json: ['balls_diff', 'first', 'last', 'change', 'vs_team_names', 'evt_name', 'url_key'],
        render: function (name, val, row) {
            var com_code = $("#ref_odds_companys").val();
            if (name == "first") {
                var odds = row["odds_" + com_code]
                return $.number(odds[0], 2) + " " + $.number(odds[1], 2) + " " + $.number(odds[2], 2);
            } else if (name == "last") {
                var odds = row["odds_" + com_code + "_c"]
                return $.number(odds[0], 2) + " " + $.number(odds[1], 2) + " " + $.number(odds[2], 2);
            } else if (name == "change") {
                var first = row["odds_" + com_code]
                var change = row["odds_" + com_code + "_c"]
                var win = change[0] - first[0]
                var draw = change[1] - first[1]
                var lost = change[2] - first[2]
                var html = "";
                if (win > 0) {
                    html += "+<span style='color: red;'>" + $.number(win, 2) + "</span>";
                } else if (win < 0) {
                    html += "-<span style='color: green;'>" + $.number(Math.abs(win), 2) + "</span>";
                } else {
                    html += "+<span>" + $.number(win, 2) + "</span>";
                }
                if (draw > 0) {
                    html += " +<span style='color: red;'>" + $.number(draw, 2) + "</span>";
                } else if (draw < 0) {
                    html += " -<span style='color: green;'>" + $.number(Math.abs(draw), 2) + "</span>";
                } else {
                    html += " +<span>" + $.number(draw, 2) + "</span>";
                }
                if (lost > 0) {
                    html += " +<span style='color: red;'>" + $.number(lost, 2) + "</span>";
                } else if (lost < 0) {
                    html += " -<span style='color: green;'>" + $.number(Math.abs(lost), 2) + "</span>";
                } else {
                    html += " +<span>" + $.number(lost, 2) + "</span>";
                }
                return html;
            } else if (name == "url_key") {
                return "<a target='_blank' href='http://odds.500.com/fenxi/ouzhi-" + val + "#datatb'>欧</a>";
            }
            return val;
        }
    };

    $("#query_result_win_table").JsonTable(query_table_meta);
    $("#query_result_draw_table").JsonTable(query_table_meta);
    $("#query_result_lost_table").JsonTable(query_table_meta);
});