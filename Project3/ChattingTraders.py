#Chatting Traders: Group Alpha
#By Julia Volpe and Ej Birch

import os
import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# DZ: Do not use absolute paths
PREFIX_DIR = ''#'/Users/juliavolpe/Desktop/Alpha-ds/Project3/'
USERS_FILE = 'users.tsv'
MESSAGES_FILE = 'messages.tsv'
DISCUSSIONS_FILE = 'discussions.tsv'
DISCUSSION_POSTS_FILE = 'discussion_posts.tsv'

# DZ: Why do you need all these functions?
def readUsers():
    df = pd.read_csv(PREFIX_DIR + USERS_FILE, delimiter = "\t")
    return df

def readMessages():
    df = pd.read_csv(PREFIX_DIR + MESSAGES_FILE, delimiter = "\t")
    return df

def readDiscussions():
    df = pd.read_csv(PREFIX_DIR + DISCUSSIONS_FILE, delimiter = "\t")
    return df

def readDiscussionPosts():
    df = pd.read_csv(PREFIX_DIR + DISCUSSION_POSTS_FILE, delimiter = "\t")
    return df

def merge():
    users = readUsers()
    messages = readMessages()
    discussions = readDiscussions()
    discussionPosts = readDiscussionPosts()
    users.rename(columns = {'id':'userid'}, inplace = True)
    messages.rename(columns = {'id':'msgid'}, inplace = True)
    discussions.rename(columns = {'id':'discussionid'}, inplace = True)
    discussionPosts.rename(columns = {'id':'postid', 'createDate':'postCreateDate'}, inplace = True)
    merged = users.join(messages.set_index(['sender_id']), on = ['userid'])
    merged = merged.join(discussions.set_index(['creator_id']), on=['userid'], how = 'outer')
    merged = merged.join(discussionPosts.set_index(['discussion_id','creator_id']), on = ['discussionid','userid'], how = 'outer')
    print(merged)
    return merged

def discussionsChart(df):
    colors = ['red', 'blue', 'yellow', 'green', 'orange', 'pink', 'purple', 'brown']
    num = df['discussionCategory'].value_counts(dropna = True)
    dp = num.plot.pie(y = 'userid', figsize = (10, 6),labels = num.tolist(), legend = None, shadow = False, startangle = 0, colors = colors)
    plt.legend(labels = num.index, loc = 'best', bbox_to_anchor = (1.0,1.1))
    plt.title('Discussion Types')
    plt.savefig('discussion-types.png', dpi = 200)
    plt.close()

def messagesChart(df):
    colors = ['blue', 'red']
    num = df['type'].value_counts(dropna = True)
    num.plot.pie(y = 'userid',figsize = (10, 6), legend = None, autopct = '%1.1f%%', shadow = False, startangle = 0, colors = colors)
    plt.legend(labels = num.index, loc = 'best', bbox_to_anchor = (1.5,1.1))
    plt.title('Message Types')
    plt.savefig('message-types.png', dpi = 200)
    plt.close()
    return num.keys().tolist()

def discussionDistribution(df):
    colors = ['red', 'blue', 'yellow', 'orange', 'green', 'pink', 'purple', 'brown']
    num = df[['postid', 'discussionCategory']].drop_duplicates()
    num = num.groupby(['discussionCategory']).count()
    num.plot.pie(y = 'postid', figsize = (10, 6), legend = None, autopct = '%1.1f%%', shadow = False, startangle = 0, colors = colors)
    plt.legend(labels = num.index, loc = 'best', bbox_to_anchor = (1.0,1.1))
    plt.title('Discussion Categories Distribution')
    plt.savefig('discussion-distribution.png', dpi = 200)
    plt.close()

def messageActivity(df):
    df2 = df[['postid', 'memberSince', 'sendDate']].drop_duplicates()
    df2.set_index('postid', inplace = True)
    df3 = df2.sendDate-df2.memberSince
    df3.hist(bins = 100)
    plt.title('Message Activity Delay')
    plt.xlabel('Category')
    plt.ylabel('Time')
    plt.savefig('post-activity.png')
    plt.close()
    return df3.dropna().tolist()

def postActivity(df):
    num = df[['postid','discussionCategory']].drop_duplicates()
    num = num.groupby(['discussionCategory']).count().idxmax()
    df4 = df[df['discussionCategory'] == num.postid]
    df2 = df4[['postid','memberSince','createDate']].drop_duplicates()
    df2.set_index('postid', inplace = True)
    df3 = df2.createDate - df2.memberSince
    df3.hist(bins = 100)
    plt.title('Post Activity Delay')
    plt.xlabel('Category')
    plt.ylabel('Time')
    plt.savefig('post-activity.png')
    plt.close()
    return df3.dropna().tolist()

def activityRange(df):
    df2 = df[['userid','createDate']].drop_duplicates()
    df3 = df2.groupby(['userid']).agg({'createDate':[np.min, np.max]}).diff()
    df4 = df3['createDate']['amin']
    df4.hist(bins = 100)
    plt.title('Activity Range')
    plt.xlabel('First Message')
    plt.ylabel('Last Message')
    plt.savefig('activity-range.png')
    plt.close()
    return df3['createDate']['amin'].dropna().tolist()

def displayBoxPlot(df, result):
    message_type = result['messageType']
    post_activity = result['postActivity']
    activity_range = result['range']
    plt.boxplot(message_type, post_activity, activity_range)
    plt.show()

def displayTimes(df):
    sendDates = set(pd.to_datetime(df.dropna(subset=['sendDate'])['sendDate'], unit = 'ms'))
    print('\nThe time difference between the first message sent and the last message sent is: ' + str(max(sendDates) - min(sendDates)))
    discussions = readDiscussions()
    creationDates = set(pd.to_datetime(discussions['createDate'], unit = 'ms'))
    print('\nThe time difference between the first discussion creation date and the last discussion creation date is: ' + str(max(creationDates) - min(creationDates)))
    users = readUsers()
    accountDates = set(pd.to_datetime(users['memberSince'], unit = 'ms'))
    print('\nThe time difference between the first account creation date and the last account creation date is: ' + str(max(accountDates) - min(accountDates)))
    discussionPosts = readDiscussionPosts()
    discussionPostDates = set(pd.to_datetime(discussionPosts['createDate'], unit = 'ms'))
    print('\nThe time difference between the first discussion post creation date and the last discussion post creation date is: ' + str(max(discussionPostDates) - min(discussionPostDates)))

def main():
    df = merge()
    result = dict()
    print('\nThe number of users in the data base is', df.userid.iloc[-1], '.')
    displayTimes(df)    
    result['messageType'] = messagesChart(df)
    discussionsChart(df)
    print('\nThe number of discussion posts is', len((df['postid'].value_counts(dropna = True))), '.')
    result['range'] = activityRange(df)
    result['msgActivity'] = messageActivity(df)
    discussionDistribution(df)
    result['postActivity'] = postActivity(df)

if __name__ == "__main__":
    main()
