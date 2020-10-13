package com.example.robosurveillance;

import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;

import static android.util.Log.e;

public class ClientConnect implements Runnable {
    Socket clientSocket;
    int port;
    String ip;
    BufferedWriter bw;
    ArrayList<String> songs = new ArrayList<>();
    public static String status;

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public ArrayList<String> getSongs() {
        return songs;
    }

    public void setSongs(ArrayList<String> songs) {
        this.songs = songs;
    }

    public static String getStatus() {
        return status;
    }

    public static void setStatus(String status) {
        ClientConnect.status = status;
    }

    public Socket getClientSocket() {
        return clientSocket;
    }

    public void setClientSocket(Socket clientSocket) {
        this.clientSocket = clientSocket;
    }

    public int getHost() {
        return port;
    }

    public void setHost(int port) {
        this.port = port;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public ClientConnect(int port, String ip) {
        this.port = port;
        this.ip = ip;

    }

    public void writeToServer(final String s) {
        final Socket clientSocket1 = this.clientSocket;

        try {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        BufferedWriter bw1 = new BufferedWriter((new OutputStreamWriter(clientSocket1.getOutputStream())));
                        bw1.write(s);
                        bw1.flush();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }
            }).start();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Override
    public void run() {
        InetAddress serverAddr = null;
        try {
            serverAddr = InetAddress.getByName(this.ip);
            this.clientSocket = new Socket(serverAddr, this.port);
            ClientConnect.status = "Connected";
        } catch (Exception e) {
            Log.e("connect with server", "cannot connect");
            System.out.println("cannot connect with server");
            e.printStackTrace();
        }
    }

    public void songList() {
        final Socket cl = this.clientSocket;
        new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    BufferedReader sockIn = new BufferedReader(
                            new InputStreamReader(cl.getInputStream()));

                    while (true) {
                        Thread.sleep(0300);
                        String s = sockIn.readLine();
                        if (s.equalsIgnoreCase("final")) {
                            sockIn.close();
                            e("break", "break");
                            break;
                        }
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                try {
                                    BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(cl.getOutputStream()));
                                    bw.write("ok");
                                    bw.flush();
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();

                        songs.add(s);
                        e("size", String.valueOf(songs.size()) + s);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
}

