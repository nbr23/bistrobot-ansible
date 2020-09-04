#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: bistrobot_buzz

short_description: Ring buzzer

version_added: "1.0"

description:
    - "Rings the buzzer on the specified GPIO pin"

options:
    buzzer_gpio_pin:
        description:
            - ID of the GPIO pin the buzzer is connected to
        required: true
    buzz_duration:
        description:
            - Number of 1/100 seconds to ring the buzzer for
        required: false

extends_documentation_fragment:
    - bistrobot

requirements:
    - bistrobot

author:
    - Maxence Ardouin
'''

EXAMPLES = '''
# Ring the buzzer on GPIO pin 17 for about 5/100 seconds
- name: Test buzzer on pin 17
  bistrobot_buzz:
    buzzer_gpio_pin: 17
    buzz_duration: 5
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from bistrobot import BistrobotBell

def run_module():
    module_args = dict(
        buzzer_gpio_pin=dict(type='int', required=True),
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
        bell.buzz(module.params['buzz_duration'])
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
