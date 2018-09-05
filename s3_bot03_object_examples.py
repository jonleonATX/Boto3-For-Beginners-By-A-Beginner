# coding: utf-8
# assumes your PC is configured, or you've loaded everything for AWS, Python, boto3
# and that you've created a user in AWS console and have access and secret access keys

### NOTE: there are two variables that are hardcoded - myProfile and bucket
### change them before running the script

# mimetypes guesses at content-type of file
# boto3 is AWS Python SDK
# pprint formats the json output for easier reading
# json parser - very helpful
# path helps translate windows \ to unix /
# requests used for api calls
import mimetypes
import boto3
from pprint import pprint
import json
from pathlib import Path
import requests

# create the session and get s3 resource as well as s3 client
# this assumes you have configured aws for a user (aws configure --profile ImAUser)

# myProfile = 'ImAUser'
# bucket = 'my-bucket'
myProfile = 'ImAUser'
bucket = 'my-bucket'

# when creating resources and clients, know when you are using session vs boto3
session = boto3.Session(profile_name=myProfile)
s3sr = session.resource('s3')
s3sc = session.client('s3')

s3br = boto3.resource('s3')
s3bc = boto3.client('s3')

# see stored value in each variable above; verify no errors on start
print(session)
print(s3sr)
print(s3sc)
print(s3br)
print(s3bc)
print('\n' * 2)

# bucket identifier and attribute
# needs to be an existing bucket for user profile used
bucket_name = s3sr.Bucket(bucket)
print(bucket_name.name)
print(bucket_name.creation_date)
print('\n' * 2)

# get all object keys for the given buckets
# in some cases this can be 1000s or more objects: see paginator samples below

# this gets the collection
bucket_objs = bucket_name.objects.all()
print(bucket_objs)
print('\n' * 2)

# this prints info on each object (bucket name and object key)
for obj in bucket_objs:
    print(obj)
print('\n' * 2)

# differnt layout of the same information above
for obj in bucket_objs:
    print("Bucket = {} ; key = {}".format(obj.bucket_name, obj.key))
print('\n' * 2)

# for buckets that may have many objects a paginator will return a dictionary
# one page at a time. dictionary changes the way the data is retrieved.
# instead of obj.key it is obj['Key']
paginator = s3sr.meta.client.get_paginator('list_objects_v2')

# print the page object
for page in paginator.paginate(Bucket=bucket_name.name):
    pprint(page)
print('\n' * 2)

# get the object information
for page in paginator.paginate(Bucket=bucket_name.name):
    for obj in page.get('Contents'):
        print("Key = {} ; Etag = {}".format(obj['Key'], obj['ETag']))
        # print(obj['Key'], obj['ETag'], obj['LastModified'], obj['Size'], obj['StorageClass'])
print('\n' * 2)

# get information about this page - long way and easy way
for page in paginator.paginate(Bucket=bucket_name.name):
    print("Number of keys on this page: {}".format(page.get('KeyCount')))
    print("Max number of keys possible: {}".format(page.get('MaxKeys')))
print('\n' * 2)

# get info by index number (specific file position)
for page in paginator.paginate(Bucket=bucket_name.name):
    pprint(page.get('Contents')[0])
print('\n' * 2)

# nested get command
for page in paginator.paginate(Bucket=bucket_name.name):
    pprint(page.get('ResponseMetadata').get('HTTPHeaders').get('content-type'))
print('\n' * 2)

# this returns a dictionary, not a string of key:value pairs in HTTPHeaders
for page in paginator.paginate(Bucket=bucket_name.name):
    for k, v in page.get('ResponseMetadata').get('HTTPHeaders').items():
        print(k,v)
print('\n' * 2)

# get values in HTTPHeaders Key directly
for page in paginator.paginate(Bucket=bucket_name.name):
    pprint(page.get('ResponseMetadata').get('HTTPHeaders').get('content-type'))
    pprint(page.get('ResponseMetadata').get('HTTPHeaders').get('date'))
    pprint(page.get('ResponseMetadata').get('HTTPHeaders').get('x-amz-bucket-region'))
print('\n' * 2)

#hardcode the full path name
pathname = 'C:/your/path/here/code/'
fn = 'sample.txt'
fullpath = Path(pathname + fn)
print(fullpath)
print('\n' * 2)

