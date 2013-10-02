package com.tinyms.oddshistory.data;

import java.text.DecimalFormat;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import android.util.Log;

public class Helper {
	
	public static boolean isDebug = true;
	
	public static void log(String msg){
		if(isDebug){
			Log.d("OddsHistory", msg);
		}
	}
	
	public static String oddsValueEmptyIf(String comName,String comKey,Map<String,String> item){
    	if(!empty(item.get("Odds_"+comKey))){
    		return comName+": "+item.get("Odds_"+comKey)+" ~ "+item.get("Odds_"+comKey+"_Change")+"<br/>";
    	}
		return "";
	}
    
	public static String oddsChangeEmptyIf(String comName,String comKey,Map<String,String> item){
    	if(!empty(item.get("Odds_"+comKey))){
    		return comName+": "+OddsStatistics(item.get("Odds_"+comKey),item.get("Odds_"+comKey+"_Change"))+"<br/>";
    	}
		return "";
    }
    
    public static String oddsModelChangeEmptyIf(String comName,String comKey,Map<String,String> item){
    	if(!empty(item.get("Odds_"+comKey))){
    		String changeModel = OddsModelStatistics(item.get("Odds_"+comKey),item.get("Odds_"+comKey+"_Change"));
	    	if(!"".equals(changeModel)){
	    		return comName+": "+changeModel+"<br/>";
	    	}
    	}
		return "";
    }
	
	public static String OddsStatistics(String oddsStart,String oddsEnd){
    	if(oddsStart==null||oddsStart.equals("")){
    		return "";
    	}
    	StringBuffer diff = new StringBuffer();
    	float[] start_odds = OddsToFloats(oddsStart);
    	float[] end_odds = OddsToFloats(oddsEnd);
    	if((start_odds.length==3) && (end_odds.length==3)){
    		float win_diff = end_odds[0] - start_odds[0];
    		float draw_diff = end_odds[1] - start_odds[1];
    		float lost_diff = end_odds[2] - start_odds[2];
    		
    		if(win_diff>0){
    			diff.append(" <font color='red'>+"+FormatFloatWith2Bit(win_diff)+"</font>");
    		}else if(win_diff<0){
    			diff.append(" <font color='green'>"+FormatFloatWith2Bit(win_diff)+"</font>");
    		}if(win_diff==0){
    			diff.append(" +0.00");
    		}
    		
    		if(draw_diff>0){
    			diff.append(" <font color='red'>+"+FormatFloatWith2Bit(draw_diff)+"</font>");
    		}else if(draw_diff<0){
    			diff.append(" <font color='green'>"+FormatFloatWith2Bit(draw_diff)+"</font>");
    		}if(draw_diff==0){
    			diff.append(" +0.00");
    		}
    		
    		if(lost_diff>0){
    			diff.append(" <font color='red'>+"+FormatFloatWith2Bit(lost_diff)+"</font>");
    		}else if(lost_diff<0){
    			diff.append(" <font color='green'>"+FormatFloatWith2Bit(lost_diff)+"</font>");
    		}if(lost_diff==0){
    			diff.append(" +0.00");
    		}
    	}
    	return diff.toString().trim();
    }
	
	public static boolean empty(String str){
    	if(str==null){
    		return true;
    	}
    	String tmp = str.trim();
    	if("".equals(tmp)){
    		return true;
    	}
    	return false;
    }
	
	public static String FormatFloatWith2Bit(double v){
    	DecimalFormat f = new DecimalFormat("0.00");
    	return f.format(v);
    }
	
	public static String OddsModelStatistics(String oddsStart,String oddsEnd){
    	String start = OddsModel(oddsStart);
    	String end = OddsModel(oddsEnd);
    	if(!start.equals(end)){
    		return start+" -&gt "+end;
    	}
    	return "";
    }
	
	public static String OddsModel(String odds_str){
    	StringBuffer sb = new StringBuffer();
    	Pattern pattern = Pattern.compile("\\d+(?=\\.)");
    	Matcher m = pattern.matcher(odds_str);
    	while(m.find()){
    		sb.append(m.group());
    	}
    	return sb.toString();
    }
	
	public static float[] OddsToFloats(String odds_str){
    	float[] odds = new float[3];
    	if(odds_str!=null&&!"".equals(odds_str)){
    		String[] items = odds_str.split(" ");
    		odds[0]=Float.parseFloat(items[0]);
    		odds[1]=Float.parseFloat(items[1]);
    		odds[2]=Float.parseFloat(items[2]);
    	}
    	return odds;
    }
    
	public static String GetResultChineseStyle(String result){
    	if("3".equals(result)){
    		return "<font color='red'>胜</font>";
    	}else if("1".equals(result)){
    		return "<font color='green'>平</font>";
    	}else if("0".equals(result)){
    		return "<font color='blue'>负</font>";
    	}
    	return "";
    }
	
}

