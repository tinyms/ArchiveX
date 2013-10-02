package com.tinyms.oddshistory.ui;

import net.simonvt.menudrawer.MenuDrawer;
import net.simonvt.menudrawer.Position;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;

import com.tinyms.oddshistory.R;

public abstract class BaseMenuDrawer extends FragmentActivity implements MenuAdapter.MenuListener {

    private static final String STATE_ACTIVE_POSITION =
            "net.simonvt.menudrawer.samples.LeftDrawerSample.activePosition";

    protected MenuDrawer mMenuDrawer;

    protected MenuAdapter mAdapter;
    protected ListView mList;

    private int mActivePosition = 0;

    @Override
    protected void onCreate(Bundle inState) {
        super.onCreate(inState);

        if (inState != null) {
            mActivePosition = inState.getInt(STATE_ACTIVE_POSITION);
        }

        mMenuDrawer = MenuDrawer.attach(this, MenuDrawer.Type.BEHIND, getDrawerPosition(), getDragMode());

        List<Object> items = new ArrayList<Object>();
        items.add(new Item("不限定", R.drawable.ic_action_refresh_dark, "quick_random"));
        items.add(new Item("同球队对阵", R.drawable.ic_action_select_all_dark, "quick_same_team_battle"));
        items.add(new Category("赛果"));
        items.add(new Item("主胜", R.drawable.ic_action_select_all_dark, "result_3"));
        items.add(new Item("平", R.drawable.ic_action_select_all_dark, "result_1"));
        items.add(new Item("主负", R.drawable.ic_action_select_all_dark, "result_0"));
        items.add(new Category("实力差"));
        items.add(new Item("主胜", R.drawable.ic_action_select_all_dark, "diff_3"));
        items.add(new Item("主平", R.drawable.ic_action_select_all_dark, "diff_1"));
        items.add(new Item("主负", R.drawable.ic_action_select_all_dark, "diff_0"));
        items.add(new Item("主不败", R.drawable.ic_action_select_all_dark, "diff_31"));
        items.add(new Item("客不败", R.drawable.ic_action_select_all_dark, "diff_01"));
        items.add(new Category("盘路"));
        items.add(new Item("深盘", R.drawable.ic_action_select_all_dark, "odds_model_deep"));
        items.add(new Item("浅盘", R.drawable.ic_action_select_all_dark, "odds_model_shallow"));
        items.add(new Category("选择场数"));
        items.add(new Item("14场", R.drawable.ic_action_select_all_dark, "select_match_num_14"));
        items.add(new Item("20场", R.drawable.ic_action_select_all_dark, "select_match_num_20"));
        items.add(new Item("30场", R.drawable.ic_action_select_all_dark, "select_match_num_30"));
        items.add(new Category("热门联赛"));
        items.add(new Item("不限定", R.drawable.ic_action_select_all_dark, "event_name_"));
        items.add(new Item("意甲", R.drawable.ic_action_select_all_dark, "event_name_意甲"));
        items.add(new Item("英超", R.drawable.ic_action_select_all_dark, "event_name_英超"));
        items.add(new Item("西甲", R.drawable.ic_action_select_all_dark, "event_name_西甲"));
        items.add(new Item("西乙", R.drawable.ic_action_select_all_dark, "event_name_西乙"));
        items.add(new Item("德甲", R.drawable.ic_action_select_all_dark, "event_name_德甲"));
        items.add(new Item("英甲", R.drawable.ic_action_select_all_dark, "event_name_英甲"));
        items.add(new Item("英冠", R.drawable.ic_action_select_all_dark, "event_name_英冠"));
        items.add(new Item("法甲", R.drawable.ic_action_select_all_dark, "event_name_法甲"));
        items.add(new Item("法乙", R.drawable.ic_action_select_all_dark, "event_name_法乙"));
        items.add(new Item("德乙", R.drawable.ic_action_select_all_dark, "event_name_德乙"));
        mList = new ListView(this);

        mAdapter = new MenuAdapter(this, items);
        mAdapter.setListener(this);
        mAdapter.setActivePosition(mActivePosition);

        mList.setAdapter(mAdapter);
        mList.setOnItemClickListener(mItemClickListener);

        mMenuDrawer.setMenuView(mList);
    }

    protected abstract void onMenuItemClicked(int position, Item item);

    protected abstract int getDragMode();

    protected abstract Position getDrawerPosition();

    private AdapterView.OnItemClickListener mItemClickListener = new AdapterView.OnItemClickListener() {
        @Override
        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
            mActivePosition = position;
            mMenuDrawer.setActiveView(view, position);
            mAdapter.setActivePosition(position);
            onMenuItemClicked(position, (Item) mAdapter.getItem(position));
        }
    };

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putInt(STATE_ACTIVE_POSITION, mActivePosition);
    }

    @Override
    public void onActiveViewChanged(View v) {
        mMenuDrawer.setActiveView(v, mActivePosition);
    }
}
