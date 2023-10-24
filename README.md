# fishingbooker_task

- This Github repository contains tasks for automated tests (WEB and API) for FishingBooker QA task. 
- Tests are written 100% in Python.
- Tests can be run via AWS Ubuntu server with Jenkins (no-code) or via IDE terminal with installed prerequisites.
- Browser support for WEB test are Chrome and Firefox, running in headless.
- All tests are parameterized.
- Short 3-minute video showing test execution in Jenkins provided at the end of the README file.

## How to run tests 

### Option 1 via AWS server with Jenkins (easiest)

- Login to http://54.242.33.182:8080/
- username: fishingbookers
- password: mocMOC123
- Choose API or WEB job
- Choose the "Build with parameters" option
  - For WEB tests, we can use the following parameters: name (test name using allure mark, default is task), browser (chrome or firefox), URL (any FishingBooker URL)
  - For API tests, we can use the following parameter: name (test name using allure mark, positive or negative)
- Click on the Build button
- On job execution, the Allure report will be generated (for both WEB and API tests)

### Option 2 via Pycharm (or other IDE) and terminal (prerequisite Python3)

- Clone git repository into IDE
- Open terminal 
- Make sure the path in the terminal is the root folder of the project
- Create a virtual environment 
  - For Mac inside the terminal within the root folder of the project type the following:
      ```
     pip install virtualenv
      ```
      ```
     virtualenv venv
      ```
      ```
     source venv/bin/activate
      ```
- After you successfully created and activated the virtual environment, install requirements needed by typing the following:
    ```
   pip install -r requirements.txt
    ```

- Run tests by typing the following:
  - For WEB tests:
    ```
     pytest --browser=firefox apps/ui/tests -m task --alluredir=/tmp/task1 --url=https://qahiring.dev.fishingbooker.com => to run test
    ```
    ```
     allure serve /tmp/task1 => to open Allure report after the test is done
    ```
  - For API tests:
    ```
     pytest apps/api/test_crew_members_photos.py -m positive --alluredir=/tmp/fbapi1 => to run test
    ```
    ```
     allure serve /tmp/fbapi1 => to open Allure report after the test is done   
    ```
    
## Video link
https://www.youtube.com/watch?v=R0rsUVOiq1c
