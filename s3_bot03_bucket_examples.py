# coding: utf-8
# assumes your PC is configured, or you've loaded everything for AWS, Python, boto3
# and that you've created a user in AWS console and have access and secret access keys

# NOTE: there are two variables that are hardcoded - myProfile and bucket
# change them before running the script

# boto3 is AWS Python SDK
# pprint formats the json output for easier reading
# json parser - very helpful
import boto3
from pprint import pprint
import json

# create the session and get s3 resource as well as s3 client
# this assumes you have configured aws for a user (aws configure --profile ImAUser)

myProfile = 'ImAUser'
bucket = 'my-bucket'

session = boto3.Session(profile_name=myProfile)
s3 = session.resource('s3')
s3c = boto3.client('s3')

# see stored value in each variable above; verify no errors on start
print(session)
print(s3)
print(s3c)
print()
print()

# bucket identifier and attribute
# needs to be an existing bucket for user profile used
bucket_name = s3.Bucket(bucket)
print(bucket_name.name)
print(bucket_name.creation_date)

# get list of s3 buckets for this user
response = s3c.list_buckets()
print(response)
print()
print()
pprint(response)

# loop through bucket names
for b in response['Buckets']:
    print(b['Name'])

# get a list of all bucket names from the response
# outer [] denote list
buckets = [b['Name'] for b in response['Buckets']]
print(buckets)
print("Bucket List: %s" % buckets)
print("Bucket List:", buckets)

# another loop through bucket names from buckets list
for b in buckets:
    print(b)

# use indices to get individual values of list; index starts with 0!
print(buckets[0])
print(buckets[1])

# find number of elements in the list
len(buckets)
print(len(buckets))

# set a bucket's policy to public; all documents become visible
# policy statement from boto3 documentation
# %s in Resource looking for previously defined bucket_name
# the '% bucket_name' will fill in %s withe bucket name
# to change bucket to private replace "Allow" with "Deny"
policy = """
    {
      "Version":"2012-10-17",
      "Statement":[{
      "Sid":"PublicReadGetObject",
      "Effect":"Allow",
      "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
          ]
        }
      ]
    }
    """ % bucket

# AWS only wants what is between the {}, so we need to strip the extra characters
print(policy)
policy = policy.strip()
print(policy)

# setup the policy to be uploaded
pol = bucket_name.Policy()
print(pol)
pol.put(Policy=policy)

# get current bucket Policy; requires client, not resource: s3c = boto3.client('s3')
current_policy = s3c.get_bucket_policy(Bucket=bucket)
print(current_policy)

# make s3 a static website
# Website configuration from boto3 documentation
ws = bucket_name.Website()

ws.put(WebsiteConfiguration={
    'ErrorDocument': {
        'Key': 'error.html'
    },
    'IndexDocument': {
        'Suffix': 'index.html'
       }
  })

#############################################################################
# a bit on parsing response strings - use policy response as s3_bot03_examples
# get the policy same as above
current_policy = s3c.get_bucket_policy(Bucket=bucket)
print(current_policy)

# print the ResponseMetadata value
# Note: works for metadata that has json single quote format
# You will notice some values contain double quotes and will be handled differently
print(current_policy['ResponseMetadata'])
print()

# print the RequestId value in the ResponseMetadata Key
print(current_policy['ResponseMetadata']['RequestId'])

# notice the policy statement contains values with double quotes
print(current_policy['Policy'])

#to get values from policy string, load into json

pol_json = json.loads(current_policy['Policy'])
# note this causes an error, need to get rid of []
# there may be an 'is_public' type function, but I wasn't sure, so I find directly
# print(pol_json['Statement']['Effect'])
# now it works - the [0] gets rid of the []
print(pol_json['Statement'][0]['Effect'])
print()


# iterate through the keys and values of the entire polcy key
for key in pol_json:
    value = pol_json[key]
    print("The key = {} ; value = {}".format(key, value))
print()
print()

# print the keys and values of the policy statement
# need the [0] to move past the [] and get the format we need
for key in pol_json['Statement'][0]:
    value = pol_json['Statement'][0][key]
    print("The key = {} ; value = {}".format(key, value))
