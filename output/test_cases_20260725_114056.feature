Feature: As a user i want to login to application

  # NOTE: This is MOCK output (no AI call was made, $0 cost).
  # It is adapted from the most similar past example below as a placeholder.
  # For real AI-written test cases tailored to your exact story, either:
  #   1) add Anthropic API credits and re-run without --mock, or
  #   2) copy the prompt printed below into https://claude.ai for free.

  # Acceptance criteria considered:
  #   - For the user story:
  #   - **User Story:**
  #   - **As a user, I want to log in to the application so that I can securely access my account.**
  #   - ### Acceptance Criteria
  #   - 1. **Successful Login**
  #   - * Given the user is on the login page
  #   - * When the user enters a valid username/email and password
  #   - * Then the user is logged in successfully and redirected to the home/dashboard page.
  #   - 2. **Invalid Credentials**
  #   - * Given the user is on the login page
  #   - * When the user enters an invalid username/email or password
  #   - * Then an appropriate error message (e.g., "Invalid username or password") is displayed.
  #   - * And the user remains on the login page.
  #   - 3. **Mandatory Fields**
  #   - * Given the user is on the login page
  #   - * When the user clicks the **Login** button without entering the required credentials
  #   - * Then validation messages are displayed for all mandatory fields.
  #   - 4. **Password Masking**
  #   - * Given the user is on the login page
  #   - * Then the password field masks the entered characters.
  #   - 5. **Remember Me (if applicable)**
  #   - * Given the user selects the **Remember Me** option
  #   - * When the user logs in successfully
  #   - * Then the application remembers the user's login as per the defined session policy.
  #   - 6. **Forgot Password (if applicable)**
  #   - * Given the user is on the login page
  #   - * When the user clicks the **Forgot Password** link
  #   - * Then the user is redirected to the password reset page.
  #   - 7. **Session Creation**
  #   - * Given the user logs in successfully
  #   - * Then a valid authenticated session is created.
  #   - * And the user can access authorized pages without logging in again until the session expires or the user logs out.
  #   - 8. **Unauthorized Access**
  #   - * Given the user is not logged in
  #   - * When the user attempts to access a protected page
  #   - * Then the user is redirected to the login page.
  #   - 9. **Account Lock (if applicable)**
  #   - * Given the user enters incorrect credentials more than the configured number of times
  #   - * Then the account is locked or additional verification is required according to the application's security policy.
  #   - 10. **Logout**
  #   - * Given the user is logged in
  #   - * When the user clicks **Logout**
  #   - * Then the session is terminated.
  #   - * And the user is redirected to the login page.

  Scenario: Successful login with valid credentials
  Given a registered user with valid credentials
  When the user enters the correct email and password
  And clicks the login button
  Then the user is redirected to the dashboard

  Scenario: Login fails with incorrect password
  Given a registered user
  When the user enters a valid email and an incorrect password
  Then an error message "Invalid email or password" is displayed

  Scenario: Account locks after repeated failed attempts
  Given a registered user
  When the user enters incorrect credentials 5 times in a row
  Then the account is locked
  And the user sees a message indicating the account is locked
