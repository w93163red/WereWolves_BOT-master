import win32com.client
import os

qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
q1info = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
computer_name = os.getenv('COMPUTERNAME')
q1info.FormatName="direct=os:"+computer_name+"\\PRIVATE$\\321"
qinfo.FormatName="direct=os:"+computer_name+"\\PRIVATE$\\123"
queue=qinfo.Open(1,0)   # Open a ref to queue to read(1)
q = q1info.Open(2,0)
msg=queue.Receive()
print ("Label:",msg.Label)
print ("Body :",msg.Body)

# msg=win32com.client.Dispatch("MSMQ.MSMQMessage")
# msg.Label="TestMsg"
# msg.Body = "The quick brown fox jumps over the lazy dog"

msg.send(q)
queue.Close()
q.Close()