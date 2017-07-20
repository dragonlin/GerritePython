import json
from pygerrit2.rest import GerritRestAPI
from requests.auth import HTTPBasicAuth
import datetime
import traceback

TIME_FORMATTER = "%Y-%m-%d %H:%M:%S"
MAX_ALERT_PERIOD_SECONDS = 3600 * 24

GERRITE_USER = ""
GERRITE_PWD = ""
GERRITE_URL_AUTH = "http://gerrite1.ext.net.nokia.com"
GERRITE_URL_CHANGE = "/changes/?q=status:open+project:NOKIAWULF/WULF"
GERRITE_URL_DETAILS = "/changes/%s/detail"

CHARACTER_SET = "utf8"

HTML_TEMPLATE = '''
<html>
<head>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
   %s
</head>
<body>
</body>
</html>
'''

HTML_INNER_GANTT_TEMPLATE = '''
<script type="text/javascript">
  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {
    var container = document.getElementById('%s');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Position' });
    dataTable.addColumn({ type: 'string', id: 'Name' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([%s]);
    chart.draw(dataTable);
  }
</script>
<div id="%s" style="height: 200px;"></div>
'''

TABLE_ROW_ELEMENT = '''
                        [ '%s', '%s', new Date(%d,%d,%d,%d,%d,%d),new Date(%d,%d,%d,%d,%d,%d)],
                    '''

class CommentObject:

    def __init__(self,title,author,comment_author,message,start_date,end_date):
        self.title = title.encode(CHARACTER_SET)
        self.author = author.encode(CHARACTER_SET)
        self.comment_author = comment_author.encode(CHARACTER_SET)
        self.message = message.encode(CHARACTER_SET)
        self.start_date = start_date
        self.end_date = end_date
    
    def __repr__(self):
        res = TABLE_ROW_ELEMENT % (self.title,self.comment_author,\
               self.start_date.year,self.start_date.month,self.start_date.day,\
               self.start_date.hour,self.start_date.minute,self.start_date.second,\
               self.end_date.year,self.end_date.month,self.end_date.day,\
               self.end_date.hour,self.end_date.minute,self.end_date.second)
        return res.decode(CHARACTER_SET)

    def __str__(self):
        return self.__repr__()

def save_html(content):
    f1 = open('./report.html','w')
    f1.write(content.encode(CHARACTER_SET))
    f1.close()

def Gerrite_Auth():
    auth = HTTPBasicAuth(GERRITE_USER,GERRITE_PWD)
    rest = GerritRestAPI(url=GERRITE_URL_AUTH,auth=auth)
    return rest

def Gerrite_Get_Data_From_URL(rest,URL):
    res = rest.get(URL)
    return res

def main():
    rest = Gerrite_Auth()
    changes = Gerrite_Get_Data_From_URL(rest,GERRITE_URL_CHANGE)
    #print len(changes)
    #print changes
    if len(changes) > 0:
        change_id = ""
        url = ""
        created_date = None
        comment_date = None
        elapsed_second = 0
        index = 1
        title = ""
        author = ""
        comment_author = ""
        message = ""
        start_date = ""
        end_date = ""
        size = 0
        commentObjects = []
        html_row_element = ""
        html_datatable = ""
        for change in changes:
            try:
                change_id = change['change_id']
                url = GERRITE_URL_DETAILS % change_id    
                detail=Gerrite_Get_Data_From_URL(rest,url)
                #print json.dumps(detail,indent=4) 
                title = detail['subject']
                created_date = datetime.datetime.strptime(detail['created'][:19],TIME_FORMATTER)
                author = detail['messages'][0]['author']['username']
                size = len(detail['messages'])
                for i in range(1,size):
                    comment_author = detail['messages'][i]['author']['username']
                    message = detail['messages'][i]['message']  
                    start_date = datetime.datetime.strptime(detail['messages'][i-1]['date'][:19],TIME_FORMATTER)  
                    end_date = datetime.datetime.strptime(detail['messages'][i]['date'][:19],TIME_FORMATTER)  
                    commentObjects.append(CommentObject(author+":"+title,author,comment_author,message,start_date,end_date))
                for commentObject in commentObjects:
                    #print commentObject
                    html_row_element = html_row_element + commentObject.__str__()

                html_datatable = html_datatable + HTML_INNER_GANTT_TEMPLATE % (author+"_"+str(index),html_row_element,author+"_"+str(index))
                commentObjects = []
                html_row_element = ""
                print index
                index = index + 1
                created_date = None
                comment_date = None
                elapsed_second = 0
            except Exception,e:
                traceback.print_exc()
        save_html(HTML_TEMPLATE % html_datatable)

if __name__=="__main__":
    main()

