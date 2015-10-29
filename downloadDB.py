import os
os.system('heroku pg:backups capture')
os.system('curl -o latest.dump `heroku pg:backups public-url`')
os.system('pg_restore --verbose --clean --no-acl --no-owner -h localhost -U adam -d southernweb latest.dump')

