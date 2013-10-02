package com.tinyms.oddshistory.data;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class Query {
	//Global Params
	public static String P_EVENT_NAME = "";
	public static String P_DETECT_RESULT = "";//detect_result
	public static String P_RESULT = "";
	public static String P_MODEL = "";
	//End
	public static String DB_NAME = "matchs";
	public static List<Map<String,String>> matchs_dataset = new ArrayList<Map<String,String>>();
	
	public static String DatabasePath(){
    	File SDFile = android.os.Environment.getExternalStorageDirectory();
    	return SDFile.getAbsolutePath()  
                + File.separator + DB_NAME;
    }
	
	public static void CheckDatabse(InputStream is){
    	String state = android.os.Environment.getExternalStorageState();
    	if (state.equals(android.os.Environment.MEDIA_MOUNTED)) {
    		File myFile = new File(DatabasePath());
    		if (!myFile.exists()) { 
    			try {
    				//InputStream is = getBaseContext().getAssets().open(DB_NAME);
    				OutputStream os = new FileOutputStream(myFile);
    				byte[] buffer = new byte[1024];
    				int length;
    				while ((length = is.read(buffer)) > 0) {
    					os.write(buffer, 0, length);
    				}
    				os.flush();
    				os.close();
    				is.close();
    			} catch (Exception e) {
    				//Log.v(LogKey, e.getMessage());
    			}
            }else{
            	if(Helper.isDebug){
            		myFile.delete();
            		CheckDatabse(is);
            	}
            }
    	}
    }
	
	public static String paramValue(String prefix,String key){
		if(key.indexOf(prefix)!=-1){
			return key.replace(prefix, "").trim();
		}
		return "";
	}
	
	public static void list(Context context){
    	matchs_dataset.clear();
    	SQLite sql = new SQLite(context,DatabasePath(),null,3);
    	SQLiteDatabase db = sql.getReadableDatabase();
    	String querySQL = "SELECT a.id,a.score,a.actual_result,a.detect_result,a.balls_diff,a.vs_team," +
    			"a.last_mix,a.last_10,a.last_6,a.last_4,a.last_mix_battle,a.last_battle,a.url_key,a.vs_date,a.evt_name,"
    			+ "b.r_3,b.r_1,b.r_0,abs(b.r_3-b.r_0) as model FROM lottery_battle as a LEFT OUTER JOIN lottery_odds as b ON a.id=b.battle_id WHERE b.com_name='WL' ";
		/*动态查询*/
    	if(!Helper.empty(P_EVENT_NAME)){
    		querySQL += " AND evt_name = '"+P_EVENT_NAME+"'";
    	}
    	if(!Helper.empty(P_DETECT_RESULT)){
    		if("1".equals(P_DETECT_RESULT)){
    			querySQL += " AND detect_result like '1%'";
    		}else{
    			querySQL += " AND detect_result = '"+P_DETECT_RESULT+"'";
    		}
    	}
    	if(!Helper.empty(P_RESULT)){
    		querySQL += " AND actual_result = "+P_RESULT;
    	}
    	
    	if(!Helper.empty(P_MODEL)){
    		if("deep".equals(P_MODEL)){
    			querySQL += " AND model >= 4";
    		}else{
    			querySQL += " AND model < 4";
    		}
    	}
    	/*End 动态查询*/
    	querySQL+=" ORDER BY RANDOM() LIMIT 14";
    	Cursor c = db.rawQuery(querySQL, null);
    	c.moveToFirst();
    	while(!c.isAfterLast()){
    		Map<String,String> item = new HashMap<String,String>();
    		item.put("id", String.valueOf(c.getInt(0)));
    		item.put("score", c.getString(1));
    		item.put("actual_result", String.valueOf(c.getInt(2)));
    		item.put("detect_result", c.getString(3));
    		item.put("balls_diff", String.valueOf(c.getDouble(4)));
    		item.put("vs_team", c.getString(5));
    		item.put("last_mix", c.getString(6));
    		item.put("last_10", c.getString(7));
    		item.put("last_6", c.getString(8));
    		item.put("last_4", c.getString(9));
    		item.put("last_mix_battle", c.getString(10));
    		item.put("last_battle", c.getString(11));
    		item.put("url_key", c.getString(12));
    		item.put("vs_date", c.getString(13));
    		item.put("evt_name", c.getString(14));
    		item.put("wl_odds", Helper.FormatFloatWith2Bit(c.getDouble(15))+" "+Helper.FormatFloatWith2Bit(c.getDouble(16))+" "+Helper.FormatFloatWith2Bit(c.getDouble(17)));
    		
    		item.put("ItemTitle", "["+item.get("evt_name")+"] "+item.get("vs_team"));
    		StringBuffer sb_tip = new StringBuffer();
			sb_tip.append("("+Helper.GetResultChineseStyle(item.get("actual_result"))+") 实力: <font color='#336699'>"+item.get("balls_diff")+"</font>");
			sb_tip.append(" 预测: <font color='#FF0033'>"+item.get("detect_result")+"</font>");
			sb_tip.append(" 初陪: "+ item.get("wl_odds"));
    		item.put("ItemText", sb_tip.toString());
    		matchs_dataset.add(item);
    		c.moveToNext();
    	}
    	c.close();
    	db.close();
    }
	
	public static void details(Map<String,String> item, Context context){
    	String sql = "SELECT com_name,r_3,r_1,r_0,r_3_c,r_1_c,r_0_c FROM lottery_odds WHERE battle_id=?";
    	SQLite sqlite = new SQLite(context ,DatabasePath(),null,3);
    	SQLiteDatabase db = sqlite.getReadableDatabase();
    	Cursor c = db.rawQuery(sql, new String[]{item.get("id")});
    	c.moveToFirst();
    	while(!c.isAfterLast()){
    		String name = c.getString(0);
    		String r_3 = String.valueOf(Helper.FormatFloatWith2Bit(c.getDouble(1)));
    		String r_1 = String.valueOf(Helper.FormatFloatWith2Bit(c.getDouble(2)));
    		String r_0 = String.valueOf(Helper.FormatFloatWith2Bit(c.getDouble(3)));
    		String r_3_c = String.valueOf(Helper.FormatFloatWith2Bit(c.getDouble(4)));
    		String r_1_c = String.valueOf(Helper.FormatFloatWith2Bit(c.getDouble(5)));
    		String r_0_c = String.valueOf(Helper.FormatFloatWith2Bit(c.getDouble(6)));
    		if("WL".equals(name)){
    			item.put("Odds_WL", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_WL_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("LB".equals(name)){
    			item.put("Odds_LB", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_LB_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("YB".equals(name)){
    			item.put("Odds_YSB", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_YSB_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("BT".equals(name)){
    			item.put("Odds_365", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_365_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("AM".equals(name)){
    			item.put("Odds_AM", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_AM_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("Inerwetten".equals(name)){//other
    			item.put("Odds_Inerwetten", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_Inerwetten_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("HG".equals(name)){
    			item.put("Odds_HG", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_HG_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("WD".equals(name)){
    			item.put("Odds_WD", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_WD_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("Bwin".equals(name)){
    			item.put("Odds_Bwin", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_Bwin_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}else if("10bet".equals(name)){
    			item.put("Odds_10bet", r_3+" "+r_1+" "+r_0);
    			item.put("Odds_10bet_Change", r_3_c+" "+r_1_c+" "+r_0_c);
    		}
    		c.moveToNext();
    	}
    	c.close();
    	db.close();
    }
}
