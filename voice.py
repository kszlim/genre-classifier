import wit
while(True):
    access_token = 'IDWUGDNBHGWFLUYQJVWXAZ33YD73CTIJ'
    wit.init()
    response = wit.voice_query_auto(access_token)
    print('Response: {}'.format(response))
    wit.close()
