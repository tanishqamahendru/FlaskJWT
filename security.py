from werkzeug.security import safe_str_cmp
from user import User
#users is the in-memory table of our registered users
users = [
    User(1, 'bob', 'asdf'),
    User(2, 'user2', 'abcxyz'),
]

#username_table would give the id, username, password from the userid_mapping, so we do not have to iterate over the users again and again
username_table = {u.username: u for u in users}
#userid_table is the userid mapping
userid_table = {u.id: u for u in users}

def authenticate(username, password):
	#None is the default value i.e if there is no username like the given.
	user = username_table.get(username, None)
	if user and safe_str_cmp(user.password, password):
		return user 

#Identity function takes in the payload (payload is the contents of the jwt token)
def identity(payload):
	#extract the user id from that payload
	userid = payload['identity']
	#retrieve the user which matches this userid
	return userid_table.get(userid, None)