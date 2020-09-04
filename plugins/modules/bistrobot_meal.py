#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: bistrobot_meal

short_description: Prompt Bistrobot to serve a meal

version_added: "1.0"

description:
    - "Serve a meal using the the gpio pins specified"

options:
    sensor_gpio_pin:
        description:
            - ID of the GPIO pin the feeder stop sensor is connected to.
        required: true
    feeder_gpio_pin:
        description:
            - ID of the GPIO ping the feeder motor is connected to. Pin used
            to activate the feeding itself.
        required: true
    buzzer_gpio_pin:
        description:
            - ID of the GPIO pin the buzzer is connected to. If specified,
            will ring the buzzer to announce the meal
        required: false
    buzz_duration:
        description:
            - Number of 1/100 seconds to ring the buzzer for
        required: false
    portion_number:
        description:
            - Number of portions to serve
        required: false

extends_documentation_fragment:
    - bistrobot

requirements:
    - bistrobot

author:
    - Maxence Ardouin
'''

EXAMPLES = '''
# Serve one meal using sensor GPIO 27 and feeder GPIO 22
- name: Serve a meal
  bistrobot_meal:
    sensor_gpio_pin: 27
    feeder_gpio_pin: 22

# Serve one meal using sensor GPIO 27 and feeder GPIO 22, announcing with
# buzzer on GPIO 17 for 10 1/100 seconds
- name: Announce and serve a meal
  bistrobot_meal:
    sensor_gpio_pin: 27
    feeder_gpio_pin: 22
    buzzer_gpio_pin: 17
    buzz_duration: 10

# Serve one meal of 2 portions using sensor GPIO 27 and feeder GPIO 22,
# announcing with buzzer on GPIO 17
- name: Announce and serve a meal of 2 portions
  bistrobot_meal:
    sensor_gpio_pin: 27
    feeder_gpio_pin: 22
    buzzer_gpio_pin: 17
    portion_number: 2
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from bistrobot import BistrobotBell, Bistrobot

def run_module():
    module_args = dict(
        sensor_gpio_pin=dict(type='int', required=True),
        feeder_gpio_pin=dict(type='int', required=True),
        buzzer_gpio_pin=dict(type='int', required=False),
        portion_number=dict(type='int', required=False, default=1),
        buzz_duration=dict(type='int', required=False, default=5),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        bell = BistrobotBell(module.params['buzzer_gpio_pin'])
        if 'buzzer_gpio_pin' in module.params:
            bell.buzz(module.params['buzz_duration'])
        bistrobot = Bistrobot(module.params['feeder_gpio_pin'],
                                module.params['sensor_gpio_pin'])
        bistrobot.serve_meal(module.params['portion_number'])
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
