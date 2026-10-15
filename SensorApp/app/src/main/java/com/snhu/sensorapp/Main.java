package com.snhu.sensorapp;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;

public class Main extends AppCompatActivity implements SensorEventListener{
    // Controls for the text views
    private TextView luxDisplayText;
    private TextView luxDisplayMax;
    private TextView luxDisplayMin;
    private TextView luxDisplayAve;
    private TextView gameStatus;


    // Sensors
    private SensorManager sensorManager;
    private Sensor lightSensor;
    private Boolean isTempSensorAvail;

    // Data fields
    private float luxMax = 0;
    private float luxMin = 100;
    private float luxAverage = 0;

    // The target value for the game
    double targetValue = 55;

    // Setting the tolerance high initially
    double tolerance = 0.25;

    // getting the upper and lower bounds of the toloerance
    double targetHigh = targetValue * (1 + tolerance);
    double targetLow  = targetValue * (1 - tolerance);

    /*
    * Initializing the activity and application startup
    */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initializing the textViews and buttons
        luxDisplayText = findViewById(R.id.sensorReading);
        luxDisplayMax= findViewById(R.id.sensorMax);
        luxDisplayMin = findViewById(R.id.sensorMin);
        luxDisplayAve = findViewById(R.id.sensorAverage);
        gameStatus = findViewById(R.id.gameStatus);


        // Reset values on the Reset button press.
        Button resetValuesBtn;
        resetValuesBtn = findViewById(R.id.reset_min_max);
        resetValuesBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                luxMax = 0;
                luxMin = 999;
                luxAverage = 0;
                targetValue = 55;
                luxDisplayMax.setText(luxMax + "");
                luxDisplayMin.setText(luxMin + "");
                luxDisplayAve.setText("0.0");
            }
        });

        // Initializes the connection to the phones sensor system
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        // setting the type of sensor
        lightSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);

        // Checking if the sensor is available to use
        if (sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT) != null) {
            lightSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
            isTempSensorAvail = true;
        }else{
            luxDisplayText.setText("Sensor is not available");
            isTempSensorAvail = false;
        }

    }

    /*
    * Register the sensor listener when the app is resumed
    */
    @Override
    protected void onResume() {
        super.onResume();
        if (isTempSensorAvail) {
            sensorManager.registerListener(this, lightSensor, SensorManager.SENSOR_DELAY_FASTEST);
        }
    }


    /*
    *  Pausing the sensor listener when the app is not in use
    */
    @Override
    protected void onPause() {
        super.onPause();
        sensorManager.unregisterListener(this);
    }

    // Method not used but required by SensorEventListener interface
    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }


    /*
    * The sensor value change event
    * This method runs anytime there is an update the photosensor
    */
    @Override
    public void onSensorChanged(SensorEvent event) {

        // Determine max value
        if (event.values[0] > luxMax){
            luxMax = event.values[0];
        }

        // Determine the min value
        if (event.values[0] < luxMin && event.values[0] > 0){
            luxMin = event.values[0];
        }

        // Uncomment to display just the value
        luxDisplayText.setText(String.format("%.4f", event.values[0])+" Lux");

        // Display the values
        luxDisplayMax.setText(String.format("%.4f", luxMax));
        luxDisplayMin.setText(String.format("%.4f", luxMin));
        luxAverage = (luxMax - luxMin)/2;
        luxDisplayAve.setText(String.format("%.4f", luxAverage));

        // Small challange to try to capture a specific brightness in a room
        if ((event.values[0] >= targetLow) && (event.values[0] <= targetHigh)){
            gameStatus.setText("You nailed it!!");
        }else{
            if (event.values[0] > targetLow){
                gameStatus.setText("Too Bright - Keep Trying");
            }else{
                gameStatus.setText("Too Dark - Keep Trying");
            }
        }
    }
}