# (Bonus Marks) Extra Features

## Description of Additions: 

### Channel Bot
We have implemented 9 commands as part of our channel bot. Within the bot we have 3 main features among others: __1) Language Filter__, 2) __Poll Feature__, 3) __Timeout Feature__. 

This channel bot is a flexible feature that can be used in any channel once activated. The bot is in a default active state in any new channel that is created, and can only be deactivated or activated again by channel owners, unless there are no  owners in the channel. 

The 9 commands that we have implemented are described below. They can only be called if channel bot is active, except /abot to activate the bot. 

 1. /abot  
    Description
        - Activates the bot. 
        - Permissions: If channel has an owner, this command is only accessible by channel owners or global owners. If channel has no owners then bot can be activated by any channel member. 
        
    Args
        - None

    2. /dbot  
    Description
        - Deactivates the bot. 
        - Permissions: If channel has an owner, this command is only accessible by channel owners or global owners. If channel has no owners then bot can be activated by any channel member. 
    Args
        - None

    3. /timeout <targethandle> <length>  
    Description
        - Times out the channel member whose handle is specified for a specified length of seconds.
        - Permissions: Only a channel owner or global owner can access this command. 
        - This timedout user will not be able to send/edit any messages in the channel they are timed out in. 
        - Channel owners can timeout themselves. 
    Args
        - targethandle is the handle of the user you want to time out
        - length is the time of the timeout in seconds

    4. /clearchat  
    Description
        - Clears the chat of the channel it is used in.
        - Removes all messages in the channel. 
        - Permissions: Only channel owners or global owners can clear the chat
    Args
        None

    5. /reset  
    Description
        THIS IS ONLY TO  BE USED BY GLOBAL OWNERS, it serves as a hard reset.
        - resets the entire server
    Args
        None

    6. /startpoll <question> <option1> <option2> ...  
    Description
        - Initiates a poll in the specified channel. 
        - The bot will read as many options as inputted.
        - First argument will be considered the question.
        - Permissions: Any channel member can initiate a poll in a channel if the channel bot is active. 
    Args
        - question 
        - option (as many as needed)

    7. /addpolloption <option1> <option2> ...  
    Description
        - Adds options to existing poll, will read as many options as inputted
        - Permissions: Any channel member can add a poll option in a channel if the channel bot is active.
    Args
        - options (as many as needed) 

    8. /vote <option>  
    Description
        - Reads one option, considering that the option inputted is valid (case sensitive).
        - Permissions: Any channel member can vote as long as bot is activated. 
        - A user can only choose 1 option.
        - If a user has already voted, their vote will change to the option selected. 
    Args
        - option

    9. /endpoll  
    Description
        - Ends existing poll.
        - Permissions: Only the user who started the poll can end the poll. 
    Args
        - None



### Language Filter

- Runs every time a message is edited or sent in a channel with an active bot. 
- Checks messages for any swear words listed in swear_words list.
- If a swear word exists in a message that will be sent, replace the message with “This message has been removed due to profanity”. 
- If a user edits a message to a new message containing profanity, this message will also be removed and replaced with “This message has been removed due to profanity”. 
- If the user swears 3 times, they will be timed out for 20 seconds for every attempted message containing a swear word. i.e. if they swear 3 seconds, they will be timed out for 60 seconds. If they swear another 3 times, they will be timed out for 120 seconds. 

### Poll Feature
- A poll can only be started when the channel bot is activated. 
- Permissions: A poll can be started by any channel member. 
- A user can only vote for 1 option at a time. 
- Only 1 poll can run at any time within a channel
- Poll can only be ended by the user who started the poll. 
- Every time the poll is updated (either a poll is started, a new option is added, a vote is changed or added, or the poll is ended), the channel bot will send a message into the channel showing the updated poll statistics and the number of votes for each option with emojis next to each option representing the number of votes for that poll option. 
- See specific commands and their descriptions above (/startpoll, /endpoll, /vote, /addpolloption)

### Timeout Feature 
- Times out the channel member whose handle is specified for a specified length of seconds.
- The user who is timed out cannot send/edit messages during the timeout period. 
- Permissions: Only a channel owner or global owner can access this command. 
- This timedout user will not be able to send/edit any messages in the channel they are timed out in. 
- Channel owners can timeout themselves. 
- channel bot command "/timeout <targethandle> <length>"

