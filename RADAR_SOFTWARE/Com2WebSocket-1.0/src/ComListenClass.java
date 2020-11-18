/**
 * ComListenClass.java
 *
 * Created on 28. Mai 2006, 10:18
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */



//import javax.comm.*;
import gnu.io.*;
import java.util.Enumeration;
import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.EventListener;
import java.util.EventObject;
import javax.swing.event.EventListenerList;
import java.util.Arrays;

/**
 *
 * @author Dadita
 */
public class ComListenClass {
    private SerialPort serialPort;
    private CommPortIdentifier portId;
    private OutputStream output;
    private InputStream input;
    private boolean isConnected = false;

	private StringBuffer inputStringBuf = new StringBuffer();

	private final int RINGBUFLEN = 2048; //number must be power of two!!!
        private ArrayList<Byte> byteList = new ArrayList<Byte>(RINGBUFLEN);
	private int ringReadStart = 0;
	private int ringWriteStop = 0;
	
	private EventListenerList listeners = new EventListenerList();
    
    /** Creates a new instance of ComListenClass */
//    public ComListenClass(javax.swing.JTextArea textArea)
    public ComListenClass()
    {
             
    }    
    
    /**collect available serial ports from system
     *and copy their names into a drop down list
     *@return a JComboBox filled with the available ports
     */
    public static javax.swing.JComboBox listPorts()
    {
	/**drop down list*/
	javax.swing.JComboBox comList = new javax.swing.JComboBox();    
	/**list of port identifiers*/
        Enumeration portEnum = CommPortIdentifier.getPortIdentifiers();

	/**print out ports and copy names into list*/
        while ( portEnum.hasMoreElements() ) 
        {
            CommPortIdentifier portIdentifier = (CommPortIdentifier) portEnum.nextElement();
            System.out.println(portIdentifier.getName() + " - " + getPortTypeName(portIdentifier.getPortType()) );
	    comList.addItem(portIdentifier.getName());
        } 
        if (comList.getItemCount()>4)
            comList.setSelectedIndex(4);
	return comList;
    }
    /**convert port identifier to string
     *@param portType port Identifier
     *@return name of specified port type (LPT,COM,...)
     */
    static String getPortTypeName ( int portType )
    {
        switch ( portType )
        {
            case CommPortIdentifier.PORT_PARALLEL:
                return "Parallel";
            case CommPortIdentifier.PORT_SERIAL:
                return "Com";
            default:
                return "unknown type";
        }
    }	
    
    /**
     *
     */
    public int openPort(String identifier, int baudRate)
    {
	try {
	    portId = CommPortIdentifier.getPortIdentifier(identifier);
	    serialPort = (SerialPort) portId.open("SPI Terminal Tester, D.Genschow", 2000);

            serialPort.setInputBufferSize(2000);
            //serialPort.setLowLatency();
            //serialPort.disableReceiveTimeout();

            output = serialPort.getOutputStream();
	    input = new BufferedInputStream(serialPort.getInputStream());
            
            serialPort.addEventListener(new ComListener());
            serialPort.notifyOnDataAvailable(true);

	    serialPort.setSerialPortParams(baudRate,
	    SerialPort.DATABITS_8,
	    SerialPort.STOPBITS_1,
	    SerialPort.PARITY_NONE);
                  

        isConnected = true;
	} catch (NoSuchPortException e) {
//	    logArea.append("\nident: " + e.toString());
	    return -1;
	} catch (PortInUseException e) {
//	    logArea.append("\nopen: " + e.toString());
	    return -1;
	} catch (UnsupportedCommOperationException e) {
//	    logArea.append("\nsetup: " + e.toString());
	    return -1;
        } catch (Exception e) {
//	    logArea.append("\ninstant: " + e.toString());
	    return -1;
	}		
	return 0;
    }

    public boolean isConnected()
    {
        return isConnected;
    }
    
    public void write(char out)
    {
        write((byte)out);
    }
    
    public void write(byte out)
    {
        try{
            output.write(out);
            output.flush();
        } catch (Exception e) 
        {
//            logArea.append(e.getMessage() + "\n");
            e.printStackTrace();
        }
    }
    
    public void write(int[] out)
    {
        try{
            for (int i=0; i<out.length; i++)
            {
                output.write(out[i]);
            }
//            output.write(13); //carriage return
            output.flush();
        } catch (Exception e) 
        {
//            logArea.append(e.getMessage() + "\n");
            e.printStackTrace();
        }
    }
    
