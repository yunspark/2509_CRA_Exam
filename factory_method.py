# # factory method
# from abc import ABC, abstractmethod
#
# class Dialog(ABC):
#     def render(self):
#         button = self.create_button()
#         button.on_click()
#
#     @abstractmethod
#     def create_button(self):
#         pass
#
# class WindowsDialog(Dialog):
#     def create_button(self):
#         return WindowsButton()
#
# class MacDialog(Dialog):
#     def create_button(self):
#         return MacButton()


# https://gist.github.com/jeonghwan-seo/a1b53b26e4d6f2cbbeecc035a93d791d

from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def run(self):
        pass


class SaveAction(Action):
    def run(self):
        print("파일 저장...")


class ExitAction(Action):
    def run(self):
        print("프로그램 종료...")


class Button(ABC):
    def click(self):
        action = self.create_action()
        action.run()

    @abstractmethod
    def create_action(self) -> Action:  # Factory Method
        pass


class SaveButton(Button):
    def create_action(self) -> Action:
        return SaveAction()


class ExitButton(Button):
    def create_action(self) -> Action:
        return ExitAction()


# 사용 예시
btn1 = SaveButton()
btn2 = ExitButton()

btn1.click()
btn2.click()
