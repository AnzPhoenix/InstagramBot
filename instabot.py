from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import configparser
import random
import pandas
import csv

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.login()

    def login(self):
        self.driver.get('https://instagram.com/accounts/login')
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_name('password').send_keys(Keys.RETURN)
        sleep(5)

    def nav_user(self, user):
        self.driver.get('https://instagram.com/' + user)

    def nav_hashtag(self, hashtag):
        self.driver.get('https://instagram.com/explore/tags/' + hashtag)

    def follow_user(self, user):
        self.nav_user(user)
        follow_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        follow_button.click()

    def like_user_post(self, user):
        self.nav_user(user)
        photo = self.driver.find_element_by_class_name('eLAPa')
        photo.click()
        self.driver.implicitly_wait(10)
        like_btn = self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button")
        next_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
        for i in range(10):
            self.driver.implicitly_wait(10)
            try:
                like_btn.click()
                sleep(2)
                next_btn.click()
                sleep(2)
            except:
                like_btn = self.driver.find_element_by_css_selector('.fr66n > button:nth-child(1)')
                like_btn.click()
                sleep(2)
                next_btn.click()
                sleep(2)

    def like_hashtag_post(self, hashtag):
        self.nav_hashtag(hashtag)
        post = self.driver.find_element_by_class_name('eLAPa')
        post.click()
        self.driver.implicitly_wait(10)
        like_button = self.driver.find_element_by_css_selector('.fr66n > button:nth-child(1)')
        next_button = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
        for i in range(10):
            try:
                like_button.click()
                self.driver.implicitly_wait(2)
                next_button.click()
                self.driver.implicitly_wait(random.randint(5, 15))
            except:
                like_button = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                like_button.click()
                self.driver.implicitly_wait(2)
                next_button.click()
                self.driver.implicitly_wait(random.randint(5,15))

    #Call this every time the script starts and every time the scripts follows people
    def write_followers_to_csv(self):
        self.driver.get('https://www.instagram.com/' + username)
        self.driver.implicitly_wait(2)
        #finds the number of followers for future reference
        num_of_followers = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text
        int_num_of_followers = int(num_of_followers)
        self.driver.implicitly_wait(2)
        #finds the follower button
        followers_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        followers_button.click()
        self.driver.implicitly_wait(10)
        #finds an initial anchor point, creates an empty list
        anchor_point = self.driver.find_element_by_css_selector('.PZuss > li:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)')
        follower_list = []
        num_of_down_clicks = 0
        #while the number of followers is more than the number of end key clicks, click the end key and add 1 to number of end clicks
        while int_num_of_followers > num_of_down_clicks:
            anchor_point.send_keys(Keys.END)
            #refreshes the anchor point every iteration
            anchor_point = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[2]/button')
            num_of_down_clicks += 1

        #finds all the elements with this xpath(the square brackets next to the li element specifies which username)
        followers = self.driver.find_elements_by_xpath(
            "/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a")

        #iterates through the list of usernames and takes the text and puts it into the follower_list list
        for i in followers:
            self.driver.implicitly_wait(2)
            follower_list.append(i.text)


        #switches back to the profile page
        self.driver.get('https://www.instagram.com/techarchlight')

        #gets the amount of people that admin is following and concatenates it into a integer
        num_of_following = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
        int_num_of_following = int(num_of_following)

        following_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
        following_button.click()

        #finds an anchor point, creates an empty list, and declares the number of end clicks for the following list
        self.driver.implicitly_wait(10)
        following_anchor_point = self.driver.find_element_by_css_selector('.PZuss > li:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)')
        following_list = []
        following_num_of_down_clicks = 0

        while int_num_of_following > following_num_of_down_clicks:
            following_anchor_point.send_keys(Keys.END)

            #refreshes the anchor point every iteration

            following_anchor_point = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[2]/button')
            following_num_of_down_clicks += 1

        followings = self.driver.find_elements_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a')

        for i in followings:
            self.driver.implicitly_wait(2)
            following_list.append(i.text)

        #because of how pandas work the length of each column needs to be the same size therefore:
        #if the length of follower list is less than the length of following list
        if len(follower_list) < len(following_list):
            #while the length of follower list is less than the length of following list it will append empty strings into the list
            while len(follower_list) < len(following_list):
                follower_list.append('')
        #else if the length of following list is less than the length of follower list
        elif len(following_list) < len(follower_list):
            #while the length of following list is lesss than the length of follower list, append empty strings
            while len(following_list) < len(follower_list):
                following_list.append('')

        #stores the list data into the data varaible and turns it into a dataframe; writes the dataframe into followers - Sheet1.csv
        data = {'Followers': follower_list, 'Following': following_list}
        dataframe = pandas.DataFrame(data=data)
        dataframe.to_csv('followers - Sheet1.csv')

    def follow_post_likers(self, hashtag):
        self.driver.get('https://www.instagram.com/' + username)
        self.driver.implicitly_wait(2)
        #finds the number of followers for future reference
        num_of_followers = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text
        int_num_of_followers = int(num_of_followers)

        #gets the amount of people that admin is following and concatenates it into a integer
        num_of_following = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
        int_num_of_following = int(num_of_following)

        #number of new people followed or the number of iterations the for loop in total
        iteration_num = 0
        new_num_of_following = int_num_of_following + iteration_num

        self.nav_hashtag(hashtag)
        post = self.driver.find_element_by_class_name('eLAPa')
        post.click()
        self.driver.implicitly_wait(2)

        #number of iterations the while loop went through
        while_loop_iteration = 0
        #if the number of people the account is following is less than 600
        if new_num_of_following < 600:
            #while the number of people the account is following is less than 600
            while new_num_of_following < 600:
                new_num_of_following = int_num_of_following + iteration_num
                self.driver.implicitly_wait(10)
                try:
                    #find the liked by button
                    liked_by_button = self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/div/div[3]/section[2]/div/div[1]/button')
                    liked_by_button.click()
                    self.driver.implicitly_wait(2)
                except:
                    if while_loop_iteration < 1:
                        next_button = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
                        next_button.click()
                        sleep(random.randint(1, 3))
                    else:
                        next_button = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]')
                        next_button.click()
                        sleep(random.randint(1, 3))

                    while_loop_iteration += 1

                #changes the [] on the div before div[3]/button
                div_num = 1

                #follows the first 10 people on the liked by list
                for i in range(10):
                    try:
                        follow_button = self.driver.find_element_by_xpath(
                            '/html/body/div[5]/div/div/div[2]/div/div/div' + '[' + str(div_num) + ']' '/div[3]/button')
                        #checks if the button says follow
                        if follow_button.text == 'Follow':
                            follow_button.click()
                            iteration_num += 1
                            div_num += 1
                            sleep(random.randint(1,3))
                        else:
                            div_num += 1
                            sleep(random.randint(1,3))
                    except:
                        break

                #closes the popup window
                close_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button')
                close_button.click()

                #makes sure that the next button is clicked instead of the previous button
                if while_loop_iteration < 1:
                    next_button = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
                    next_button.click()
                    sleep(random.randint(1,3))
                else:
                    next_button = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]')
                    next_button.click()
                    sleep(random.randint(1,3))

                while_loop_iteration += 1

        else:
            self.write_followers_to_csv()

    def unfollow_not_following_back(self):
        self.write_followers_to_csv()
        sleep(random.randint(3,5))

        self.driver.get('https://www.instagram.com/' + username)
        self.driver.implicitly_wait(2)
        #finds the number of followers for future reference
        num_of_followers = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text
        int_num_of_followers = int(num_of_followers)
        self.driver.implicitly_wait(2)
        #finds the follower button
        followers_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        followers_button.click()
        self.driver.implicitly_wait(10)
        #finds an initial anchor point, creates an empty list
        anchor_point = self.driver.find_element_by_css_selector('.PZuss > li:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)')
        follower_list = []
        num_of_down_clicks = 0
        #while the number of followers is more than the number of end key clicks, click the end key and add 1 to number of end clicks
        while int_num_of_followers > num_of_down_clicks:
            anchor_point.send_keys(Keys.END)
            #refreshes the anchor point every iteration
            anchor_point = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[2]/button')
            num_of_down_clicks += 1

        #finds all the elements with this xpath(the square brackets next to the li element specifies which username)
        followers = self.driver.find_elements_by_xpath(
            "/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a")

        #iterates through the list of usernames and takes the text and puts it into the follower_list list
        for i in followers:
            self.driver.implicitly_wait(2)
            follower_list.append(i.text)


        #switches back to the profile page
        self.driver.get('https://www.instagram.com/techarchlight')

        #gets the amount of people that admin is following and concatenates it into a integer
        num_of_following = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
        int_num_of_following = int(num_of_following)

        following_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
        following_button.click()

        #finds an anchor point, creates an empty list, and declares the number of end clicks for the following list
        self.driver.implicitly_wait(10)
        following_anchor_point = self.driver.find_element_by_css_selector('.PZuss > li:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)')
        following_list = []
        following_num_of_down_clicks = 0

        while int_num_of_following > following_num_of_down_clicks:
            following_anchor_point.send_keys(Keys.END)

            #refreshes the anchor point every iteration

            following_anchor_point = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[2]/button')
            following_num_of_down_clicks += 1

        followings = self.driver.find_elements_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a')

        for i in followings:
            self.driver.implicitly_wait(2)
            following_list.append(i.text)

        sleep(random.randint(3,10))

        for i in following_list:
            try:
                if i not in follower_list:
                #go to the user's profile and unfollow
                    self.driver.get('https://instagram.com/' + i)
                    self.driver.implicitly_wait(2)
                    try:
                        sleep(random.randint(15,45))
                        unfollow_button = self.driver.find_element_by_xpath(
                            '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button')
                    except:
                        unfollow_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button')
                    unfollow_button.click()
                    sleep(random.randint(15,45))
                    #if there is a popup to confirm unfollow
                    try:
                        confirm_unfollow_button = self.driver.find_element_by_xpath(
                            '/html/body/div[4]/div/div/div/div[3]/button[1]')
                        confirm_unfollow_button.click()
                        sleep(random.randint(15, 30))
                    except:
                        continue
                else:
                    continue
            except:
                continue



if __name__ == '__main__':

    #for login credentials
    config_path = './config.ini'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)
    cparser.read(config_path)
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']

    #for reading follower and following list
    #datafile = pandas.read_csv('followers - Sheet1.csv')

    #creates a list for followers
    #follower = datafile.Followers

    #creates a list for following
    #following = datafile.Following

    ig_bot = InstaBot(username, password)

# ig_bot.follow_post_likers('pcbuilds')
# sleep(random.randint(3,5))
script_on = True
while script_on == True:
    ig_bot.unfollow_not_following_back()
    sleep(random.randint(30,60))
    ig_bot.follow_post_likers('pcbuilds')
    sleep(random.randint(30, 60))
