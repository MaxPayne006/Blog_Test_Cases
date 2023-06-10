from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path  # path variable to the chromerdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object)
wait = WebDriverWait(driver, 20)


# Test 1: Register a new user
def register_new_user():
    # Open the browser and navigate to the registration page
    driver.get('http://127.0.0.1:9000/register')

    # Entering user details into the registration form
    name_input = driver.find_element(By.ID, 'name')
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')
    confirm_password_input = driver.find_element(By.ID, 'password-confirm')

    name_input.send_keys('Abdul Sammi')
    email_input.send_keys('abdul@gmail.com')
    password_input.send_keys('12345678')
    confirm_password_input.send_keys('12345678')

    # Click the "Register" button
    register_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[5]/div/button')
    register_button.click()
    try:
        dashboard = wait.until(EC.url_to_be('http://127.0.0.1:9000/dashboard'))
    except:
        print("Test 1 failed. User Registration Failed not redirected to the Dashboard.")
        return
    # Assert that the user is redirected to the home page after successful login
    assert dashboard, "Registration failed. User not redirected to the Dashboard."
    print("Test 1 passed. User Registered Successfully")
    driver.delete_all_cookies()
    

# Test 2: Login with invalid credentials
def login_with_invalid_credentials():
    
    # Open the browser and navigate to the login page
    driver.get('http://127.0.0.1:9000/login')

    # Entering valid credentials into the login form
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')

    email_input.send_keys('sammi@gmail.com')
    password_input.send_keys('123')

    # Click the "Login" button
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button')
    login_button.click()
    
    error_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div[1]')))

    # Get the text of the error element
    error_text = error_element.text

    # Assert that the error message matches the expected value
    expected_error_message = "These credentials do not match our records."
    assert error_text == expected_error_message, f"Test failed."
    print("Test 2 passed. Login with Invalid Credentials is handled correctly.")


# Test 3: Login with valid credentials
def login_with_valid_credentials():
    
    # Open the browser and navigate to the login page
    driver.get('http://127.0.0.1:9000/login')

    # Entering valid credentials into the login form
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')

    email_input.send_keys('abdul@gmail.com')
    password_input.send_keys('12345678')

    # Click the "Login" button
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button')
    login_button.click()
    try:
        dashboard = wait.until(EC.url_to_be('http://127.0.0.1:9000/dashboard'))
    except:
        print("Test 3 failed. Login Failed.")
        return
    # Assert that the user is redirected to the home page after successful login
    assert dashboard, "Login failed. User not redirected to the Dashboard."
    print("Test 3 passed. User is logged in and redirected to the dashboard.")
    driver.delete_all_cookies()
    

# Test 4: Create a new blog post
def create_new_post():
    # Open the browser and navigate to the login page
    driver.get('http://127.0.0.1:9000/login')
    # Entering valid credentials into the login form
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')
    checkbox = driver.find_element(By.ID, 'remember')

    email_input.send_keys('abdul@gmail.com')
    password_input.send_keys('12345678')
    checkbox.click()
    # Click the "Login" button
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button')
    login_button.click()
    wait.until(EC.url_to_be('http://127.0.0.1:9000/dashboard'))
    # Navigate to create post page
    driver.get(url='http://127.0.0.1:9000/posts/create')

    title_input = driver.find_element(By.ID, 'title')
    title_input.send_keys('Blog Post N0. 1')

    # Switch to the CKEditor iframe
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe.cke_wysiwyg_frame'))

    # Find the CKEditor textarea element
    ckeditor_textarea = driver.find_element(By.CSS_SELECTOR, 'body.cke_editable')

    # Clear the existing content (optional)
    ckeditor_textarea.clear()

    # Set the desired text in the CKEditor textarea by executing JavaScript
    text_to_send = "This is a test blog post."
    driver.execute_script("arguments[0].innerHTML = arguments[1]", ckeditor_textarea, text_to_send)

    # Switch back to the main content
    driver.switch_to.default_content()


    submit_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/form/input[2]')
    submit_button.send_keys(Keys.ENTER)

    posts = wait.until(EC.url_to_be('http://127.0.0.1:9000/posts'),message="Timeout")
    # Assert that the user is redirected to the home page after successful login
    assert posts, "Post Creation Failed."
    print("Test 4 passed. User is able to create posts")
    driver.delete_all_cookies()


# Test 5: Edit Blog post
def edit_post():
    # Open the browser and navigate to the login page
    driver.get('http://127.0.0.1:9000/login')
    # Entering valid credentials into the login form
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')
    checkbox = driver.find_element(By.ID, 'remember')

    email_input.send_keys('abdul@gmail.com')
    password_input.send_keys('12345678')
    checkbox.click()

    # Click the "Login" button
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button')
    login_button.click()
    wait.until(EC.url_to_be('http://127.0.0.1:9000/dashboard'))
    edit_btn = driver.find_element(By.XPATH,'//*[@id="app"]/main/div/div/div/div/div[2]/table/tbody/tr[2]/td[2]/a')
    edit_btn.click()

    # wait for sometime
    time.sleep(5) 

    title_input = driver.find_element(By.ID, 'title')
    title_input.send_keys(' Edited Blog Post')

    # Switch to the CKEditor iframe
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe.cke_wysiwyg_frame'))

    # Find the CKEditor textarea element
    ckeditor_textarea = driver.find_element(By.CSS_SELECTOR, 'body.cke_editable')

    # Clear the existing content (optional)
    ckeditor_textarea.clear()

    # Set the desired text in the CKEditor textarea by executing JavaScript
    text_to_send = "  This Blog Post is Edited"
    driver.execute_script("arguments[0].innerHTML = arguments[1]", ckeditor_textarea, text_to_send)

    # Switch back to the main content
    driver.switch_to.default_content()

    submit_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/form/input[3]')
    submit_button.send_keys(Keys.ENTER)
    posts = wait.until(EC.url_to_be('http://127.0.0.1:9000/posts'),message="Timeout")
    assert posts, "Failed to Edit Post."
    print("Test 5 passed. User is able to Edit posts")
    driver.delete_all_cookies()
    

# Test 6: Check Delete Blog Post 
def delete_post():
    driver.get('http://127.0.0.1:9000/login')
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'password')
    checkbox = driver.find_element(By.ID, 'remember')
    email_input.send_keys('abdul@gmail.com')
    password_input.send_keys('12345678')
    checkbox.click()
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div/div[2]/form/div[4]/div/button')
    login_button.click()
    wait.until(EC.url_to_be('http://127.0.0.1:9000/dashboard'))
    delete_button = driver.find_element(By.XPATH,'//*[@id="app"]/main/div/div/div/div/div[2]/table/tbody/tr[2]/td[3]/form/input[3]')
    delete_button.click()
    posts = wait.until(EC.url_to_be('http://127.0.0.1:9000/posts'),message="Timeout")
    assert posts, "Failed to Delete Post."
    print("Test 6 passed. User is able to Delete posts")
    driver.delete_all_cookies()


register_new_user()
login_with_invalid_credentials()
login_with_valid_credentials()
create_new_post()
edit_post()
delete_post()

driver.quit()



