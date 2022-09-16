import tweepy
import pandas as pd

def fetch_contacts(api, user_list, contacts):
    """
        Obtains friends and followers of users from a given list of users.

        - if contacts = 'friends' fetches the profiles followed by each user in the list;
        - if contacts = 'followers' fetches the profiles following each user in the list;
        - if contacts = 'all', performs both operations.

        The contacts are stored in a DataFrame, where each row represents an instance of a relationship
        i.e. the profile in the 'source' col follows the profile in the 'target' col.
    
    :param List[twitter.Api] api: a list with one or more Twitter API instances;
    :param list user_list: a list of userIDs to fetch friends and followers from;
    :param str contacts: the kind of contacts wanted for each user in the list:
        'friends' are profiles followed by the user(s);
        'followers' are profiles following the user(s);
        'all' is the union of friends and followers.
    :return: a DataFrame with friends, followers or both for each userID. 
    """
    df = pd.DataFrame(columns=['source','target']) # empty df

    if contacts == 'friends':
    # fetching friends
        for userID in user_list:
            friends = []
            friends_list = []
            # fetching the user
            user = api.get_user(user_id=userID)
            # fetching the friends_count
            friends_count = user.friends_count
            try:
                for page in tweepy.Cursor(api.get_friend_ids, user_id=userID).pages():
                    friends.extend(page)
                    print(user.screen_name, 'follows', len(friends), 'profiles')
                    if friends_count >= 5000: #Only take first 5000 friends
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            friends_list.append(friends)
            temp1 = pd.DataFrame(columns=['source', 'target'])
            temp1['target'] = friends_list[0] # set the list of friends as the target column
            temp1['source'] = userID # set the user ID as the source 
            df = df.append(temp1)

    elif contacts == 'followers':
    # fetching followers
        for userID in user_list:
            followers = []
            follower_list = []
            # fetching the user
            user = api.get_user(user_id=userID)
            # fetching the followers_count
            followers_count = user.followers_count
            try:
                for page in tweepy.Cursor(api.get_follower_ids, user_id=userID).pages():
                    followers.extend(page)
                    print(user.screen_name, 'is followed by', len(followers), 'profiles')
                    if followers_count >= 5000: #Only take first 5000 followers
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            follower_list.append(followers)
            temp2 = pd.DataFrame(columns=['source', 'target'])
            temp2['source'] = follower_list[0] # set the list of followers as the source column
            temp2['target'] = userID # set the user ID as the target (user is followed by followers)
            df = df.append(temp2)
            
    elif contacts == 'all':
    # fetching friends
        for userID in user_list:
            friends = []
            friends_list = []
            # fetching the user
            user = api.get_user(user_id=userID)
            # fetching the friends_count
            friends_count = user.friends_count
            try:
                for page in tweepy.Cursor(api.get_friend_ids, user_id=userID).pages():
                    friends.extend(page)
                    if friends_count >= 5000: #Only take first 5000 friends
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            friends_list.append(friends)
            temp1 = pd.DataFrame(columns=['source', 'target'])
            temp1['target'] = friends_list[0] # set the list of friends as the target column
            temp1['source'] = userID # set the user ID as the source 
            df = df.append(temp1)
    # fetching followers
        for userID in user_list:
            followers = []
            follower_list = []
            # fetching the user
            user = api.get_user(user_id=userID)
            # fetching the followers_count
            followers_count = user.followers_count
            try:
                for page in tweepy.Cursor(api.get_follower_ids, user_id=userID).pages():
                    followers.extend(page)
                    print(user.screen_name, 'follows', len(friends), 'profiles \n', 
                        user.screen_name, 'is followed by', len(followers), 'profiles')
                    if followers_count >= 5000: #Only take first 5000 followers
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            follower_list.append(followers)
            temp2 = pd.DataFrame(columns=['source', 'target'])
            temp2['source'] = follower_list[0] # set the list of followers as the source column
            temp2['target'] = userID # set the user ID as the target (user is followed by followers)
            df = df.append(temp2)    
    else: 
        raise ValueError("Unknown mode: contacts should be one of 'friends', 'followers', 'all'")
    return df 
    
