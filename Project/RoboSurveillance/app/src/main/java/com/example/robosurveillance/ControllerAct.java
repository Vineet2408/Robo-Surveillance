package com.example.robosurveillance;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class ControllerAct extends AppCompatActivity {

    ImageView frameView;
    Button connectBtn,playBtn,sendCmdBtn;
    Bitmap last;
    Socket socket;
    TextView statusTextView;
    EditText commandEditText;

    Handler handler;
    Bitmap i[];
    int counter=0;
    ClientConnect cc;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view);

        Intent in=getIntent();
        Window window=getWindow();
        window.setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);
        String ip=in.getStringExtra("ip");
        String port=in.getStringExtra("port");
        int portNumber=Integer.parseInt(port);

        cc=new ClientConnect(portNumber,ip);
        final Thread[] t = new Thread[1];

        frameView=findViewById(R.id.controllerView);
        playBtn=findViewById(R.id.playBtn);
        sendCmdBtn=findViewById(R.id.sendCmdBtn);
        commandEditText=findViewById(R.id.commandText);
        connectBtn=findViewById(R.id.ControllerConnectBtn);
        statusTextView=findViewById(R.id.statusTextView);

        handler=new Handler();

        connectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try{
                    t[0] =new Thread(cc);
                    t[0].start();
                }
                catch (Exception e)
                {
                    Toast.makeText(ControllerAct.this, "error in connection ", Toast.LENGTH_SHORT).show();
                }

            }
        });
        playBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try{
                    socket=cc.getClientSocket();
                    statusTextView.setText(ClientConnect.getStatus());
                    ClientThread ct=new ClientThread();
                    Thread t = new Thread(ct);
                    t.start();

                }
                catch (Exception e)
                {
                    Toast.makeText(ControllerAct.this, e.getMessage()+"playBtn", Toast.LENGTH_SHORT).show();
                }
            }
        });

        sendCmdBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {

                    cc.writeToServer(commandEditText.getText().toString());
                } catch (Exception e) {
                    Toast.makeText(ControllerAct.this, e.getMessage() + "sendBtn", Toast.LENGTH_SHORT).show();
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
                Toast.makeText(ControllerAct.this, "error in connection of receiving", Toast.LENGTH_SHORT).show();
                e.printStackTrace();
            }
        }
    }

    protected class Downloading extends AsyncTask<Void,Void,Void>
    {

        InputStream is;
        //999414,6841390
        Bitmap bitim;

        @Override
        protected Void doInBackground(Void... voids)
        {
            i=new Bitmap[1000];

            while(true)
            {
                byte imbyte[]=new byte[6841390];
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {

                    is=socket.getInputStream();
                    is.read(imbyte,0,imbyte.length);

                } catch (Exception e) {
                    Toast.makeText(ControllerAct.this, e.getMessage()+"input vali", Toast.LENGTH_LONG).show();
                    e.printStackTrace();
                }

                try {

                    Bitmap b= BitmapFactory.decodeByteArray(imbyte,0,imbyte.length);
                    bitim=b;
                }
                catch (Exception e)
                {
                    handler.post(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(ControllerAct.this, "IllegalStateException cannot decode", Toast.LENGTH_SHORT).show();
                        }
                    });
                }

                if(bitim==null)
                {
                    try{

                        handler.post(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(ControllerAct.this, "null object", Toast.LENGTH_SHORT).show();
                            }
                        });

                    }catch (Exception e)
                    {
                        handler.post(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(ControllerAct.this, "width = ", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                }

                i[counter++]=bitim;
                if(counter>4)
                    setImage();

                if(counter>400)
                {
                    counter=0;
                    i=new Bitmap[1000];
                }
            }
        }

        private void setImage()
        {
            handler.post(new Runnable() {
                @Override
                public void run()
                {
                    try
                    {
                      /*  if(i[counter-4]!=null)
                        {
                            last=i[counter-4];
                            frameView.setImageBitmap(last);
                        }
                        else

                            frameView.setImageBitmap(last);*/
                        if(i[counter-4]==null)
                        {
                            frameView.setImageBitmap(i[counter-2]);
                        }
                        else

                            frameView.setImageBitmap(i[counter-4]);
                    }
                    catch (Exception e)
                    {
                        handler.post(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(ControllerAct.this, "this frame was null", Toast.LENGTH_SHORT).show();

                            }
                        });
                    }
                }
            });
        }
    }
}


