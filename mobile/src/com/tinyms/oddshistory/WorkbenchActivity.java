package com.tinyms.oddshistory;

import java.io.IOException;
import java.util.Map;

import com.tinyms.oddshistory.data.Helper;
import com.tinyms.oddshistory.data.MatchAdapter;
import com.tinyms.oddshistory.data.Query;
import com.tinyms.oddshistory.ui.BaseMenuDrawer;
import com.tinyms.oddshistory.ui.DetailsActivity;
import com.tinyms.oddshistory.ui.Item;

import net.simonvt.menudrawer.MenuDrawer;
import net.simonvt.menudrawer.Position;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.SeekBar;
import android.widget.Toast;

public class WorkbenchActivity extends BaseMenuDrawer {
	
	public static String LogKey = "OddsHistory";
	private MatchAdapter matchs = null;
	
    @Override
    protected void onCreate(Bundle inState) {
        super.onCreate(inState);
        try {
			Query.CheckDatabse(getBaseContext().getAssets().open(Query.DB_NAME));
		} catch (IOException e) {
			e.printStackTrace();
		}
        
        mMenuDrawer.setContentView(R.layout.activity_contentsample);
        mMenuDrawer.setTouchMode(MenuDrawer.TOUCH_MODE_FULLSCREEN);
        mMenuDrawer.setSlideDrawable(R.drawable.ic_drawer);
        mMenuDrawer.setDrawerIndicatorEnabled(true);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.ICE_CREAM_SANDWICH) {
            getActionBar().setDisplayHomeAsUpEnabled(true);
        }
        
