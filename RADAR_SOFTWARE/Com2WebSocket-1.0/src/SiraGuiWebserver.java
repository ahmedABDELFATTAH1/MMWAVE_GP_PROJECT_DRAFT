
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Collection;
import org.java_websocket.server.WebSocketServer;
import org.java_websocket.WebSocket;
import org.java_websocket.WebSocketImpl;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.framing.Framedata;

/**
 *
 * @author Genschow
 */
public class SiraGuiWebserver extends WebSocketServer {
    private ComListenClass comPort;
     private DataInputStream input_S;
    private DataOutputStream output_S;
    
    public SiraGuiWebserver( int port, ComListenClass com, DataInputStream input, DataOutputStream output ) throws UnknownHostException {
        super( new InetSocketAddress( port ) );
        comPort = com;
        input_S = input;
        output_S= output;
    }
   
    public SiraGuiWebserver( InetSocketAddress address ) {
        super( address );
    }    
    
    public void updateStreams(DataInputStream input, DataOutputStream output )
    {
        input_S = input;
        output_S= output;    
    }
    
   @Override
    public void onOpen( WebSocket conn, ClientHandshake handshake ) {
        //this.sendToAll( "new connection: " + handshake.getResourceDescriptor() );
        System.out.println( conn.getRemoteSocketAddress().getAddress().getHostAddress() + " entered the room!" );
    }

    @Override
    public void onClose( WebSocket conn, int code, String reason, boolean remote ) {
        //this.sendToAll( conn + " has left the room!" );
        System.out.println( conn + " has left the room!" );
    }

    @Override
    public void onMessage( WebSocket conn, String message ) {
        //this.sendToAll( message );
        //System.out.println( conn + ": " + message );
        if (comPort.isConnected())
            comPort.write(message);
        try{
            output_S.writeBytes(message);
            output_S.flush();
        } catch (Exception e) {}
    }
/*
    @Override
    public void onFragment( WebSocket conn, Framedata fragment ) {
        System.out.println( "received fragment: " + fragment );
    }    
*/
    @Override
    public void onError( WebSocket conn, Exception ex ) {
        ex.printStackTrace();
        if( conn != null ) {
            // some errors like port binding failed may not be assignable to a specific websocket
        }
    }  
    
/**
    * Sends <var>text</var> to all currently connected WebSocket clients.
    * 
    * @param text
    *            The String to send across the network.
    * @throws InterruptedException
    *             When socket related I/O errors occur.
    */
    public void sendToAll( String text ) {
        Collection<WebSocket> con = connections();
           synchronized ( con ) {
                for( WebSocket c : con ) {
                    c.send( text );
                }
           }
   }    

    public void sendToAll( byte[] data ) {
        Collection<WebSocket> con = connections();
           synchronized ( con ) {
                for( WebSocket c : con ) {
                    c.send( data );
                }
        }   
    }  
    
}
