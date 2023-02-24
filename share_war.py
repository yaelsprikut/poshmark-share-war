import selenium, time, argparse, sys, os, textwrap
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from usernames import usernames



def rt(d):
    times = np.random.rand(1000)+np.random.rand(1000)+d
    return np.random.choice(times, 1).tolist()[0]


def login(debugger=False):

    if debugger is True:
        import pdb; pdb.set_trace()
    else:
        pass

    url = "https://poshmark.ca/login"
    driver.get(url)

    time.sleep(rt(5))

    try:
        ## Login
        print(textwrap.dedent('''
            [*] logging into Poshmark seller account: {}...
                the share war will begin momentarily...
            '''.format(poshmark_username)))
        username = driver.find_element_by_name("login_form[username_email]")
        username.send_keys(poshmark_username)
        time.sleep(rt(5))

        password = driver.find_element_by_name("login_form[password]")
        password.send_keys(poshmark_password)
        time.sleep(rt(5))

        password.send_keys(Keys.RETURN)
        time.sleep(rt(5))

        ## Check for Captcha
        try:
            captcha_pat = "//span[@class='base_error_message']"
            captcha_fail = driver.find_element_by_xpath(captcha_pat)
            if len(str(captcha_fail)) > 100:
                print(textwrap.dedent('''
                    [*] caught by captchas...
                    [*] please complete captchas
                        robots game before proceeding...
                    [*] please proceed to terminal debugger
                    '''))
                login(debugger=True)
                return
            else:
                pass
        except Exception as e:
            pass
 
        ## Navigate to Seller Page
        # time.sleep(rt(10))
        # seller_page = get_seller_page_url(args.account)
        # driver.get(seller_page)


        # ## Confirm Account to Share If Not Username
        # if args.bypass == True:
        #     pass
        # else:
        #     if args.account != poshmark_username:
        #         confirm_account_sharing(args.account, poshmark_username)
        #         if quit_input is True:
        #             return False
        #         else:
        #              pass
        #     else:
        #         pass

        return True

    except:
        ## Captcha Catch
        print(textwrap.dedent('''
            [*] ERROR in Share War: Thrwarted by Captchas
                you may now attempt to login with the python debugger
            '''))
        offer_user_quit()
        login(debugger=True)
        pass


def confirm_account_sharing(account, username):

        ## Get User Input
        print(textwrap.dedent('''
            [*] you have requested to share
                the items in another poshmark closet:
                ------------------------------------
                [*]: {}
                ------------------------------------
            '''.format(account)))
        confirm_mes = (textwrap.dedent('''
            [*] to confirm this request, enter [y]
                to cancel and share your closet items instead enter [n] :
            '''))

        confirm_selection = input(confirm_mes)
        cs = str(confirm_selection).lower()
        if cs == 'y':
            pass
        elif cs == 'n':
            ## Redirect to users's closet page
            seller_page = get_seller_page_url(username)
            driver.get(seller_page)
        else:
            print('[*] you have entered an invalid selection...')
            offer_user_quit()
            if quit_input is True:
                pass
            else:
               confirm_account_sharing(account, username)


def offer_user_quit():
    ## Provide Option to Quit
    quit_mes = textwrap.dedent('''
            [*] if you would like to quit, enter [q]
                otherwise, enter any other key to continue
            ''')
    quit_selection = input(quit_mes)
    qs = str(quit_selection).lower()
    if qs == 'q':
        global quit_input
        quit_input = True
    else:
        pass


def get_seller_page_url(poshmark_account):
    url_stem = 'https://poshmark.ca/closet/'
    available = '?availability=available'
    url = '{}{}{}'.format(url_stem, poshmark_account, available)
    return url


def scroll_page(n, delay=5):
    scroll = 0
    screen_heights = [0]

    print("[*] scrolling through all items in closet...")

    for i in range(1, n+1):
        scroll +=1
        scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll_script)
        height = driver.execute_script("return document.documentElement.scrollHeight")
        last_height = screen_heights[-1:][0]

        if height == last_height:
            return
        else:
            screen_heights.append(height)
            time.sleep(rt(delay))


def get_closet_urls():
    items = driver.find_elements_by_xpath("//div[@class='item-details']")
    urls = [i.find_element_by_css_selector('a').get_attribute('href') for i in items]
    return urls

