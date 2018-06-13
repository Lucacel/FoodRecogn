package com.foodrecogn.foodrecognition.Validator;

import com.foodrecogn.foodrecognition.Model.User;

import java.io.Serializable;

public class UserValidator implements Serializable {

    public String validate_user(User user){
        StringBuilder strBuilder = new StringBuilder("");
        if (user.getUsername().isEmpty()) {
            strBuilder.append("Invalid user name. ");
        }
        if (user.getPassword().isEmpty()) {
            strBuilder.append("Invalid password. ");
        }
        if (user.getEmail().isEmpty() || !user.getEmail().contains("@") || !user.getEmail().contains(".")) {
            strBuilder.append("Invalid email. ");
        }
        return strBuilder.toString();
    }

}
