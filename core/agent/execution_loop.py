from core.services.navigator import Navigator
from core.services.screenshot import ScreenshotService
from core.services.vision import VisionService
from core.services.action_engine import ActionEngine
from core.agent.planner import Planner


class ExecutionLoop:
    def __init__(self, headless: bool = False):
        self.navigator = Navigator(headless=headless)
        self.screenshot = ScreenshotService(navigator=self.navigator)
        self.vision = VisionService()
        self.action_engine = ActionEngine(navigator=self.navigator)
        self.planner = Planner()

    def run_once(self, command: str) -> dict:
        image = self.screenshot.capture()
        ui_state = self.vision.analyze_ui(image, command)
        action = self.planner.decide(command, ui_state)
        self.action_engine.execute(action)
        return {'action': action, 'ui_state': ui_state}

    def run_goal(self, goal: str, max_steps: int = 10) -> list:
        history = []
        for _ in range(max_steps):
            image = self.screenshot.capture()
            ui_state = self.vision.analyze_ui(image, goal)
            action = self.planner.decide(goal, ui_state)
            self.action_engine.execute(action)
            history.append({'action': action, 'ui_state': ui_state})
            if action.get('type') == 'done':
                break
        return history

    def close(self):
        self.navigator.close()
