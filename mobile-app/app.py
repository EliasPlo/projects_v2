from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from plyer import notification
from datetime import datetime
import time
from kivy.clock import Clock

class TaskApp(App):
    def build(self):
        self.tasks = []
        self.layout = BoxLayout(orientation='vertical')
        
        # Text input for task
        self.task_input = TextInput(hint_text='Enter your task', multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.task_input)
        
        # Add task button
        self.add_button = Button(text='Add Task', size_hint_y=None, height=50)
        self.add_button.bind(on_press=self.add_task)
        self.layout.add_widget(self.add_button)
        
        # Scrollable task list
        self.scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 200))
        self.layout.add_widget(self.scroll)
        
        self.task_list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        self.scroll.add_widget(self.task_list_layout)

        return self.layout

    def add_task(self, instance):
        task_text = self.task_input.text
        if task_text:
            # Create task label
            task_label = Label(text=task_text, size_hint_y=None, height=40)
            self.task_list_layout.add_widget(task_label)
            
            # Add task to task list
            self.tasks.append(task_text)
            
            # Reset input field
            self.task_input.text = ''

            # Schedule a reminder (e.g. 10 seconds after the task is added)
            Clock.schedule_once(lambda dt: self.send_reminder(task_text), 10)

    def send_reminder(self, task):
        # Send notification reminder
        notification.notify(
            title="Task Reminder",
            message=f"Don't forget: {task}",
            timeout=10
        )

if __name__ == '__main__':
    TaskApp().run()