def get_like_icons():
    print("Get like icons")
    item_pat = "//div[@class='social-action-bar tile__social-actions']"
    # item_pat = "//div[@class='d--fl ai--c cursor--pointer social-action-bar__action social-action-bar__like']"
    items = driver.find_elements_by_xpath(item_pat)
    like_icons = [i.find_element_by_css_selector(".social-action-bar__like") for i in items]
    return like_icons

def get_closet_share_icons():
    item_pat = "//div[@class='social-info social-actions d-fl ai-c jc-c']"
    items = driver.find_elements_by_xpath(item_pat)
    share_icons = [i.find_element_by_css_selector("a[class='share']") for i in items]
    if not share_icons:
        item_pat = "//div[@class='d--fl ai--c social-action-bar__action social-action-bar__share']"
        items = driver.find_elements_by_xpath(item_pat)
        share_icons = [i.find_element_by_css_selector(".share-gray-large") for i in items]
    return share_icons

def click_like_item(like_icon, d=3):
    print("Like item")
    ## First share click
    driver.execute_script("arguments[0].click();", like_icon); time.sleep(rt(d))

def clicks_share_followers(share_icon, d=5.5):
    ## First share click
    driver.execute_script("arguments[0].click();", share_icon); time.sleep(rt(d))

    ## Second share click
    try:
        share_pat = "//a[@class='pm-followers-share-link grey']"
        share_followers = driver.find_element_by_xpath(share_pat)
        driver.execute_script("arguments[0].click();", share_followers); time.sleep(rt(d))
    except:
        share_pat = "//a[@class='internal-share__link']"
        share_followers = driver.find_element_by_xpath(share_pat)
        driver.execute_script("arguments[0].click();", share_followers); time.sleep(rt(d))


def open_closet_item_url(url):
    print(url)
    driver.get(url)
    time.sleep(rt(5))


def deploy_share_war(n=3, order=True, random_subset=0):
    print("[*] DEPLOYING SHARE WAR")
    
    try:
        if login() is True:
            pass
        else:
            return
        ## Navigate to Seller Page
        for seller in usernames:
            seller_page = get_seller_page_url(seller)
            driver.get(seller_page)
            print("SELLER===> ", seller)

            ## Confirm Account to Share If Not Username
            if args.bypass == True:
                pass
            else:
                if seller != poshmark_username:
                    confirm_account_sharing(seller, poshmark_username)
                    if quit_input is True:
                        return False
                    else:
                        pass
                else:
                    pass
            scroll_page(n)

            ## Like Icons
            like_icons = get_like_icons()
            ## Share Icons and Order
            share_icons = get_closet_share_icons()

            if order is True:
                share_icons.reverse()
            else:
                pass

            ## Share Random Subset of Items
            if random_subset != 0:
                print("Getting Random Subset...")
                try: 
                    random_subset = int(random_subset)
                    print(textwrap.dedent('''
                        [*] you have selected to share a random subset of {} items
                            from all {} PoshMark listings in the closet...
                            please wait...
                        '''.format(random_subset, len(share_icons))))

                    like_icons = np.random.choice(like_icons, random_subset, replace=False).tolist()
                    share_icons = np.random.choice(share_icons, random_subset, replace=False).tolist()
                    print("like_icons: ", like_icons)
                    print("share_icons: ", share_icons)
                    time.sleep(rt(10))
                except:
                    pass
            else:
                pass
            print("second pass...")
            ## Share Message
            print(textwrap.dedent('''
                [*] sharing PoshMark listings for {} items in closet...
                    please wait...
                '''.format(len(share_icons))))
            
            ## Share Listings
            [click_like_item(item) for item in like_icons]
            [clicks_share_followers(item) for item in share_icons]
            print("[*] closet successfully shared...posh-on...")
            pass 
    except:
        print("[*] ERROR in Share War")
        pass
    exit()
    ## Closing Message
    loop_delay = int(random_loop_time/60)
    current_time = time.strftime("%I:%M%p on %b %d, %Y")
    print(textwrap.dedent('''
        [*] the share war will continue in {} minutes...
            current time: {}
        '''.format(loop_delay, current_time)))