def fetch_contacts_named(api, user_list, contacts):
    """
        Obtains friends and followers of users from a given list of users.

        - if contacts = 'friends' fetches the profiles followed by each user in the list;
        - if contacts = 'followers' fetches the profiles following each user in the list;
        - if contacts = 'all', performs both operations.

        The contacts are stored in a DataFrame, where each row represents an instance of a relationship
        i.e. the profile in the 'source' col follows the profile in the 'target' col.
    
    :param List[twitter.Api] api: a list with one or more Twitter API instances;
    :param list user_list: a list of screen names of users to fetch friends and followers from;
    :param str contacts: the kind of contacts wanted for each user in the list:
        'friends' are profiles followed by the user(s);
        'followers' are profiles following the user(s);
        'all' is the union of friends and followers.
    :return: a DataFrame with friends, followers or both for each screen name in the user_list. 
    """
    df = pd.DataFrame(columns=['source','target']) # empty df

    if contacts == 'friends':
    # fetching friends
        for u in user_list:
            friends = []
            friends_list = []
            # fetching the user
            user = api.get_user(screen_name=u)
            # fetching the friends_count
            friends_count = user.friends_count
            try:
                for page in tweepy.Cursor(api.get_friends, screen_name=u).pages():
                    friends.extend(page)
                    if friends_count >= 5000: #Only take first 5000 friends
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            print(user.screen_name, 'follows', len(friends), 'profiles')
            # appending names to friend list
            for friend in friends:
                friends_list.append(friend.screen_name)
            temp1 = pd.DataFrame(columns=['source', 'target'])
            temp1['target'] = friends_list # set the list of friends as the target column
            temp1['source'] = u # set the user ID as the source 
            df = df.append(temp1)

    elif contacts == 'followers':
    # fetching followers
        for u in user_list:
            followers = []
            follower_list = []
            # fetching the user
            user = api.get_user(screen_name=u)
            # fetching the followers_count
            followers_count = user.followers_count
            try:
                for page in tweepy.Cursor(api.get_followers, screen_name=u).pages():
                    followers.extend(page)
                    if followers_count >= 5000: #Only take first 5000 followers
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            print(user.screen_name, 'is followed by', len(followers), 'profiles')
            # appending names to followers list
            for follower in followers:
                follower_list.append(follower.screen_name)
            temp2 = pd.DataFrame(columns=['source', 'target'])
            temp2['source'] = follower_list # set the list of followers as the source column
            temp2['target'] = u # set the user ID as the target (user is followed by followers)
            df = df.append(temp2)
            
    elif contacts == 'all':
    # fetching friends
        for u in user_list:
            friends = []
            friends_list = []
            # fetching the user
            user = api.get_user(screen_name=u)
            # fetching the friends_count
            friends_count = user.friends_count
            try:
                for page in tweepy.Cursor(api.get_friends, screen_name=u).pages():
                    friends.extend(page)
                    if friends_count >= 5000: #Only take first 5000 friends
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            # appending names to friend list
            for friend in friends:
                friends_list.append(friend.screen_name)
            temp1 = pd.DataFrame(columns=['source', 'target'])
            temp1['target'] = friends_list # set the list of friends as the target column
            temp1['source'] = u # set the user ID as the source 
            df = df.append(temp1)
    # fetching followers
        for u in user_list:
            followers = []
            follower_list = []
            # fetching the user
            user = api.get_user(screen_name=u)
            # fetching the followers_count
            followers_count = user.followers_count
            try:
                for page in tweepy.Cursor(api.get_followers,screen_name=u).pages():
                    followers.extend(page)
                    if followers_count >= 5000: #Only take first 5000 followers
                        break
            except tweepy.TweepyException:
                print("error")
                continue
            print(user.screen_name, 'follows', len(friends), 'profiles \n', 
                user.screen_name, 'is followed by', len(followers), 'profiles')
            for follower in followers:
                follower_list.append(follower.screen_name)
            temp2 = pd.DataFrame(columns=['source', 'target'])
            temp2['source'] = follower_list # set the list of followers as the source column
            temp2['target'] = u # set the user ID as the target (user is followed by followers)
            df = df.append(temp2)    
    else: 
        raise ValueError("Unknown mode: contacts should be one of 'friends', 'followers', 'all'")
    return df 

