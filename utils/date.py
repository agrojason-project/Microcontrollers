from datetime import datetime
import http.client

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

class DateTime:
    def __init__(self):
        self.date = datetime.min 

    
    def get_utc_now(self):
        try:
            conn = http.client.HTTPConnection('google.com') 
            conn.request("GET", "/")
            r = conn.getresponse()
            r.getheaders() #Get all http headers
            ts = r.getheader('date') # Get the date part of the http header
            self.date = datetime.strptime(ts[5:25], "%d %b %Y %H:%M:%S") 
        except:
            self.date = datetime.utcnow()
        return self.date.strftime(DATETIME_FORMAT)
