package com.foodrecogn.foodrecognition.DataBase;

import android.arch.persistence.room.Dao;
import android.arch.persistence.room.Insert;
import android.arch.persistence.room.Query;
import android.arch.persistence.room.Update;

import com.foodrecogn.foodrecognition.Model.PhotoInfo;

import java.util.List;

@Dao
public interface PhotoInfoDao {

    @Insert
    void insertPhotInfo(PhotoInfo photoInfo);

    @Query("SELECT * FROM PhotoInfo WHERE owner = :username")
    List<PhotoInfo> getAllPhotoInfoForUser(String username);

    @Query("SELECT * FROM PhotoInfo WHERE filename = :filename")
    PhotoInfo getPhotoInfo(String filename);

    @Update
    void updatePhotoInfo(PhotoInfo photoInfo);

}
