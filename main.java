import com.fazecast.jSerialComm.SerialPort;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class ArduinoMonitor extends Application {
    private SerialPort serialPort;
    private Label sensorLabel = new Label("Aguardando dados...");

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        VBox root = new VBox(10, sensorLabel);
        Scene scene = new Scene(root, 300, 200);

        primaryStage.setTitle("Monitor de Sensores");
        primaryStage.setScene(scene);
        primaryStage.show();

        conectarSerial();
    }

    private void conectarSerial() {
        serialPort = SerialPort.getCommPort("COM3"); // Altere para a porta correta
        serialPort.setBaudRate(9600);
        serialPort.setComPortTimeouts(SerialPort.TIMEOUT_READ_BLOCKING, 0, 0);

        if (serialPort.openPort()) {
            System.out.println("Conectado à porta serial.");
            Thread leituraThread = new Thread(this::lerDadosSerial);
            leituraThread.setDaemon(true);
            leituraThread.start();
        } else {
            System.out.println("Falha ao conectar à porta serial.");
        }
    }

    private void lerDadosSerial() {
        try (InputStream in = serialPort.getInputStream()) {
            byte[] buffer = new byte[1024];
            while (true) {
                int len = in.read(buffer);
                if (len > 0) {
                    String dado = new String(buffer, 0, len, StandardCharsets.UTF_8).trim();
                    Platform.runLater(() -> sensorLabel.setText("Sensor: " + dado));
                    System.out.println("Recebido: " + dado);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void stop() {
        if (serialPort != null && serialPort.isOpen()) {
            serialPort.closePort();
            System.out.println("Porta serial fechada.");
        }
    }
}