if __name__=="__main__":

    ##################################
    ## Arguments for Script
    ##################################

    ## Default Arguments with RawTextHelpFormatter
    class RawTextArgumentDefaultsHelpFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter
        ):
            pass

    ## Check to ensure user has created the credentials.py file
    exists = os.path.isfile('./credentials.py')
    if not exists:
        print(textwrap.dedent('''
            [*] ERROR: `credentials.py` file does not exist.
                You may need to create the file, for example, 
                by copying `example_credentials.py`...

            [*] In terminal, enter the following command:
                cp example_credentials.py credentials.py

            [*] Then edit credentials.py with your
                poshmark closet and password.
                '''))
        sys.exit()
    else:
        import credentials


    ## Fail gracefully if the username or password not specified
    try:
        poshmark_username = credentials.poshmark_username
        poshmark_password = credentials.poshmark_password
    except AttributeError:
        print(textwrap.dedent('''
            [*] ERROR: Username and/or password not specified...
            [*] You may need to uncomment poshmark_username and 
                poshmark_password in credentials.py
            '''))
        sys.exit()

    ## Poshmark closet URL only works with username, so verify
    ## that the user is not using their email address to log in.
    if '@' in poshmark_username:
        print(textwrap.dedent('''
                    [*] Do not your user email address to log in...
                        use your Poshmark username (closet) instead...
                    '''))
        sys.exit()


    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
        [*] Help file for share_war.py
            from the poshmark_sharing repository:
            https://github.com/jmausolf/poshmark_sharing
        '''),
        usage='use "python %(prog)s --help" for more information',
        formatter_class=RawTextArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--time", default=7200, type=float, 
        help=textwrap.dedent('''\
            loop time in seconds to repeat the code

            :: example, repeat in two hours:
            -t 7200
            '''))
    parser.add_argument("-n", "--number", default=1000, type=int, 
        help="number of closet scrolls")
    parser.add_argument("-o", "--order", default=True, type=bool, 
        help="preserve closet order")
    parser.add_argument("-r", "--random_subset", default=0, type=int, 
        help="select a random subset (number) of items to share")
    parser.add_argument("-a", "--account", default=poshmark_username, 
        type=str,help=textwrap.dedent('''\
            the poshmark closet account you want to share
            (default is the login account in credentials.py)

            :: example, share another user's closet items:
            -a another_username
            '''))
    parser.add_argument("-b", "--bypass", default=False, type=bool, 
        help=textwrap.dedent('''\
            option to bypass user confirmation
            by default, if the account to be shared is not equal
            to the poshmark username, the user will be prompted to 
            confirm this selection

            :: example, bypass user confirmation
            -b True
            '''))
    parser.add_argument("-d", "--driver", default='0', type=str, 
        help=textwrap.dedent('''\
            selenium web driver selection
            drivers may be called by either entering the name
            of the driver or entering the numeric code 
            for that driver name as follows:
            Firefox==0, Chrome==1, Edge==2, Safari==3

            :: example, use Firefox:
            -d Firefox 
            -d 0

            :: example, use Chrome:
            -d Chrome
            -d 1
            '''))

    args = parser.parse_args()


    ##################################
    ## Run Script
    ##################################

    ## Start Share War Loop
    starttime = time.time()

    while True:

        ## Select and Start Webdriver
        try:
            ## Try to start driver
            if args.driver == '0' or args.driver == 'Firefox':
                driver = webdriver.Firefox()
            elif args.driver == '1' or args.driver == 'Chrome':
                driver = webdriver.Chrome()
            elif args.driver == '2' or args.driver == 'Edge':
                driver = webdriver.Edge()
            elif args.driver == '3' or args.driver == 'Safari':
                driver = webdriver.Safari()
            else:
                print(textwrap.dedent('''
                    [*] ERROR Driver argument value not supported!
                        Check the help (-h) argument for supported values.
                    '''))

            ## Driver Implicit Wait
            driver.implicitly_wait(0)

        except NameError:
            print(textwrap.dedent('''
                [*] ERROR You don't have the web driver for argument
                    given ({}) you need to download it, go here for
                    installation info:
                    https://selenium-python.readthedocs.io/installation.html#drivers
                '''.format(args.driver)))
            sys.exit()

        except Exception as e:
            print(textwrap.dedent('''
                [*] ERROR the selected driver may not be setup correctly. 
                    Ensure you can access it from the command line and 
                    try again. 
                    {}
                '''.format(e)))
            sys.exit()

        else:
            pass

        ## Time Delay: While Loop
        random_loop_time = rt(args.time)

        ## Run Main App
        quit_input = False
        deploy_share_war(args.number, args.order, args.random_subset)

        if quit_input is False:
            time.sleep(rt(10))
            driver.close()

            ## Time Delay: While Loop
            time.sleep(random_loop_time - ((time.time() - starttime) % 
                random_loop_time))
        else:
            driver.close()
            sys.exit()