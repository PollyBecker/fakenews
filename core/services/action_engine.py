from selenium.webdriver.common.keys import Keys
from core.services.navigator import Navigator


class ActionEngine:
    def __init__(self, navigator: Navigator):
        self.navigator = navigator

    def execute(self, action: dict):
        action_type = action.get('type')

        if action_type == 'open_url':
            self.navigator.open_url(action['url'])

        elif action_type == 'click':
            driver = self.navigator._get_driver()
            element = driver.execute_script(
                f"return document.elementFromPoint({action['x']}, {action['y']})"
            )
            if element:
                element.click()

        elif action_type == 'type':
            driver = self.navigator._get_driver()
            driver.switch_to.active_element.send_keys(action['text'])

        elif action_type == 'press_key':
            driver = self.navigator._get_driver()
            key = getattr(Keys, action['key'].upper(), action['key'])
            driver.switch_to.active_element.send_keys(key)

        elif action_type == 'scroll':
            self.navigator.scroll(action.get('amount', 300))

        elif action_type == 'done':
            pass
