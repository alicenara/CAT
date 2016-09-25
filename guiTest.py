from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from tests.perform_tests import test_initial_data


class CatWidget(Widget):
    pass


class CatApp(App):

    def build(self):
        parent = Widget()
        self.main_screen = CatWidget()
        test_btn = Button(text='Test :D')
        test_btn.bind(on_press=self.button_pressed)
        test_btn.bind(on_release=self.do_tests)
        parent.add_widget(self.main_screen)
        parent.add_widget(test_btn)
        return parent

    def button_pressed(self, obj):
        obj.text = "Wait!"
        obj.background_color = (0.0, 0.0, 1.0, 1.0)

    def do_tests(self, obj):
        if test_initial_data():
            obj.text = "Finished OK!"
            obj.background_color = (0.0, 1.0, 0.0, 1.0)
        else:
            obj.text = "Something went wrong"
            obj.background_color = (1.0, 0.0, 0.0, 1.0)


if __name__ == '__main__':
    CatApp().run()
