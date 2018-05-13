"""
start service.py in common

use postman to send the belowing to localhost:4040

{
 "jsonrpc": "2.0",
 "id": 123,
 "method": "logNewsClickForUser",
 "params": ["user", "nmuYSK3LFDb7SY727Ibonw==\n"]
}

python click_log_processor.py

then open mongo

use tap-news
db.user_preference_model.findOne() should return preference dict of user

"""