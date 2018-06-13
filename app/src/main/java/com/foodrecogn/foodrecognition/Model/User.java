package com.foodrecogn.foodrecognition.Model;

import android.arch.persistence.room.Entity;
import android.arch.persistence.room.Ignore;
import android.arch.persistence.room.PrimaryKey;
import android.support.annotation.NonNull;

import java.io.Serializable;

@Entity
public class User implements Serializable {
    @PrimaryKey
    @NonNull
    private String username;

    private String password;
    private String email;
    private String first_name;
    private String last_name;
    private String country;
    private Integer points;

    @Ignore
    public User(String username, String password, String email, String first_name, String last_name, String country, Integer points) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.first_name = first_name;
        this.last_name = last_name;
        this.country = country;
        this.points = points;
    }

    public User(String username, String password, String email) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.first_name = "";
        this.last_name = "";
        this.country = "";
        this.points = 0;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirst_name() {
        return first_name;
    }

    public void setFirst_name(String first_name) {
        this.first_name = first_name;
    }

    public String getLast_name() {
        return last_name;
    }

    public void setLast_name(String last_name) {
        this.last_name = last_name;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public Integer getPoints() {
        return points;
    }

    public void setPoints(Integer points) {
        this.points = points;
    }

    @Override
    public String toString() {
        return  "username='" + username + '\'' + '\n' +
                "password='" + password + '\'' + '\n' +
                "email='" + email + '\'' + '\n' +
                "first_name='" + first_name + '\'' + '\n' +
                "last_name='" + last_name + '\'' + '\n' +
                "country='" + country + '\'' + '\n' +
                "points=" + points + '\n';
    }
}
