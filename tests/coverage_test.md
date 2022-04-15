- this file describes which tests we need to create to ensure all our implementation code is actually being run
- for example if we have an auth function such as:
	```python
	def auth(arg1):
		if arg1 == 'apple':
			return true
		elif arg1 == 'fox':
			return true
		elif arg1 == 'bread':
			return true
		else:
			return false
	```
	- we need to make sure we test every elif statement here with a distinct test
- the coverage report shows us that we have not written tests for our helper functions, and since I do not think we need to, I have added these files as exclusions to the coveragerc file.
		- I have also sent usman a message about this, and if he says we need to write tests I will
		
- with regards to actual 'elif statements' we have forgotten to test, they are in the following lines for the following files:

Filename				Coverage	Lines
src/admin.py            97%   		63-68, 68-exit
src/auth.py             96%   		39-exit, 40-39
src/channel.py          73%		    80-81, 81, 114-113, 131-144, 152-154, 158-167, 210-211, 211, 241-245, 245-250
src/channels.py         92%		    55-56, 56, 90-91, 91
src/config.py           100%
src/dm.py               99%		    187-188, 188
src/echo.py              0%		    1-7
src/error.py            100%
src/other.py            100%
src/persistence.py       85%	    19-21
src/profile.py           33%   		7-14, 18-24, 28-35
src/token.py             90%   		50-53, 53, 59-63, 63
src/user.py             100%
src/users.py            100%
----------------------------------------------------------------
TOTAL                    87%

- I have tried to write tests for the profile and channel, but since I hardly know what is going on in there, it is difficult to write such specific edge test cases. Consider this line here:
	```python
    elif start + 49 <= message_length:
        end_return = end = start + 50
	```
	- since I do not understand this function I can't really write a good test for it. 
	- **I think the author of the implementation should write the test.**
	


