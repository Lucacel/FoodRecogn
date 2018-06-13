package com.foodrecogn.foodrecognition.Model;

import java.io.Serializable;
import java.util.ArrayList;

public class GraphInfo implements Serializable {
    private ArrayList<PhotoInfo> photoInfos = new ArrayList<>();

    public void addPhoto(PhotoInfo photoInfo){
        if (photoInfo.getKcal() >= 0 || !photoInfo.getDate().equals("")){
            photoInfos.add(photoInfo);
        }
    }

    public void removePhoto(String filename){
        for (PhotoInfo p : photoInfos){
            if (p.getFilename().equals(filename))
                photoInfos.remove(p);
        }
    }

    public ArrayList<PhotoInfo> getPhotoInfos(){
        return photoInfos;
    }

    public PhotoInfo getPhotoInfo(String filename){
        for (PhotoInfo p : photoInfos){
            if (p.getFilename().equals(filename))
                return p;
        }
        return null;
    }

}