def fetch_network(api, userID):
    """
        Fetches the network of relationships of a given userID: 
        its friends, followers and their relationships between each other 
    """
    df = pd.DataFrame(columns=['source','target']) # empty df
    
    # fetching friends
    friends = []
    friends_list = []
    # fetching the user
    user = api.get_user(user_id=userID)
    friends_count = user.friends_count
    try:
        for page in tweepy.Cursor(api.get_friend_ids, user_id=userID).pages():
            friends.extend(page)
            print(user.screen_name, 'follows', len(friends), 'profiles')
            if friends_count >= 5000: #Only take first 5000 friends
                break
    except tweepy.TweepyException:
        print("error")
    friends_list.append(friends)
    temp1 = pd.DataFrame(columns=['source', 'target'])
    temp1['target'] = friends_list[0] # set the list of friends as the target column
    temp1['source'] = userID # set the user ID as the source 
    df = df.append(temp1)

    # fetching followers
    followers = []
    follower_list = []
    followers_count = user.followers_count 
    try:
        for page in tweepy.Cursor(api.get_follower_ids, user_id=userID).pages():
            followers.extend(page)
            print(user.screen_name, 'is followed by', len(followers), 'profiles')
            if followers_count >= 5000: #Only take first 5000 followers
                break
    except tweepy.TweepyException:
        print("error")
    follower_list.append(followers)
    temp2 = pd.DataFrame(columns=['source', 'target'])
    temp2['source'] = follower_list[0] # set the list of followers as the source column
    temp2['target'] = userID # set the user ID as the target (user is followed by followers)
    df = df.append(temp2) 
    
    # friends of friends
    for friend_id in temp1['target']:
        friends_of_friends = []
        friends_of_friends_list = []
        # fetching the user
        try:
            user = api.get_user(user_id=friend_id)
        except tweepy.TweepyException:
            continue    
        # fetching the friends_count and followers_count
        friends_of_friends_count = user.friends_count
        try:
            for page in tweepy.Cursor(api.get_friend_ids, user_id=friend_id).pages():
                friends_of_friends.extend(page)
                print(user.screen_name, 'follows', len(friends_of_friends), 'profiles')
                if friends_of_friends_count >= 5000: #Only take first 5000 friends
                    break
        except tweepy.TweepyException:
            print("error")
            continue
        friends_of_friends_list.append(friends_of_friends)
        temp3 = pd.DataFrame(columns=['source', 'target'])
        temp3['target'] = friends_of_friends_list[0] # set the list of friends as the target column
        temp3['source'] = friend_id # set the user ID as the source 
        df = df.append(temp3)
    
    # friends of followers
    for follower_id in temp2['source']:
        friends_of_followers = []
        friends_of_followers_list = []
        # fetching the user
        try:
            user = api.get_user(user_id=follower_id)
        except tweepy.TweepyException:
            continue    
        # fetching the friends_count and followers_count
        friends_of_followers_count = user.followers_count
        try:
            for page in tweepy.Cursor(api.get_friend_ids, user_id=follower_id).pages():
                friends_of_followers.extend(page)
                print(user.screen_name, 'follows', len(friends_of_followers), 'profiles')
                if friends_of_followers_count >= 5000: #Only take first 5000 friends
                    break
        except tweepy.TweepyException:
            print("error")
            continue
        friends_of_followers_list.append(friends_of_followers)
        temp4 = pd.DataFrame(columns=['source', 'target'])
        temp4['target'] = friends_of_followers_list[0] # set the list of friends as the target column
        temp4['source'] = follower_id # set the user ID as the source 
        df = df.append(temp4)
    return df

def twitter_monitor(api, user_list):
  """
    Fetches a list of features from each account in user_list and saves them into a DataFrame

  :param List[twitter.Api] api: a list with one or more Twitter API instances;
  :param list user_list: a list of screen names of users to fetch features from;
  :returns: a DataFrame where each row represents a user and each column a feature.
  """
  df = pd.DataFrame(columns=['screen_name','description', 'statuses_count', 'friends_count', 'followers_count',
                            'account_age_days', 'average_tweets'])
  for account in user_list:
    temp = pd.DataFrame(columns=['screen_name','description', 'statuses_count', 'friends_count', 'followers_count', 
                                'account_age_days', 'average_tweets'])
    user = api.get_user(screen_name=account)
    temp['screen_name'] = str(user.screen_name)
    temp['description'] = str(user.description)
    temp['statuses_count'] = str(user.statuses_count)
    temp['friends_count'] = str(user.friends_count)
    temp['followers_count'] = str(user.followers_count)
    tweets = str(user.statuses_count)
    account_created_date = user.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    temp['average_tweets'] = 0
    if account_age_days > 0:
      average_tweets = str(round(int(tweets)/int(account_age_days),2))
    temp['account_age_days'] = str(account_age_days)

    df = df.append(temp)
  return df