# upload a file with minimal logic using resource not client
# upload with same filename
resp = bucket_name.upload_file(str(fullpath),
    str(fn), ExtraArgs={'ContentType': 'text/plain'})
print(resp)
print('\n' * 2)

#same as above but using mimetypes
content_type = mimetypes.guess_type(fn)[0] or 'text/plain'
print(content_type)
print('\n' * 2)
bucket_name.upload_file(str(fullpath),
    str(fn), ExtraArgs={'ContentType': content_type})

# download a file with minimal logic using resource not client
# download with same filename
bucket_name.download_file(fn, pathname + 'hello.txt')

# get object's ACL
object_acl = s3sr.ObjectAcl(bucket, fn)
print(object_acl.bucket_name)
print(object_acl.object_key)
print(object_acl.grants)
print(object_acl.owner)
print(object_acl.request_charged)
print(object_acl.get_available_subresources())
print(object_acl.Object())
print('\n' * 2)



# get object's summary
object_summary = s3sr.ObjectSummary(bucket, fn)
print(object_summary.bucket_name)
print(object_summary.key)
print(object_summary.e_tag)
print(object_summary.owner)
print(object_summary.get_available_subresources())
print(object_summary.Acl())
print(object_summary.Object())
#print(object_summary.Version())  ## ValueError: Required parameter id not set
print(object_summary.last_modified)
timeFormat=object_summary.last_modified
formatedTime=timeFormat.strftime("%Y-%m-%d %H:%M:%S")
pprint( 'Bucket name is '+ bucket + ' and key name is ' + object_summary.key + ' \
and last modified at time '+ formatedTime)
print('\n' * 2)

# get object
object = s3sr.Object(bucket, fn)
print(object.bucket_name)
print(object.key)
print(object.e_tag)
print(object.delete_marker)
print(object.website_redirect_location)
print(object.version_id)
ver_id = object.version_id
print(object.Version(ver_id))
print('\n' * 2)

# get object's versions
version_all_data = s3bc.list_object_versions (Bucket = bucket, Prefix = fn)
pprint(version_all_data)
print('\n' * 2)

# just the version portion of the response
version_list = version_all_data.get('Versions')
pprint(version_list)
print('\n' * 2)

# list only the version IDs
for version in version_list:
    versionId = version.get('VersionId')
    print(versionId)
print('\n' * 2)

# this works without the version id
object_acl = s3sc.get_object_acl(
    Bucket=bucket,
    Key=fn)
pprint(object_acl)
print('\n' * 2)

# to get this to work, bucket and object policies must be in replace
# specifically look for s3:GetObjectVersionAcl
object_acl_byVersion = s3sc.get_object_acl(
    Bucket=bucket,
    Key=fn,
    VersionId=ver_id)
pprint(object_acl_byVersion)
print('\n' * 2)

# generating pre-signed URLs and getting the file
presigned_url = s3sc.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': bucket,
        'Key': fn  })
pprint(presigned_url)
print('\n' * 2)

# doesn't save the file; need to add that functionality
get_presigned_file = requests.get(presigned_url)
pprint(get_presigned_file)
# print(get_presigned_file.text) ## works - prints contents of file
print('\n' * 2)


# create a paginator with a max numbe of items returned
paginator = s3sr.meta.client.get_paginator('list_objects_v2')

# print the page object
page_iterator = paginator.paginate(Bucket=bucket_name.name ,
                                   PaginationConfig={'MaxItems': 50})
for page in page_iterator:
    pprint(page)
print('\n' * 2)

# get the object information
for page in page_iterator:
    for obj in page.get('Contents'):
        print("Key = {} ; Etag = {}".format(obj['Key'], obj['ETag']))
        # print(obj['Key'], obj['ETag'], obj['LastModified'], obj['Size'], obj['StorageClass'])
print('\n' * 2)

for page in page_iterator:
    print("Number of keys on this page: {}".format(page.get('KeyCount')))
    print("Max number of keys possible: {}".format(page.get('MaxKeys')))

# find total number of objects in bucket
# this will say 1000/1000 if more than 1000 objects, then IsTruncated is True
resp = s3sc.list_objects_v2(Bucket=bucket)
print('list_objects_v2 returned {}/{} files.'.format(resp['KeyCount'], resp['MaxKeys']))
print(resp['IsTruncated'])

# this will give the number of objects total
size = sum(1 for _ in bucket_name.objects.all())
print(size)
