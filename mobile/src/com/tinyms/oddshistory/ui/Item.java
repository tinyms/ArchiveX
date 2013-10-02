package com.tinyms.oddshistory.ui;

public class Item {
	String id;
    String title;
    int iconRes;

    Item(String title_, int iconRes_, String id_) {
    	id = id_;
    	title = title_;
    	iconRes = iconRes_;
    }

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public int getIconRes() {
		return iconRes;
	}

	public void setIconRes(int iconRes) {
		this.iconRes = iconRes;
	}

}
