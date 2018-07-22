from __future__ import with_statement
from __future__ import print_function
import sys
import urllib2
import csv
import settings
import requests
import pprint


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, unicode(value, 'utf-8')) for key, value
                    in row.iteritems()])

def post_record(r):

    form = dict(r)

    if form.get("type", "") == "webservice":
        return post_webservice(r)

    form['auth_key'] = settings.auth_key
    file_name = form.pop("file_data", None)
    title = r.get('title').encode('utf-8')
    pp = pprint.PrettyPrinter(indent=4)


    if file_name is not None:
        try:
            if settings.DEBUG:
                print("SENDING ... %s" % file_name)
                pp.pprint(form)

            print("Uploading '%s' (%s) .... " % (title, file_name), end='')
            sys.stdout.flush()   
            with open(file_name, 'rb') as f:
                r = requests.post(settings.url, files={'file': f}, data=form)
                print('OK' if r.status_code == 201 else 'ERROR ' + str(r.status_code))
                if settings.DEBUG or r.status_code != 201:
                    print("Detalle")
                    print(pp.pprint(r.json()))
        except Exception, e:
            print("Error %s " % str(e))
    else:

        try:
            print("Uploading %s" % title   )
            pp = pprint.PrettyPrinter(indent=4)
            print("SENDING WEB SOURCE TO... %s" % settings.url)
            pp.pprint(form)
            response = requests.post(settings.url, data=form)
    		
            print("Respuesta:")
            print(response.text)
        except Exception, e:
            print("Error Web Source %s " % str(e))


def post_webservice(r):
    print("uploading %s" % r.get('title').encode('utf-8'))

    form = dict(r)
    form['auth_key'] = settings.auth_key

    try:
        pp = pprint.PrettyPrinter(indent=4)
        print("SENDING WEBSERVICE TO %s ..." % settings.url)
        pp.pprint(form)
        response = requests.post(settings.url, data=form)
		
        print("Respuesta:")
        print(response.text)
    except Exception, e:
        print("Error %s " % str(e))
        
if __name__=="__main__":
    csv_name=sys.argv[1]

    csv_data = open(csv_name,"rb")
    try:
        for r in UnicodeDictReader(csv_data):
            post_record(r)
    finally:
        csv_data.close()
