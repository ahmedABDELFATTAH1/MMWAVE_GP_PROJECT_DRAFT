/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.PrintStream;
import java.net.Socket;
import org.java_websocket.WebSocketImpl;


/**
 *
 * @author Genschow
 */
public class Com2WebSocketGUI extends javax.swing.JFrame {
    private ComListenClass comListener;
    private SiraGuiWebserver webSockServ;
    private Socket tcpClient;
    private DataInputStream input;
    //private PrintStream output;
    private DataOutputStream output;
    private UpdateThread updater;// = new UpdateThread();
    /**
     * Creates new form Com2WebSocketGUI
     */
    public Com2WebSocketGUI() {
        initComponents();
        comListener = new ComListenClass();
	//WebSocketImpl.DEBUG = true;
        try{
            webSockServ = new SiraGuiWebserver(9090, comListener, input, output);
        } catch (Exception e) {
            e.printStackTrace();
        }
        webSockServ.start();
        System.out.println( "WebServer started on port: " + webSockServ.getPort() );
	comListener.addComReceiveEventListener(new ComRecEvtListener());		

    }
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        comPortComboBox = new javax.swing.JComboBox();
        baudRateComboBox = new javax.swing.JComboBox();
        connectToggleButton = new javax.swing.JToggleButton();
        jPanel2 = new javax.swing.JPanel();
        conTCPButton = new javax.swing.JButton();
        ipTextField = new javax.swing.JTextField();
        portTextField = new javax.swing.JTextField();
        connectedCheckBox = new javax.swing.JCheckBox();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        getContentPane().setLayout(new java.awt.GridLayout(0, 2));

        comPortComboBox.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" }));
        comPortComboBox.setSelectedIndex(4);
        comPortComboBox.setMaximumSize(new java.awt.Dimension(150, 30));
        comPortComboBox.setMinimumSize(new java.awt.Dimension(40, 20));
        comPortComboBox.setPreferredSize(new java.awt.Dimension(50, 25));
        comPortComboBox = comListener.listPorts();

        baudRateComboBox.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "1000000", "921600", "500000", "460800", "230400", "115200", "57600", "19200" }));
        baudRateComboBox.setSelectedIndex(4);
        baudRateComboBox.setMaximumSize(new java.awt.Dimension(150, 15));
        baudRateComboBox.setMinimumSize(new java.awt.Dimension(40, 20));
        baudRateComboBox.setPreferredSize(new java.awt.Dimension(50, 25));

        connectToggleButton.setText("connect");
        connectToggleButton.setMaximumSize(new java.awt.Dimension(150, 30));
        connectToggleButton.setMinimumSize(new java.awt.Dimension(40, 20));
        connectToggleButton.setPreferredSize(new java.awt.Dimension(50, 25));
        connectToggleButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                connectToggleButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addComponent(comPortComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 84, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(4, 4, 4)
                        .addComponent(connectToggleButton, javax.swing.GroupLayout.PREFERRED_SIZE, 84, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(baudRateComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 84, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(comPortComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(connectToggleButton, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(4, 4, 4)
                .addComponent(baudRateComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(235, Short.MAX_VALUE))
        );

        getContentPane().add(jPanel1);

        conTCPButton.setText("connect TCP");
        conTCPButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                conTCPButtonActionPerformed(evt);
            }
        });

        ipTextField.setText("192.168.4.1");

        portTextField.setText("2323");

        connectedCheckBox.setText("connected");
        connectedCheckBox.setEnabled(false);

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addComponent(conTCPButton, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(ipTextField))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(portTextField, javax.swing.GroupLayout.PREFERRED_SIZE, 39, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(connectedCheckBox))
                .addContainerGap(52, Short.MAX_VALUE))
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGap(6, 6, 6)
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(ipTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(portTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(conTCPButton)
                .addGap(18, 18, 18)
                .addComponent(connectedCheckBox)
                .addContainerGap(199, Short.MAX_VALUE))
        );

        getContentPane().add(jPanel2);

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void connectToggleButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_connectToggleButtonActionPerformed
        try{
            if (connectToggleButton.isSelected()) {
                Integer baudrate = Integer.parseInt((String)baudRateComboBox.getSelectedItem());
                String port = (String) (comPortComboBox.getSelectedItem());
                if (comListener.openPort(port, baudrate )  > -1) {
                //                    921600)   > -1) {
            //                    1500000)   > -1) {
            //                    460800)   > -1) {
            //                    470700)   > -1) {
            //                    115200)   > -1) {
            connectToggleButton.setText("Close");
            }
            else
            connectToggleButton.setSelected(false);
            } else {
                connectToggleButton.setText("Open");
                comListener.closePort();
            }
        } catch (Exception e) { 
            e.printStackTrace();
        }
    }//GEN-LAST:event_connectToggleButtonActionPerformed

    private void conTCPButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_conTCPButtonActionPerformed
        try {
            if (tcpClient != null) {
                if (!tcpClient.isClosed()) {
                    output.close();
                    input.close();
                    tcpClient.close();
                    connectedCheckBox.setSelected(false);
                } else connectClient();
            } else connectClient();
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
        
    }//GEN-LAST:event_conTCPButtonActionPerformed

    private void connectClient()
    {
        try{
            tcpClient = new Socket(ipTextField.getText(),Integer.parseInt(portTextField.getText()));
            input = new DataInputStream(tcpClient.getInputStream());
            //output = new PrintStream(tcpClient.getOutputStream());
            output = new DataOutputStream(tcpClient.getOutputStream());
            webSockServ.updateStreams(input, output);
            connectedCheckBox.setSelected(true);
            updater = new UpdateThread();
            updater.start();    
        } catch (Exception e) {System.out.println(e.getMessage());}
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Com2WebSocketGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Com2WebSocketGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Com2WebSocketGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Com2WebSocketGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new Com2WebSocketGUI().setVisible(true);
            }
        });
    }
//receive Events
    class ComRecEvtListener implements ComListenClass.ComRingBufferUpdateEventListener
    {
        public void dataReceived (ComListenClass.ComRingBufferUpdateEvent e)
        {
//do smth with the event			
//			System.out.println(e.eventName);
//			System.out.println(e.inputBuf.toString());
            try{
                webSockServ.sendToAll(e.arrayBuf);
                //System.out.println(e.arrayBuf);
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }		
    }
    
    class UpdateThread extends Thread
    {
            private byte[] buffer = new byte[1024];
            
            public UpdateThread() 
            {
            }

            @Override 
            public void run()
            {
                try{
                    while( tcpClient.isConnected())
                    {                    
                        int read = input.read(buffer);
                        webSockServ.sendToAll(buffer);
//                        String str = new String(buffer);
//                        System.out.println(str);
                    }
                } catch (Exception e) {}
                connectedCheckBox.setSelected(false);
            }
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JComboBox baudRateComboBox;
    private javax.swing.JComboBox comPortComboBox;
    private javax.swing.JButton conTCPButton;
    private javax.swing.JToggleButton connectToggleButton;
    private javax.swing.JCheckBox connectedCheckBox;
    private javax.swing.JTextField ipTextField;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JTextField portTextField;
    // End of variables declaration//GEN-END:variables
}