        RelativeLayout bottomLayout = (RelativeLayout)findViewById(R.id.MainButtomBarLayout);
        bottomLayout.getBackground().setAlpha(200);
        ListView matchs_grid = (ListView)findViewById(R.id.listView_matchs);
        matchs_grid.setOnItemClickListener(new OnItemClickListener(){

			@Override
			public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,
					long id) {
				// 弹出详细页面
				Map<String,String> item = (Map<String,String>)Query.matchs_dataset.get(Integer.valueOf(String.valueOf(id)));
				Query.details(item,WorkbenchActivity.this);
				StringBuffer sb_strike = new StringBuffer();
				sb_strike.append("总10场: "+item.get("last_mix")+"<br/>");
				sb_strike.append("近10场: "+item.get("last_10")+"<br/>");
				sb_strike.append("近06场: "+item.get("last_6")+"<br/>");
				sb_strike.append("近04场: "+item.get("last_4")+"<br/>");
				
				String text_strike = sb_strike.toString();
				StringBuffer sb_tip = new StringBuffer();
				sb_tip.append("实力: <font color='#336699'>"+item.get("balls_diff")+"</font>");
				sb_tip.append(" 预测: <font color='#FF0033'>"+item.get("detect_result")+"</font>");
				sb_tip.append(" 赛果: "+Helper.GetResultChineseStyle(item.get("actual_result"))+" <font color='#CC6600'>"+item.get("score")+"</font><br/>");
				text_strike += "<br/>总6场战绩: <font color='#003366'>"+item.get("last_mix_battle")+"</font>";
				text_strike += "<br/>近6场战绩: <font color='#003366'>"+item.get("last_battle")+"</font><br/><br/>";
				text_strike += sb_tip.toString();
				
				StringBuffer sb = new StringBuffer();
				sb.append(Helper.oddsValueEmptyIf("威廉","WL",item));
				sb.append(Helper.oddsValueEmptyIf("立博","LB",item));
				sb.append(Helper.oddsValueEmptyIf("韦德","WD",item));
				sb.append(Helper.oddsValueEmptyIf("贝塔","365",item));
				sb.append(Helper.oddsValueEmptyIf("必赢","Bwin",item));
				sb.append(Helper.oddsValueEmptyIf("因特","Inerwetten",item));
				sb.append(Helper.oddsValueEmptyIf("易博","YSB",item));
				sb.append(Helper.oddsValueEmptyIf("澳门","AM",item));
				//sb.append(oddsValueEmptyIf("皇冠","HG",item));
				
				
				//sb.append(oddsValueEmptyIf("十贝","10bet",item));
				sb.append("<br/>");
				sb.append(Helper.oddsChangeEmptyIf("威廉","WL",item));
				sb.append(Helper.oddsChangeEmptyIf("立博","LB",item));
				sb.append(Helper.oddsChangeEmptyIf("韦德","WD",item));
				sb.append(Helper.oddsChangeEmptyIf("贝塔","365",item));
				sb.append(Helper.oddsChangeEmptyIf("必赢","Bwin",item));
				sb.append(Helper.oddsChangeEmptyIf("因特","Inerwetten",item));
				sb.append(Helper.oddsChangeEmptyIf("易博","YSB",item));
				sb.append(Helper.oddsChangeEmptyIf("澳门","AM",item));
				//sb.append(oddsChangeEmptyIf("皇冠","HG",item));
				
				
				//sb.append(oddsChangeEmptyIf("十贝","10bet",item));
//				sb.append("<br/>");
//				sb.append(oddsModelChangeEmptyIf("威廉","WL",item));
//				sb.append(oddsModelChangeEmptyIf("立博","LB",item));
//				sb.append(oddsModelChangeEmptyIf("易博","YSB",item));
//				sb.append(oddsModelChangeEmptyIf("贝塔","365",item));
//				sb.append(oddsModelChangeEmptyIf("澳门","AM",item));
//				sb.append(oddsModelChangeEmptyIf("Iner","Inerwetten",item));
//				sb.append(oddsModelChangeEmptyIf("皇冠","HG",item));
//				sb.append(oddsModelChangeEmptyIf("韦德","WD",item));
//				sb.append(oddsModelChangeEmptyIf("Bwin","Bwin",item));
//				sb.append(oddsModelChangeEmptyIf("10bet","10bet",item));
				
				Intent intent = new Intent(WorkbenchActivity.this,DetailsActivity.class);
				intent.putExtra(DetailsActivity.KEY_STRIKE, text_strike);
				intent.putExtra(DetailsActivity.KEY_ODDS, sb.toString());
				intent.putExtra(DetailsActivity.KEY_TEAM_NAMES_TITLE, "["+item.get("evt_name")+"] "+item.get("vs_team"));
				startActivity(intent);
			}
        	
        });
        
        mMenuDrawer.setOnInterceptMoveEventListener(new MenuDrawer.OnInterceptMoveEventListener() {
            @Override
            public boolean isViewDraggable(View v, int dx, int x, int y) {
                return v instanceof SeekBar;
            }
        });
        
        ImageButton refresh = (ImageButton)findViewById(R.id.btn_310_search);
        refresh.setClickable(true);
        refresh.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View arg0) {
				load_data();
			}});
        
        matchs = new MatchAdapter(this);
        matchs.setMatchData(Query.matchs_dataset);
        matchs_grid.setAdapter(matchs);
        
        load_data();
        
    }
    
    private void load_data(){
    	Query.list(WorkbenchActivity.this);
    	matchs.notifyDataSetChanged();
    	Nodify("已更换新的一批");
    }
    
    private void Nodify(String msg){
    	Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onMenuItemClicked(int position, Item item) {
    	String key = item.getId();
    	Helper.log(key);
    	Query.P_EVENT_NAME = Query.paramValue("event_name_", key);
    	Query.P_DETECT_RESULT = Query.paramValue("diff_", key);
    	Query.P_RESULT = Query.paramValue("result_", key);
    	//v = Query.paramValue("quick_", key);
    	this.load_data();
        mMenuDrawer.closeMenu();
    }

    @Override
    protected int getDragMode() {
        return MenuDrawer.MENU_DRAG_CONTENT;
    }

    @Override
    protected Position getDrawerPosition() {
        return Position.LEFT;
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                mMenuDrawer.toggleMenu();
                return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onBackPressed() {
        final int drawerState = mMenuDrawer.getDrawerState();
        if (drawerState == MenuDrawer.STATE_OPEN || drawerState == MenuDrawer.STATE_OPENING) {
            mMenuDrawer.closeMenu();
            return;
        }

        super.onBackPressed();
    }

}
