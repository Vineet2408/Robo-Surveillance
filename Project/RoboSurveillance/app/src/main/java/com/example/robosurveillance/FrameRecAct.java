package com.example.robosurveillance;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class FrameRecAct extends AppCompatActivity {


    ImageView frameView;
    Button connectBtn,sendCmdBtn;
    Bitmap last;
    Socket socket;
    TextView statusTextView;

    Handler handler;
    Bitmap i[];
    int counter=0;
    ClientConnect cc;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_frame_rec);
        Intent in=getIntent();
        String ip=in.getStringExtra("ip");
        String port=in.getStringExtra("port");
        int portNumber=Integer.parseInt(port);

        cc=new ClientConnect(portNumber,ip);
        final Thread[] t = new Thread[1];
        handler=new Handler();
        frameView=findViewById(R.id.FrameRecImageView);
        connectBtn=findViewById(R.id.connectFrameRec);
        sendCmdBtn=findViewById(R.id.sendCmdBtn);

        sendCmdBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {

                    cc.writeToServer("hello pi");
                } catch (Exception e) {
                    Toast.makeText(FrameRecAct.this, e.getMessage() + "sendBtn", Toast.LENGTH_SHORT).show();
                }
            }
        });

        connectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                try{
                    t[0] =new Thread(cc);
                    t[0].start();
                    Toast.makeText(FrameRecAct.this, "connected ", Toast.LENGTH_SHORT).show();
                }
                catch (Exception e)
                {
                    Toast.makeText(FrameRecAct.this, e.getMessage()+"error in connection ", Toast.LENGTH_SHORT).show();
                }

            }
        });

        frameView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                try{
                    socket=cc.getClientSocket();

                    ClientThread ct=new ClientThread();
                    Thread t = new Thread(ct);
                    t.start();

                }
                catch (Exception e)
                {
                    Toast.makeText(FrameRecAct.this, e.getMessage()+"playBtn", Toast.LENGTH_SHORT).show();
                }

            }
        });

    }


    public class ClientThread implements Runnable {

        PrintWriter pw;

        @Override
        public void run() {
            try{
                Downloading load=new Downloading();
                load.execute();
            }
            catch (Exception e)
            {
                Toast.makeText(FrameRecAct.this, "error in connection of receiving", Toast.LENGTH_SHORT).show();
                e.printStackTrace();
            }
        }
    }
    protected class Downloading extends AsyncTask<Void,Void,Void>
    {

        InputStream is;
        //999414,6841390
        Bitmap bitim=null;

        Socket socket;

        @SuppressLint("WrongThread")
        @Override
        protected Void doInBackground(Void... voids)
        {

            socket=cc.getClientSocket();
            ObjectInputStream ois=null;
            byte data[];
            try {
                ois = new ObjectInputStream(socket.getInputStream());
            } catch (IOException e) {
                e.printStackTrace();
            }

            while(true)
            {
                try {
                    data = (byte[])ois.readObject();
                    bitim=BitmapFactory.decodeByteArray(data,0,data.length);
                } catch (ClassNotFoundException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                catch(NullPointerException e)
                {
                    e.printStackTrace();
                }


                handler.post(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            frameView.setImageBitmap(bitim);
                            Thread.sleep(600);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        }

    }
}




