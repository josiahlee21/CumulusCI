""" Tasks are the basic unit of execution in CumulusCI.

Subclass BaseTask or a descendant to define custom task logic
"""

import logging
import time

from cumulusci.core.exceptions import TaskRequiresSalesforceOrg
from cumulusci.core.exceptions import TaskOptionsError


class BaseTask(object):
    """ BaseTask provides the core execution logic for a Task

    Subclass BaseTask and provide a `_run_task()` method with your
    code.
    """
    task_options = {}
    salesforce_task = False  # Does this task require a salesforce org?

    def __init__(self, project_config, task_config,
                 org_config=None, flow=None, **kwargs):
        self.project_config = project_config
        self.task_config = task_config
        self.org_config = org_config
        self.return_values = {}
        """ a dict of return_values that can be used by task callers """
        self.result = None
        """ a simple result object for introspection, often a return_code """
        self.flow = flow
        """ The flow for this task execution """
        if self.salesforce_task and not self.org_config:
            raise TaskRequiresSalesforceOrg('This task requires a Saleforce '
                                            'org_config but none was passed '
                                            'to the Task constructor')
        self._init_logger()
        self._init_options(kwargs)
        self._validate_options()
        self._update_credentials()
        self._init_task()

    def _init_logger(self):
        """ Initializes self.logger """
        self.logger = logging.getLogger(__name__)

    def _init_options(self, kwargs):
        """ Initializes self.options """
        self.options = self.task_config.options
        if self.options is None:
            self.options = {}
        if kwargs:
            self.options.update(kwargs)

    def _validate_options(self):
        missing_required = []
        for name, config in self.task_options.items():
            if config.get('required') is True and name not in self.options:
                missing_required.append(name)

        if missing_required:
            raise TaskOptionsError(
                '{} requires the options ({}) '
                'and no values were provided'.format(
                    self.__class__.__name__,
                    ', '.join(missing_required)
                )
            )

    def _update_credentials(self):
        """ Override to do any logic  to refresh credentials """
        pass

    def _init_task(self):
        """ Override to implement dynamic logic for initializing the task. """
        pass

    def __call__(self):
        self._log_begin()
        self.result = self._run_task()
        return self.return_values

    def _run_task(self):
        """ Subclasses should override to provide their implementation """
        pass

    def _log_begin(self):
        """ Log the beginning of the task execution """
        self.logger.info('Beginning task: %s', self.__class__.__name__)
        if self.salesforce_task and not self.flow:
            self.logger.info('%15s %s', 'As user:', self.org_config.username)
            self.logger.info('%15s %s', 'In org:', self.org_config.org_id)
        self.logger.info('')

    def _retry(self):
        while True:
            try:
                self._try()
                break
            except Exception as e:
                if not (self.options['retries'] and self._is_retry_valid(e)):
                    raise
                if self.options['retry_interval']:
                    self.logger.warning(
                        'Sleeping for {} seconds before retry...'.format(
                        self.options['retry_interval']))
                    time.sleep(self.options['retry_interval'])
                    if self.options['retry_interval_add']:
                        self.options['retry_interval'] += self.options[
                            'retry_interval_add']
                self.options['retries'] -= 1
                self.logger.warning(
                    'Retrying ({} attempts remaining)'.format(
                    self.options['retries']))

    def _try(self):
        raise NotImplementedError(
            'Subclasses should provide their own implementation')

    def _is_retry_valid(self, e):
        return True
