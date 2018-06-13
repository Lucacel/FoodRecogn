package com.foodrecogn.foodrecognition;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends Activity {
    Button loginBtn;
    Button registerBtn;
    EditText usernameEditText;
    EditText passwordEditText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_layout);


        loginBtn = findViewById(R.id.login_btn);
        registerBtn = findViewById(R.id.register_btn);
        usernameEditText = findViewById(R.id.username_editText);
        passwordEditText = findViewById(R.id.password_editText);

        RequestQueue queue = Volley.newRequestQueue(this);
        final String url = "http://127.0.0.1:8086/login";



        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(final View view) {
                String username = usernameEditText.getText().toString();
                String password = passwordEditText.getText().toString();

                Map<String, String> params = new HashMap();
                params.put("username", username);
                params.put("passowrd", password);
                JSONObject parameters = new JSONObject(params);

                if (username.equals("admin") && password.equals("admin")){
                    Intent intent = new Intent(view.getContext(), MainActivity.class);
                    startActivity(intent);
                }
                else if (!username.isEmpty()&&!password.isEmpty())
                {

                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                            Request.Method.POST, url, parameters, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Toast.makeText(view.getContext(), response.toString(), Toast.LENGTH_LONG).show();
                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Toast.makeText(view.getContext(), error.toString(), Toast.LENGTH_LONG).show();
                        }
                    }
                    );
                    Volley.newRequestQueue(view.getContext()).add(jsonObjectRequest);

                }
                else {
                    Toast.makeText(view.getContext(), "error", Toast.LENGTH_SHORT).show();
                }
            }
        });



        registerBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(view.getContext(), RegisterActivity.class);
                startActivity(intent);
            }
        });


    }
}
