# Gotify Notifications

The `gotify` notification platform enables you to easily send notifications with a custom prioirty and extra information via [Gotify](https://gotify.net/).

### Installation
The recommendet way to install the integration is via [HACS](https://hacs.xyz/).
If you want to install it manually copy the `homeassistant-gotify` directory to the `<config_dir>/custom_components` directory of HomeAssistant.

### Configuration
This integration exposes itself as a [notifications integration](https://www.home-assistant.io/integrations/notify/) and configured by adding the folowing snippet to the `configuration.yaml` file:
```yaml
notify:
  - name: "my gotify"
    platform: gotify
    url: <gotify_url>
    token: <gotify_token>
```
Replace `<gotify_url>` and `<gotify_token>` with the url of your Gotify instance and the application token to be used.

### Usage
This integration accepts the same values as the official Gotify API. For a full list of extras that can be added to a notification refer to the [Gotify docs](https://gotify.net/docs/msgextras). Here a few examples:

#### Simple text message
```yaml
action:
  - service: notify.my_gotify
    data:
      message: "This is a test message."
```

#### Message with title and priority
```yaml
action:
  - service: notify.my_gotify
    data:
      message: "This is a test message."
      title: "Gotify Test"
      data:
        priority: 10
```

#### Message with click event
```yaml
action:
  - service: notify.my_gotify
    data:
      message: "This is a test message."
      title: "Gotify Test"
      data:
        priority: 10
        extras:
          'client::notification':
            click:
              url: https://www.home-assistant.io/
```

##### Message with image
```yaml
action:
  - service: notify.my_gotify
    data:
      message: "This is a test message."
      title: "Gotify Test"
      data:
        priority: 10
        extras:
          'client::notification':
            bigImageUrl: https://placekitten.com/400/300
```

### License
The whole project is under the [GPL-3 license](https://www.gnu.org/licenses/gpl-3.0.html).