package com.foodrecogn.foodrecognition.DataBase;

import android.arch.persistence.room.Database;
import android.arch.persistence.room.RoomDatabase;

import com.foodrecogn.foodrecognition.Model.PhotoInfo;
import com.foodrecogn.foodrecognition.Model.User;

import java.io.Serializable;

@Database(entities = {User.class, PhotoInfo.class}, version = 1, exportSchema = false)
public abstract class DataBaseOps extends RoomDatabase  implements Serializable{
    public abstract UserDao userDaoAccess();
    public abstract PhotoInfoDao photoInfoDaoAccess();
}