    public void write(String out)
    {
        System.out.println("com_write: " + out);
        
        for (int i=0; i<out.length(); i++)
        {
            write(out.getBytes()[i]);
        }    
		
    }

    public void write(String out, char endChar)
    {
        System.out.println(out);
        
        for (int i=0; i<out.length(); i++)
        {
            write(out.getBytes()[i]);
        }    
		write(endChar);
    }
	
	
    /**
     *
     */
    public int closePort()
    {
	try {
	    serialPort.close();
	    input.close();
	    output.close();
        isConnected = false;
	} catch (Exception e) {
//	    logArea.append("\nclose: " + e.getMessage());
	    return -1;
	}	
	return 0;
    }
    
	public void addComReceiveEventListener (ComRingBufferUpdateEventListener listener)
	{
		listeners.add(ComRingBufferUpdateEventListener.class, listener);		
	}
	
	public void removeComReceiveEventListener (ComRingBufferUpdateEventListener listener)
	{
		listeners.remove(ComRingBufferUpdateEventListener.class, listener);
	}
	
	protected synchronized void notifyComReceiveListeners (ComRingBufferUpdateEvent e)
	{
		for (ComRingBufferUpdateEventListener l : listeners.getListeners(ComRingBufferUpdateEventListener.class) )
			l.dataReceived(e);
	}
	
    /**
     * Syntax of transmission:
     *	< [ch#] | [hibyte] [lowbyte] < [ch#] | [hibyte] [lowbyte] ...
     */
    public class ComListener implements SerialPortEventListener 
    {
        public void serialEvent (SerialPortEvent event)
        {
            if (event.getEventType()==SerialPortEvent.DATA_AVAILABLE)
            {
                try
                {
                    int readyBytes = input.available();
                    byte [] buffer = new byte[readyBytes];
                    readyBytes = input.read(buffer);
                    if(readyBytes>0)
                    {		
                        //append new data to buffer
                        for (int i = 0; i<readyBytes; i++)
                        {
                            byteList.add(buffer[i]);
                            if (i!=0)
                            {
                                if ((buffer[i] == 10) && (buffer[i-1] == 13)) //CRLF received
                                {
                                    Byte[] dataBuf = new Byte[byteList.size()];
                                    dataBuf = byteList.toArray(dataBuf); 
                                   
                                    //remnove CRLF
                                    /*
                                    byte[] exportBytes = new byte[dataBuf.length-2]; //remove CRLF
                                    */
                                    byte[] exportBytes = new byte[dataBuf.length]; //convert to byte
                                    for ( int k=0; k<exportBytes.length; k++)
                                        exportBytes[k] = dataBuf[k];
                                    
                                    //System.out.println("read length: " + exportBytes.length);
                                    notifyComReceiveListeners(new ComRingBufferUpdateEvent(this, "RingUpdate", exportBytes, ringReadStart, ringWriteStop));                                    

                                    byteList = new ArrayList<Byte>(RINGBUFLEN);
                                }
                            }
                        }
                        
/*                        
                        ringWriteStop = (ringWriteStop+readyBytes)&(RINGBUFLEN-1);
                        //append new data to old buffer
                        for (int i=0; i)
                        notifyComReceiveListeners(new ComRingBufferUpdateEvent(this, "RingUpdate", buffer, ringReadStart, ringWriteStop));
*/
                    }                    
                    
                } 
                
                catch (Exception e) 
                {
//                    logArea.append("\n" + e.getMessage());
                    e.printStackTrace();
//                    System.out.println("\n" + e.getMessage());
                }
                
            }
        }
    }    
/*    
	class BufferParseListener implements ComParser.ComParserDoneEventListener
	{
		public void dataParsed (ComParser.ComParserDoneEvent e)
		{
//			System.out.println("com->parsed: " );
//			System.out.println(e.inputBuf.toString());
			inputStringBuf = e.inputBuf;
			ringReadStart = e.readStart;
		}
	}
*/	
	public class ComRingBufferUpdateEvent extends EventObject
	{
		String eventName;
		//StringBuffer inputBuf;
                byte[] arrayBuf;
		int readStart,writeStop;
		ComRingBufferUpdateEvent (Object source, String evtName, byte[] data, int readStart, int writeStop)
		{
			super(source);
			eventName = evtName;
			arrayBuf = data;
			this.readStart = readStart;
			this.writeStop = writeStop;
		}

        }
	
	
	public interface ComRingBufferUpdateEventListener extends EventListener
	{
		void dataReceived (ComRingBufferUpdateEvent e);
	}
	
}

