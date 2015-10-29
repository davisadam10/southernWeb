import boto
import os
import sys
from boto.s3.key import Key

testfile = "/Users/adam/dev/workspace/git/southernWeb/mydb.dump"
os.system('pg_dump -Fc --no-acl --no-owner -h localhost -U adam southernweb > %s' % testfile)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

bucket_name = 'southernwebdelayrepay'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


import boto.s3
bucket = conn.get_bucket(bucket_name)


print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


k = Key(bucket)
k.key = 'latest.dump'
k.set_contents_from_filename(testfile,
    cb=percent_cb, num_cb=10)
k.set_acl('public-read-write')
print 'Finished Upload To Amazon'

os.system("heroku pg:backups restore 'https://s3-eu-west-1.amazonaws.com/southernwebdelayrepay/latest.dump' HEROKU_POSTGRESQL_TEAL_URL --confirm southernweb")

print 'Database Update Is Complete'