from selenium.webdriver.common.by import By

LOGIN_SELECTORS = {
    'email': (By.CSS_SELECTOR, '.email'),
    'password': (By.CSS_SELECTOR, '.loginPassword input'),
    'login': (By.CSS_SELECTOR, '.primary'),
}

CREATE_USER_SELECTORS = {
    'email': (By.CSS_SELECTOR, '#userEmail'),
    'password': (By.CSS_SELECTOR, '#userPassword'),
    'continue': (By.CSS_SELECTOR, '.continueButton'),
    'name': (By.CSS_SELECTOR, '#userFullName'),
    'age': (By.CSS_SELECTOR, '#userAge'),
    'female': (By.CSS_SELECTOR, 'input[value=female]'),
    'sign_up': (By.CSS_SELECTOR, '.signup'),
    'next': (By.CSS_SELECTOR, '.medium'),
    'follows': (By.CSS_SELECTOR, '.FollowButton'),
    'done': (By.CSS_SELECTOR, '.nuxModalPickerInterestButton'),
    'skip': (By.CSS_SELECTOR, '.optionalSkip'),
    'confirm': (By.CSS_SELECTOR, '.confirm'),
    'country': (By.CSS_SELECTOR, 'option[value=US]'),
    'change_photo': (By.CSS_SELECTOR, '.changePhoto'),
    'choose_file': (By.CSS_SELECTOR, 'input[name=file]'),
    'username': (By.CSS_SELECTOR, '#userUserName'),
    'about': (By.CSS_SELECTOR, '#userAbout'),
    'location': (By.CSS_SELECTOR, '#userLocation'),
    'save_settings': (By.CSS_SELECTOR, '.saveSettingsButton'),
}

CREATE_BOARDS_SELECTORS = {
    'create_board1': (By.CSS_SELECTOR, '.BoardCreateRep'),
    'create_board2': (By.CSS_SELECTOR, '.createBoardButton'),
    'name': (By.CSS_SELECTOR, '#boardEditName'),
    'description': (By.CSS_SELECTOR, '#boardEditDescription'),
    'category': (By.CSS_SELECTOR, 'select[name=category]'),
    'save_board': (By.CSS_SELECTOR, '.saveBoardButton'),
}

LIKE_SELECTORS = {'like': (By.CSS_SELECTOR, '.repinLike .LikeButton'), }

COMMENT_SELECTORS = {
    'comment_input': (By.CSS_SELECTOR, 'textarea.content'),
    'comment_button': (By.CSS_SELECTOR, '.addComment'),
}

REPIN_SELECTORS = {
    'pin': (By.CSS_SELECTOR, '.repin'),
    'boards': (By.CSS_SELECTOR, '.sectionItems:nth-child(2) .BoardLabel'),
}

FOLLOW_SELECTORS = {'follow': (By.CSS_SELECTOR, '.UserFollowButton'), }

UNFOLLOW_SELECTORS = {
    'pinners': (By.CSS_SELECTOR, 'a.navScopeBtn:nth-child(2)'),
    'unfollows': (By.CSS_SELECTOR, '.FollowButton'),
}
