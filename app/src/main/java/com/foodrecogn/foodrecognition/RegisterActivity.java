package com.foodrecogn.foodrecognition;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class RegisterActivity extends Activity {

    Button r_login_btn;
    Button r_register_btn;
    EditText r_username_editText;
    EditText r_password_editText;
    EditText r_email_editText;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register_activity);


        r_login_btn = findViewById(R.id.r_login_btn);
        r_register_btn = findViewById(R.id.r_register_btn);
        r_username_editText = findViewById(R.id.r_username_editText);
        r_password_editText = findViewById(R.id.r_password_editText);
        r_email_editText = findViewById(R.id.r_email_editText);

        r_login_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(view.getContext(), LoginActivity.class);
                startActivity(intent);
            }
        });


    }
}
