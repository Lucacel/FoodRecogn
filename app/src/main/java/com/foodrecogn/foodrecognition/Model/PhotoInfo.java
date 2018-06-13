package com.foodrecogn.foodrecognition.Model;

import android.arch.persistence.room.Entity;
import android.arch.persistence.room.ForeignKey;
import android.arch.persistence.room.Ignore;
import android.arch.persistence.room.PrimaryKey;
import android.support.annotation.NonNull;

import java.io.Serializable;

@Entity(foreignKeys = @ForeignKey(entity =  User.class,
                                            parentColumns = "username",
                                            childColumns = "owner"))
public class PhotoInfo implements Serializable {
    @PrimaryKey
    @NonNull
    private String filename;

    private String label; // name of food
    private String percentage; // chances of being
    private Integer kcal; //kilo calories
    private String date; //date when photo was made

    private String owner;

    @Ignore
    public PhotoInfo(String filename, String label, String percentage, Integer kcal, String date, String owner) {
        this.filename = filename;
        this.label = label;
        this.percentage = percentage;
        this.kcal = kcal;
        this.date = date;
        this.owner = owner;
    }

    public PhotoInfo(String filename, String owner) {
        this.filename = filename;
        this.owner = owner;
        this.kcal = -1;
        this.date = "";
        this.label = "";
        this.percentage = "";
    }

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public String getPercentage() {
        return percentage;
    }

    public void setPercentage(String percentage) {
        this.percentage = percentage;
    }

    public Integer getKcal() {
        return kcal;
    }

    public void setKcal(Integer kcal) {
        this.kcal = kcal;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getOwner() {
        return owner;
    }

    public void setOwner(String owner) {
        this.owner = owner;
    }
}
