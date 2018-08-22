# coding: utf-8
# run command inside directory: pipenv run ipython -i ipythonsession.py
"""Use this file in ipython for an easy start to AWS scripting"""

import boto3

# create the session and get s3 resource as well as s3 client
#session = boto3.Session(profile_name='jleontrader')
session = boto3.Session(profile_name='Trainer1')
s3 = session.resource('s3')
s3_client = boto3.client('s3')
