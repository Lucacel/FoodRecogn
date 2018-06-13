package com.foodrecogn.foodrecognition.DataBase;

import android.arch.persistence.room.Dao;
import android.arch.persistence.room.Insert;
import android.arch.persistence.room.Query;
import android.arch.persistence.room.Update;

import com.foodrecogn.foodrecognition.Model.User;

@Dao
public interface UserDao {

    @Insert
    void insertUser(User user);

    @Query("SELECT * FROM User WHERE username = :username")
    User getUserFromDB(String username);

    @Update
    void updateUser(User user);

}
