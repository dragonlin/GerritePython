import json
from pygerrit2.rest import GerritRestAPI
from requests.auth import HTTPBasicAuth
import datetime

TIME_FORMATTER = "%Y-%m-%d %H:%M:%S"
MAX_ALERT_PERIOD_SECONDS = 3600 * 24

Status_list = ['open','closed','merged','pending','reviewed','abandoned','draft']


GERRITE_USER = ""
GERRITE_PWD = ""
PROJECT_NAME = "openstack/horizon"

GERRITE_URL_AUTH = "https://review.openstack.org"
GERRITE_URL_CHANGE = "/changes/?q=status:%s+project:%s"%(Status_list[2],PROJECT_NAME)
GERRITE_URL_DETAILS = "/changes/%s/detail"
GERRITE_URL_DETAILS = "/changes/%s/?o=CURRENT_REVISION&o=CURRENT_FILES"
GERRITE_URL_Files = "/changes/%s/revisions/{revision-id}/files/"

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
        self.title = title
        self.author = author
        self.comment_author = comment_author
        self.message = message
        self.start_date = start_date
        self.end_date = end_date
    
    def __repr__(self):
        return TABLE_ROW_ELEMENT % (self.title,self.comment_author,\
               self.start_date.year,self.start_date.month,self.start_date.day,\
               self.start_date.hour,self.start_date.minute,self.start_date.second,\
               self.end_date.year,self.end_date.month,self.end_date.day,\
               self.end_date.hour,self.end_date.minute,self.end_date.second)

    def __str__(self):
        return self.__repr__()

def save_html(content):
    f1 = open('./report.html','w')
    f1.write(content)
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
    print len(changes)
    files_dict = {}
    if len(changes) > 0:
        change_id = ""
        url = ""
        created_date = None
        comment_date = None
        elapsed_second = 0
        index = 0
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
            change_id = change['change_id']
            index+=1
            if index == 100:
                break 
            print str(index) + " - " + change_id
            url = GERRITE_URL_DETAILS % change_id    
            detail=Gerrite_Get_Data_From_URL(rest,url)
            #print "detail",json.dumps(detail,indent=4)
            
            title = detail['subject']
            # ---- get all commit files in changes ----
            current_revisionId = detail['current_revision']
            revisions = detail['revisions']
            files_json_string  = revisions[current_revisionId]['files']
            #print type(files_json_string) 
            #print "files",json.dumps(revisions[current_revisionId]['files'],indent=4)
            #files_dict = json.loads(str(files_json_string))
            for (fileName,codeInfo) in files_json_string.items():
                #print fileName
                files_dict[fileName] = files_dict.get(fileName,0) + 1
                #print type(codeInfo)
            #print files_dict
            
        
    print files_dict
        #save_html(HTML_TEMPLATE % html_datatable)

if __name__=="__main__":
    main()

