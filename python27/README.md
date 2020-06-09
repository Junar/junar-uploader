Junar API Publish Module 
========================

The publish method allows to create and update datasets that are on the cloud or on local machines. It allows the use of a GUID to identify pre-existing resources to be updated or to create brand new resources. The file formats currently supported are CSV, XLS, XLSX, KML and KMZ. XML is also supported, but depending on the inner structure of the dataset it could return and error so it’s not recommended to publish through the API.  
  
This document briefly describes the use of the API Publish module through a curl request or [**using our junar uploader tool (recommended)**](#ourtool), the parameters needed and its syntax, error handling as well as providing a sample operation of publishing and updating a resource. For more specific questions or support, please send an email to support@junar.com.  
  
  
**URL**  
The API domain is the same as it is defined on the Junar Workspace. In this document we’ll use the following 
http://api.myopendata.com/datastreams/publish/{guid}  
  
**Supported Request Method**  
  `POST`
  
**Parameters**  
  * guid: An alphanumeric string that's unique to each data view. Optional. Only to use when updating a resource with a new file_data, source or titles, description, etc. If this parameter is not present, a new resource with a new guid will be created.  
  * title: Up to 100 characters. Mandatory.  
  * description: Up to 140 characters. Optional.  
  * category : Name of the category to use. It must be a pre-existing category for the account.  
Mandatory. Categories are created from the Admin section of the account Workspace.  
  * tags: Tags for the data view. Multiple tags can be added separating them by commas. Optional.  
  * notes: Additional notes to provide context to the data view. This field supports basic HTML text format and up to 1000 characters. Optional.  
  * table_id: The location of the table on the document, starting from zero. If the document is an XLS or any other multi sheet document, the id will increase by one for each sheet on the document (i.e. the first sheet will be table0, the second sheet will be table1, and so on). Mandatory.  
  * auth_key : Your private API auth key, provided by Junar. Mandatory. 
  * meta_data: If the resource has an additional metadata field it should be entered here as an encoded json element. Optional.  
  * file_data: The name of the file to be used as dataset. The file should be on the same directory as the curl executable in order to collect it, and cointain a @ before the file name with its extension type (i.e. @sample-dataset.csv). Mandatory if no source is provided.  
  * source: The URL to the file to be used as dataset. Mandatory if no file_data is provided. 
  * clone: If set to True, it allows to inherit customizations of a data view (headers, filters, parameters, column formatting) to the new revision. Must go accompanied by the guid parameter to indicate the data view that is being cloned. Optional.  
  * header_row: Defines which row to be selected as the header row of the data view. Rows must be entered as row0 (for the first row), row1 (for the second row) and so on. Only one header row accepted per data view.  
   
**Example**  
I want to create a data view using a file from my computer called mydataset.csv. Since it's a csv file it only contains one sheet, so table0 is the value to input on the table_id parameter. The title, description, tags and notes are defined and no additional meta_data field is used. The publishing API key has been requested and delivered, and added to the corresponding field and the category to be used is already defined in the account. The curl request should look like this:  
  
  `curl -v -F "title=Open Data" -F "description=Some description" -F "category=Open Data" -F "tags=hello,world" -F "notes=some notes" -F "table_id=table0" -F "auth_key=YOUR_AUTH_KEY" -F "meta_data=" -F "file_data=@mydataset.csv" http://api.myopendata.com/datastreams/publish`  
  
I should receive confirmation of success as a json similar to this: 

  `{'description': 'Some description', 'title': 'Open Data', 'created_at': '2014-03-04 22:55:40', 'tags': ['hello', 'world'], 'source': 'mydataset.csv', 'link': 'http://myopendata.com/datastreams/75239/open-data/', 'user': 'myuser', 'id': 'OPEN-DATA-48953'}`  
  
This creates a new data view with "Pending Review" status on the Junar workspace, and still needs to be “Published” in order to be displayed in the open data site.  
The resulting resource will take the entire table of the source document and create a data view containing all the information in it. In the current version of the Publish module, selecting specific columns or rows of the table is not available. It is important to save the return id1 since it'll be necessary to update the resource. If I wanted, for instance, to replace the uploaded csv file for an xls hosted under a known URL, select a new table to use and change the data view title and description while keeping the headers modifications made to the data view, the curl request should look like this 
  `curl -v -F "guid=OPEN-DATA-48953" -F "title=Open Data Resource" -F "description=This is a more adequate description to the data view" -F "category=Open Data" -F "tags=hello,world" -F "notes=some notes" -F "table_id=table2" –F “clone=True” -F "auth_key=YOUR_AUTH_KEY" -F "source=http://www.mysite.com/folder/open_data.xls" http://api.myopendata.com/datastreams/publish`  
  
**And the response will look like this:**  
  
  `{'description': 'This is a more adequate description to the data view', 'title': 'Open Data Resource', 'created_at': '2014-03-04 23:15:40', 'tags': ['hello', 'world'], 'source': 'http://www.mysite.com/folder/open_data.xls', 'link': 
'http://myopendata.com/datastreams/75239/open-data/', 'user': 'myuser', 'id': 'OPEN-DATA-48953'}`  
   
Notice how all fields not modified contain the same information has they had before since the API will create a new revision of the resource. This new revision will have the same status as the latest revision. Revisions can be handled on the Junar Workspace as any other resource.  
  
**Error Handling - HTTP 400**  
When an error is found, it returns a HTTP 400 with the following syntax:  
  
  `{"error": 400, "message": "Bad Request", "description": error_description} 
Here are the possible values for error_description explained: The auth_key does not exist. ==> The auth_key is not a valid private key The GUID does not exist. ==> A dataview with such guid could not be found tableN does not exist. ==> The table_id could not be found in the data source. title: This field is required. ==> The title is mandatory [title | description]: Ensure this value has at most XX characters (it has YY). ==> The title is limited to 100 characters. The description is limited to 140.` 
  
  
Our tool. The Junar Uploader
==============

Uploads data to a Junar Site using the Junar API.

Usage:

Copy *settings.py.tpl* to *settings.py* and edit according parameters to your site. Put your auth_key and url.
The **url** parameter like:  

  `http://you_api_url/datastreams/publish`  

Create a csv file with the information for the files to upload.
You can upload a simple spreadsheet with data or define the information for a web service connection.

### <a name="ourtool"></a>
Upload spreadsheet data
-----------------------

You'll need a index csv file with a spreadsheet list.  

Sample for [a spreadsheet with data here](https://docs.google.com/a/okfn.org/spreadsheet/ccc?key=0Aq9agjil66PydGFaRERZOVBEam5KMUFIM1dKVklrRlE#gid=0)  

**Fields**  

 * title: Mandatory. Name for you data. Up to 100 characters
 * description: Optional. Information about this file. Up to 140 characters
 * category: A valid category name. Mandatory
 * tags: A **quoted** comma separated values like: "tag1, tag2, tag3"
 * meta_data: Do not use if you don't need it
 * file_data: Path to readable spreadsheet file
 * table_id: Use *table0* for the first sheet (or single *csv* file)
 * guid: Optional. use it with *clone* for update existing data.
 * clone: Optional. *True* for edit a pre-existing data. If you don't provide the guid we detect it by dataset filename.  

Call jupload.py with the csv file as parameter. Make sure all the files are readable on their relative locations to the script.

**Sample call:**  
  `python jupload.py info.csv`  

**Consider the following:**  
  * Csv columns must be separated by commas.  
  * Csv file must be saved in utf-8 encoding.  
  * juploader prints the title of the dataset being uploaded and then the response obtained from Junar's API  


juploader for web services
--------------------------------

You can add web services too using the same tool **jupload.py**  
Works like juploader but **uses different parameters**. You can see them in [this CSV file] (https://docs.google.com/spreadsheets/d/1uwSctyt5JMWibZUSChsUrI-hvFh_0oNPNfgkADuhhZM/edit?usp=sharing)  
  
The first column on the csv specify the *type* is a **webservice**, **if you forget this field the process will fail.**  
  
So, defining the fields in the csv file you can add a webservice to your junar account like this:  
  `python jupload.py info-webservices.csv`

You can define more than one web service in the same csv file. You must use **one line** for each web service definition.

**Fields:**  
  * type:  Always *webservice*  
  * title:  The title of the data  
  * description:  Information about this data (140 max length)  
  * category: A valid category name  
  * tags: A **quoted** comma separated values like: "tag1, tag2, tag3"
  * endpoint: The url of the web service  
  * impl_type: Use **14** for *REST/JSON* and **1** for *SOAP/XML*. Others values are not allowed  
  * path_to_data:  Field name for the data with a *$.* prefix. Sample *$.data*  
  * path_to_headers: Field name for the headers data (field names) with a *$.* prefix. Sample *$.headers*  
  * token: just if webservice need it  
  * algorithm: just if webservice need it  
  * signature: just if webservice need it  
  * username: just if webservice need it  
  * password: just if webservice need it  
  * create_datastream: Optional. If you want to create a view use = 1  
  * status: Optional. For publish dataset and view (if *create_datastream*) use 3. Default is 1 (pending revision).  
  * data_source and select_statement: Optionals. If you want to define more about fields you can use this field.  
  * You can't use *clone* on web services.  
  
  


