package com.foodrecogn.foodrecognition.DataBase;

import android.arch.persistence.room.Room;
import android.content.Context;

import com.foodrecogn.foodrecognition.Model.PhotoInfo;
import com.foodrecogn.foodrecognition.Model.User;

import java.io.Serializable;
import java.util.List;

public class DataBase implements Serializable {
    private static final String DATABASE_NAME = "data_base";
    private DataBaseOps dataBaseOps;

    public DataBase(Context appContext){
        dataBaseOps = Room.databaseBuilder(appContext.getApplicationContext(),
                DataBaseOps.class,
                DATABASE_NAME).fallbackToDestructiveMigration().build();
    }

    public void addUserToDB(User user){
        // user is valid
        dataBaseOps.userDaoAccess().insertUser(user);
    }

    public void addPhotoInfo(PhotoInfo photoInfo){
        dataBaseOps.photoInfoDaoAccess().insertPhotInfo(photoInfo);
    }

    public User getUser(String username){
        return dataBaseOps.userDaoAccess().getUserFromDB(username);
    }

    public PhotoInfo getPhotoInfo(String filename){
        return dataBaseOps.photoInfoDaoAccess().getPhotoInfo(filename);
    }

    public List<PhotoInfo> getAllPhotoInfo(String username){
        return dataBaseOps.photoInfoDaoAccess().getAllPhotoInfoForUser(username);
    }

    public User updateUser(User user){
        dataBaseOps.userDaoAccess().updateUser(user);
        return dataBaseOps.userDaoAccess().getUserFromDB(user.getUsername());
    }

    public PhotoInfo updatePhotoInfo(PhotoInfo photoInfo){
        dataBaseOps.photoInfoDaoAccess().updatePhotoInfo(photoInfo);
        return dataBaseOps.photoInfoDaoAccess().getPhotoInfo(photoInfo.getFilename());
    }

}
