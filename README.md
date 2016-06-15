# title_generation
generate title for Chinese text
it is a running server, you can run server using the following command:
python server.py

The address of the server would be http://your server address: 8060
You can change port number 8060 to any number

You can post your data like this:
{"title":"","first":"","content":""}

title is the original title in the content you sent, can be empty.
first is the first paragraph in the content (good for news), the new title will be extracted from this paragraph, content is the full text you sent.

This method using Chinese Dependency Tree is a rule-based title extraction method.
