import win32com.client
import os

qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
q1info = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
computer_name = os.getenv('COMPUTERNAME')
qinfo.FormatName="direct=os:"+computer_name+"\\PRIVATE$\\123"
q1info.FormatName="direct=os:"+computer_name+"\\PRIVATE$\\321"
queue = qinfo.Open(2,0)   # Open a ref to queue
q1 = q1info.Open(1,0)
msg=win32com.client.Dispatch("MSMQ.MSMQMessage")
msg.Label="TestMsg"
msg.Body = "The quick brown fox jumps over the lazy dog"
msg.Send(queue)
msg=q1.Receive()
print(msg)
queue.Close()
q1.Close()